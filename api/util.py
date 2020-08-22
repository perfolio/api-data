import sys
import io
import csv
import zipfile
import datetime
import re
import requests
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist


def errorhandler(message):
    """
    Print error message and exit with code 1.

    - message: The error message to print.
    """

    print(message)
    sys.exit(1)


def get_french_data(zip_filename, csv_filename, freq):
    """
    Get factor data from Kenneth French's data library and clean it up.

    - zip_filename: A string with the zip file name.
    - csv_filename: A string with the CSV file name.
    - freq: The frequency of factor data. Daily, monthly or annually.

    Returns: A pandas dataframe with the factor returns in US dollar.
    """

    request_string = f"https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{zip_filename}.zip"

    r = requests.get(request_string)

    if r.status_code != 200:
        errorhandler(message="Error: Could not get " + request_string)

    z = zipfile.ZipFile(io.BytesIO(r.content))
    data = io.TextIOWrapper(z.open(csv_filename, "r"))
    tuple_list = []

    # Choose length of date interval strings
    if freq == "D":
        date_length = 8
    elif freq == "M":
        date_length = 6
    else:
        date_length = 4

    with data as file:
        reader = csv.reader(file)
        for row in reader:
            # Look for rows with the data wanted
            if row and re.match(
                r"\s*\d{" + str(date_length) + r"}\s*\b", row[0]
            ):
                if freq == "D":
                    row[0] = datetime.datetime.strptime(
                        row[0].strip(), "%Y%m%d"
                    ).strftime("%Y-%m-%d")
                elif freq == "M":
                    row[0] = datetime.datetime.strptime(
                        row[0].strip(), "%Y%m"
                    ).strftime("%Y-%m")
                else:
                    row[0] = row[0].strip()

                # Convert string to float
                row[1:] = [
                    np.float64(round(float(value) / 100, 8))
                    for value in row[1:]
                ]
                tuple_list.append(tuple(row))

    if re.search(r".*_5_.*", zip_filename):
        column_names = ["interval", "MktRF", "SMB", "HML", "RMW", "CMA", "RF"]
    elif re.search(r".*Momentum.*", zip_filename) or re.search(
        r".*MOM.*", zip_filename
    ):
        column_names = ["interval", "MOM"]
    else:
        column_names = ["interval", "MktRF", "SMB", "HML", "RF"]

    df = pd.DataFrame(tuple_list, columns=column_names).set_index("interval")

    if freq == "D":
        # Get date vector without missing dates
        full_datevector = [
            date.strftime("%Y-%m-%d")
            for date in pd.date_range(start=df.index[0][:7], end=df.index[-1])
        ]
        return df.reindex(full_datevector)

    return df


def get_ecb_riskfree_rates(freq):
    """
    Get riskfree rates from ECB (Daily rates: EONIA, monthly or annually rates: EURIBOR 1M)

    - freq: The frequency of risk free rates. Daily, monthly or annually.

    Returns: A pandas dataframe with the risk free rates in EUR.
    """

    if freq == "D":
        identifier = "EON/D.EONIA_TO.RATE"
    elif freq == "M":
        identifier = "FM/M.U2.EUR.RT.MM.EURIBOR1MD_.HSTA"
    elif freq == "A":
        identifier = "FM/M.U2.EUR.RT.MM.EURIBOR1MD_.HSTA"
    else:
        errorhandler("Error: Invalid frequency given.")

    request_string = (
        f"https://sdw-wsrest.ecb.europa.eu/service/data/{identifier}"
    )
    r = requests.get(request_string)

    if r.status_code != 200:
        errorhandler(message="Error: Could not get " + request_string)

    with io.BytesIO(r.content) as file:
        tree = ET.parse(file)
        root = tree.getroot()
        # Register namespace to improve XPath readability
        ns = {
            "x": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
            "y": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
        }
        root_list = root.findall("x:DataSet/y:Series/y:Obs", ns)

        tuple_list = []

        if freq == "D":
            for obs in root_list:
                date = obs[0].attrib["value"]
                value = np.float64(
                    round(float(obs[1].attrib["value"]) / 100 / 360, 8)
                )
                tuple_list.append((date, value))
        elif freq == "M":
            for obs in root_list:
                date = obs[0].attrib["value"]
                value = np.float64(
                    round(float(obs[1].attrib["value"]) / 100 / 12, 8)
                )
                tuple_list.append((date, value))
        elif freq == "A":
            for obs in root_list:
                # Look for december rates
                if re.match(r"\s*\d{4}-12\s*", obs[0].attrib["value"]):
                    date = obs[0].attrib["value"][:-3]
                    value = np.float64(
                        round(float(obs[1].attrib["value"]) / 100, 8)
                    )
                    tuple_list.append((date, value))

    df = pd.DataFrame(tuple_list, columns=["interval", "RF"]).set_index(
        "interval"
    )

    if freq == "D":
        # Get date vector without missing dates
        full_datevector = [
            date.strftime("%Y-%m-%d")
            for date in pd.date_range(start=df.index[0][:4], end=df.index[-1])
        ]
        return df.reindex(full_datevector)

    return df


def get_boe_exchange_rates(freq):
    """
    Get 16.00 London time exchange rates against USD.

    - freq: The frequency of exchange rates. Daily, monthly or annually.

    Returns: A pandas dataframe with the exchange rates.
    """
    currency_identifier_map = {
        "EUR": {"A": "XUALERD", "M": "XUMLERD", "D": "XUDLERD"},
        "JPY": {"A": "XUALJYD", "M": "XUMLJYD", "D": "XUDLJYD"},
        "GBP": {"A": "XUALGBD", "M": "XUMLGBD", "D": "XUDLGBD"},
        "CHF": {"A": "XUALSFD", "M": "XUMLSFD", "D": "XUDLSFD"},
        "RUB": {"A": "XUALBK69", "M": "XUMLBK69", "D": "XUDLBK69"},
        "AUD": {"A": "XUALADD", "M": "XUMLADD", "D": "XUDLADD"},
        "BRL": {"A": "XUALB8KL", "M": "XUMLB8KL", "D": "XUDLB8KL"},
        "CAD": {"A": "XUALCDD", "M": "XUMLCDD", "D": "XUDLCDD"},
        "CNY": {"A": "XUALBK73", "M": "XUMLBK73", "D": "XUDLBK73"},
        "INR": {"A": "XUALBK64", "M": "XUMLBK64", "D": "XUDLBK64"},
        "DKK": {"A": "XUALDKD", "M": "XUMLDKD", "D": "XUDLDKD"},
        "NZD": {"A": "XUALNDD", "M": "XUMLNDD", "D": "XUDLNDD"},
        "NOK": {"A": "XUALNKD", "M": "XUMLNKD", "D": "XUDLNKD"},
        "SEK": {"A": "XUALSKD", "M": "XUMLSKD", "D": "XUDLSKD"},
        "PLN": {"A": "XUALBK49", "M": "XUMLBK49", "D": "XUDLBK49"},
        "ILS": {"A": "XUALBK65", "M": "XUMLBK65", "D": "XUDLBK65"},
        "KRW": {"A": "XUALBK74", "M": "XUMLBK74", "D": "XUDLBK74"},
        "TRY": {"A": "XUALBK75", "M": "XUMLBK75", "D": "XUDLBK75"},
    }

    df = pd.DataFrame()

    for key in currency_identifier_map:
        request_string = "http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?CodeVer=new&xml.x=yes"
        params = {
            "Datefrom": "01/Jan/1963",
            "Dateto": "now",
            "SeriesCodes": currency_identifier_map[key][freq],
        }

        r = requests.get(request_string, params=params)

        if r.status_code != 200:
            errorhandler(message="Error: Could not get " + request_string)

        with io.BytesIO(r.content) as file:
            try:
                tree = ET.parse(file)
            except ET.ParseError:
                errorhandler(
                    "Bank of England API returned bad answer. Please try again."
                )
            root = tree.getroot()
            ns = {
                "x": "http://www.bankofengland.co.uk/boeapps/iadb/agg_series"
            }
            root_list = root.findall("x:Cube/x:Cube[@TIME][@OBS_VALUE]", ns)

        tuple_list = []

        if freq == "D":
            for cube in root_list:
                date = cube.attrib["TIME"]
                value = np.float64(
                    round(1 / float(cube.attrib["OBS_VALUE"]), 8)
                )
                tuple_list.append((date, value))
        elif freq == "M":
            for cube in root_list:
                date = cube.attrib["TIME"][:-3]
                value = np.float64(
                    round(1 / float(cube.attrib["OBS_VALUE"]), 8)
                )
                tuple_list.append((date, value))
        elif freq == "A":
            for cube in root_list:
                date = cube.attrib["TIME"][:-6]
                value = np.float64(
                    round(1 / float(cube.attrib["OBS_VALUE"]), 8)
                )
                tuple_list.append((date, value))

        if df.empty:
            df = pd.DataFrame(tuple_list, columns=["interval", key]).set_index(
                "interval"
            )
        else:
            df = df.join(
                pd.DataFrame(tuple_list, columns=["interval", key]).set_index(
                    "interval"
                )
            )

    if freq == "D":
        # Get date vector without missing dates
        full_datevector = [
            date.strftime("%Y-%m-%d")
            for date in pd.date_range(start=df.index[0][:4], end=df.index[-1])
        ]
        return df.reindex(full_datevector)

    return df


def build_model(model, df):
    """
    """

    # Change NaN to None for database NULL compatibility
    df = df.where(df.notnull(), None)

    update_list = []
    create_list = []

    currency = df["currency"].iloc[0] if "currency" in df else ""
    region = df["region"].iloc[0] if "region" in df else ""

    for index, row in df.iterrows():
        row_dict = row.to_dict()
        new_instance = model(interval=row.name, **row_dict)
        try:
            if "Factor" in model.__name__:
                instance = model.objects.get(
                    interval=row.name,
                    currency=row["currency"],
                    region=row["region"],
                )
            elif "RiskFreeRate" in model.__name__:
                instance = model.objects.get(
                    interval=row.name, currency=row["currency"]
                )
            elif "ExchangeRate" in model.__name__:
                instance = model.objects.get(interval=row.name)
            else:
                errorhandler(
                    "Unknown model. Please add query pattern to build_model function."
                )
            if not instance == new_instance:
                update_list.append(new_instance)
        except ObjectDoesNotExist:
            create_list.append(new_instance)

    # Only update database if there is something to update
    if update_list:
        model.objects.bulk_update(update_list, row.index.to_list())
    if create_list:
        model.objects.bulk_create(create_list)

    # Print result
    if currency and region:
        print(
            f"{len(create_list)} created, {len(update_list)} updated, {len(df.index) - len(create_list) - len(update_list)} unchanged in {model.__name__} for region {region} and currency {currency}."
        )
    elif currency:
        print(
            f"{len(create_list)} created, {len(update_list)} updated, {len(df.index) - len(create_list) - len(update_list)} unchanged in {model.__name__} for currency {currency}."
        )
    else:
        print(
            f"{len(create_list)} created, {len(update_list)} updated, {len(df.index) - len(create_list) - len(update_list)} unchanged in {model.__name__}."
        )


def convert_dataframe(
    df_factor_source,
    df_fxrates_r,
    df_rf_source,
    dict_rf_target,
    region,
    currency,
):
    try:
        df_rf_target = dict_rf_target[currency]
    except KeyError:
        df_rf_target = df_rf_source

    df_factor_target = pd.DataFrame()
    df_factor_target["MktRF"] = round(
        1
        / (1 + df_fxrates_r[currency])
        * (1 + df_factor_source["MktRF"] + df_rf_source["RF"])
        - 1
        - df_rf_target["RF"],
        4,
    )
    df_factor_target["SMB"] = round(
        1 / (1 + df_fxrates_r[currency]) * df_factor_source["SMB"], 4
    )
    df_factor_target["HML"] = round(
        1 / (1 + df_fxrates_r[currency]) * df_factor_source["HML"], 4
    )
    df_factor_target["MOM"] = round(
        1 / (1 + df_fxrates_r[currency]) * df_factor_source["MOM"], 4
    )

    if "RMW" in df_factor_source and "CMA" in df_factor_source:
        df_factor_target["RMW"] = round(
            1 / (1 + df_fxrates_r[currency]) * df_factor_source["RMW"], 4
        )
        df_factor_target["CMA"] = round(
            1 / (1 + df_fxrates_r[currency]) * df_factor_source["CMA"], 4
        )

    df_factor_target = df_factor_target.loc[
        df_factor_target["MktRF"]
        .first_valid_index() : df_factor_target["MktRF"]
        .last_valid_index()
    ]
    df_factor_target["currency"] = currency
    df_factor_target["region"] = region

    return df_factor_target


def build_base_dataframes(df_factors, df_mom, region, with_rf=False):
    df_factors["MOM"] = df_mom["MOM"]
    df_factors["currency"] = "USD"
    df_factors["region"] = region

    if with_rf:
        df_rf = df_factors[["RF"]]
        df_rf["currency"] = "USD"
        df_factors.drop(["RF"], axis=1, inplace=True)
        return df_factors, df_rf

    df_factors.drop(["RF"], axis=1, inplace=True)
    return df_factors, None
