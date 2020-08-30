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
from django.db.models import Model
from typing import List, Tuple, Dict

from get_data.job import currency


class FactorConverter:
    """
    A class with a collection of methods to convert factor returns in other currencies than USD.
    """

    def __init__(
        self,
        df_fxrates_d: pd.DataFrame,
        df_fxrates_m: pd.DataFrame,
        df_fxrates_a: pd.DataFrame,
        df_rf_usd_d: pd.DataFrame,
        df_rf_usd_m: pd.DataFrame,
        df_rf_usd_a: pd.DataFrame,
        dict_rf_d: Dict[pd.DataFrame],
        dict_rf_m: Dict[pd.DataFrame],
        dict_rf_a: Dict[pd.DataFrame],
    ) -> None:
        """
        Create an instance of class and set all fx rate returns and riskfree rates for currency conversion.

        Args:

        """
        self.df_fxrates_r_d = round((df_fxrates_d / df_fxrates_d.shift(periods=1) - 1), 8)
        self.df_fxrates_r_d.drop(self.df_fxrates_r_d.index[:1], inplace=True)
        self.df_fxrates_r_m = round((df_fxrates_m / df_fxrates_m.shift(periods=1) - 1), 8)
        self.df_fxrates_r_m.drop(self.df_fxrates_r_m.index[:1], inplace=True)
        self.df_fxrates_r_a = round((df_fxrates_a / df_fxrates_a.shift(periods=1) - 1), 8)
        self.df_fxrates_r_a.drop(self.df_fxrates_r_a.index[:1], inplace=True)

        self.df_rf_usd_d = df_rf_usd_d
        self.df_rf_usd_m = df_rf_usd_m
        self.df_rf_usd_a = df_rf_usd_a

        self.dict_rf_d = dict_rf_d
        self.dict_rf_m = dict_rf_m
        self.dict_rf_a = dict_rf_a

    def get_fxrates_r(self, freq: str) -> pd.DataFrame:
        """
        Get fx rate returns

        Args:
            freq: The frequency of the fx rate returns. D (daily), M (monthly) or A (annually).

        Returns:
            A Pandas dataframe with the desired fx rate returns.

        Raises:
            ValueError: If invalid frequency passed.
        """

        if freq == "D":
            return self.df_fxrates_r_d
        elif freq == "M":
            return self.df_fxrates_r_m
        elif freq == "A":
            return self.df_fxrates_r_a
        else:
            raise ValueError(
                "Invalid frequency. Choose D (daily), M (monthly) or A (annually)."
            )

    def get_rf_usd(self, freq: str) -> pd.DataFrame:
        """
        Get riskfree rates for USD

        Args:
            freq: The frequency of the riskfree rates. D (daily), M (monthly) or A (annually).

        Returns:
            A Pandas dataframe with the desired riskfree rates in USD.

        Raises:
            ValueError: If invalid frequency passed.
        """

        if freq == "D":
            return self.dict_rf_d[currency]
        elif freq == "M":
            return self.dict_rf_m[currency]
        elif freq == "A":
            return self.dict_rf_a[currency]
        else:
            raise ValueError(
                "Invalid frequency. Choose D (daily), M (monthly) or A (annually)."
            )

    def get_rf_target(self, freq: str, currency: str) -> pd.DataFrame:
        """
        Get riskfree rates for target currency.

        Args:
            freq: The frequency of the riskfree rates. D (daily), M (monthly) or A (annually).
            currency: The target currency.

        Returns:
            A Pandas dataframe with the desired riskfree rates for the target currency.

        Raises:
            ValueError: If invalid frequency passed.
            ValueError: If no data exists for currency given.
        """
        try:
            if freq == "D":
                return self.df_rf_t
            elif freq == "M":
                return self.df_rf_usd_m
            elif freq == "A":
                return self.df_rf_usd_a
            else:
                raise ValueError(
                    "Invalid frequency. Choose D (daily), M (monthly) or A (annually)."
                )
        except KeyError:
            raise ValueError("No rf data for currency given.")

    def convert_mktrf(
        self, s_factor_source: pd.Series, freq: str, currency: str
    ) -> pd.Series:
        """
        Convert market factor returns series following Glueck et al. (2020) to different currency.

        Args:
            s_fxrates_r: The pandas series of fx rates returns
            s_rf_source: The pandas series of risk free rates of source currency
            s_rf_target: The pandas series of risk free rates of target currency
            s_factor_source: The pandas series of factor returns in original currency

        Returns:
            A currency converted pandas series of factor returns
        """

        return round(
            1 / (1 + s_fxrates_r) * (1 + s_factor_source + s_rf_source) - 1 - s_rf_target,
            4,
        )

    def convert_longShortFactor(
        self, s_fxrates_r: pd.Series, s_factor_source: pd.Series
    ) -> pd.Series:
        """
        Convert factor returns series following Glueck et al. (2020) to different currency.

        Args:
            s_fxrates_r: The pandas series of fx rates returns
            s_factor_source: The pandas series of factor returns in original currency

        Returns:
            A currency converted pandas series of factor returns
        """

        return round(1 / (1 + s_fxrates_r) * s_factor_source, 4)

    def convert_dataframe(
        self, df_factor_source: pd.DataFrame, region: str, currency: str, freq: str
    ) -> pd.DataFrame:
        """
        Converts a Pandas dataframe with factor returns from USD to currency given.

        Args:
            df_factor_source: The Pandas dataframe with the original USD factor returns.
            df_fxrates_r: The Pandas dataframe with the fx rates returns.
            df_rf_source: The Pandas dataframe with the USD rf.
            region: The region of the factor returns.
            currency: The desired currency of the factor returns.

        Returns:
            A Pandas dataframe with the currency-converted factor returns.
        """

        # Check rf dict for rf for currency given, default to USD rf
        try:
            df_rf_target = dict_rf_target[currency]
        except KeyError:
            df_rf_target = df_rf_source

        # Convert factor returns
        df_factor_target = pd.DataFrame()
        df_factor_target["MktRF"] = self.convert_mktrf(
            df_fxrates_r[currency],
            df_rf_source["RF"],
            df_rf_target["RF"],
            df_factor_source["MktRF"],
        )
        df_factor_target["SMB"] = convert_factor(
            df_fxrates_r[currency], df_factor_source["SMB"]
        )
        df_factor_target["HML"] = convert_factor(
            df_fxrates_r[currency], df_factor_source["HML"]
        )
        df_factor_target["MOM"] = convert_factor(
            df_fxrates_r[currency], df_factor_source["MOM"]
        )

        if "RMW" in df_factor_source and "CMA" in df_factor_source:
            df_factor_target["RMW"] = convert_factor(
                df_fxrates_r[currency], df_factor_source["RMW"]
            )
            df_factor_target["CMA"] = convert_factor(
                df_fxrates_r[currency], df_factor_source["CMA"]
            )

        # If MktRF for given interval is NaN (due to missing rf), remove instance
        df_factor_target = df_factor_target.loc[
            df_factor_target["MktRF"]
            .first_valid_index() : df_factor_target["MktRF"]
            .last_valid_index()
        ]

        # Set currency and region
        df_factor_target["currency"] = currency
        df_factor_target["region"] = region

        return df_factor_target


class Fetchers:
    """
    """

    @staticmethod
    def get_french_factors(
        zip_filename: str, csv_filename: str, freq: str
    ) -> pd.DataFrame:
        """
        Get factor data from Kenneth French's data library and clean it up.

        Args:
            zip_filename: A string with the zip file name.
            csv_filename: A string with the CSV file name.
            freq: The frequency of factor data. Daily, monthly or annually.

        Returns:
            A pandas dataframe with the factor returns in US dollar.

        Raises:
            ConnectionError: If Kenneth French's data library returns bad answer.
        """

        request_string = f"https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{zip_filename}.zip"

        r = requests.get(request_string)

        if r.status_code != 200:
            raise ConnectionError("Error: Could not get " + request_string)

        z = zipfile.ZipFile(io.BytesIO(r.content))
        data = io.TextIOWrapper(z.open(csv_filename, "r"))
        tuple_list: List[Tuple[float]] = []

        # Choose length of date interval strings
        if freq == "D":
            date_length = 8
        elif freq == "M":
            date_length = 6
        else:
            date_length = 4

        # Following code is complex due to machine incompatibility of CSV files in Kenneth French's data library
        with data as file:
            reader = csv.reader(file)
            for row in reader:
                # Look for rows with the data wanted
                if row and re.match(r"\s*\d{" + str(date_length) + r"}\s*\b", row[0]):
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
                        np.float64(round(float(value) / 100, 8)) for value in row[1:]
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

    @staticmethod
    def get_ecb_riskfreeRates(freq: str) -> pd.DataFrame:
        """
        Get riskfree rates from ECB (Daily rates: EONIA, monthly or annually rates: EURIBOR 1M)

        Args:
            freq: The frequency of risk free rates. Daily, monthly or annually.

        Returns:
            A pandas dataframe with the risk free rates in EUR.

        Raises:
            NotImplementedError: If frequency given is not supported.
            ConnectionError: If ECB API endpoint returns bad answer.
        """

        if freq == "D":
            identifier = "EON/D.EONIA_TO.RATE"
        elif freq == "M":
            identifier = "FM/M.U2.EUR.RT.MM.EURIBOR1MD_.HSTA"
        elif freq == "A":
            identifier = "FM/M.U2.EUR.RT.MM.EURIBOR1MD_.HSTA"
        else:
            raise NotImplementedError("Frequency not supported.")

        request_string = f"https://sdw-wsrest.ecb.europa.eu/service/data/{identifier}"
        r = requests.get(request_string)

        if r.status_code != 200:
            raise ConnectionError("Error: Could not get " + request_string)

        with io.BytesIO(r.content) as file:
            tree = ET.parse(file)
            root = tree.getroot()
            # Register namespace to improve XPath readability
            ns = {
                "x": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
                "y": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
            }
            root_list = root.findall("x:DataSet/y:Series/y:Obs", ns)

            tuple_list: List[Tuple[float]] = []

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
                    value = np.float64(round(float(obs[1].attrib["value"]) / 100 / 12, 8))
                    tuple_list.append((date, value))
            elif freq == "A":
                for obs in root_list:
                    # Look for december rates
                    if re.match(r"\s*\d{4}-12\s*", obs[0].attrib["value"]):
                        date = obs[0].attrib["value"][:-3]
                        value = np.float64(round(float(obs[1].attrib["value"]) / 100, 8))
                        tuple_list.append((date, value))

        df = pd.DataFrame(tuple_list, columns=["interval", "RF"]).set_index("interval")

        if freq == "D":
            # Get date vector without missing dates
            full_datevector = [
                date.strftime("%Y-%m-%d")
                for date in pd.date_range(start=df.index[0][:4], end=df.index[-1])
            ]
            return df.reindex(full_datevector)

        return df

    @staticmethod
    def get_boe_fxRates(freq: str) -> pd.DataFrame:
        """
        Get 16.00 London time exchange rates against USD from Bank of England API.

        Args:
            freq: The frequency of exchange rates. Daily, monthly or annually.

        Returns:
            A Pandas dataframe with the exchange rates.

        Raises:
            ConnectionError: If Bank of England API returns bad answer.
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
                ConnectionError("Error: Could not get " + request_string)

            with io.BytesIO(r.content) as file:
                try:
                    tree = ET.parse(file)
                except ET.ParseError:
                    raise ConnectionError(
                        "Bank of England API returned bad answer. Please try again."
                    )
                root = tree.getroot()
                ns = {"x": "http://www.bankofengland.co.uk/boeapps/iadb/agg_series"}
                root_list = root.findall("x:Cube/x:Cube[@TIME][@OBS_VALUE]", ns)

            tuple_list: List[Tuple[float]] = []

            if freq == "D":
                for cube in root_list:
                    date = cube.attrib["TIME"]
                    value = np.float64(round(1 / float(cube.attrib["OBS_VALUE"]), 8))
                    tuple_list.append((date, value))
            elif freq == "M":
                for cube in root_list:
                    date = cube.attrib["TIME"][:-3]
                    value = np.float64(round(1 / float(cube.attrib["OBS_VALUE"]), 8))
                    tuple_list.append((date, value))
            elif freq == "A":
                for cube in root_list:
                    date = cube.attrib["TIME"][:-6]
                    value = np.float64(round(1 / float(cube.attrib["OBS_VALUE"]), 8))
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


# TODO: Add as methods to models, refactor repeating code


def build_model(model: Model, df: pd.DataFrame) -> None:
    """
    Create or update instances of given model with data in dataframe.
    Implemented using batches of SQL queries.

    Args:
        model: The Django ORM model to add or update data to.
        df: The Pandas dataframe with the data to add or update.

    Raises:
        NotImplementedError: If unknown model is passed in args.
    """

    # Change NaN to None for database NULL compatibility
    df = df.where(df.notnull(), None)

    update_list: List[model] = []
    create_list: List[model] = []

    currency = df["currency"].iloc[0] if "currency" in df else ""
    region = df["region"].iloc[0] if "region" in df else ""

    for index, row in df.iterrows():
        row_dict = row.to_dict()
        new_instance = model(interval=row.name, **row_dict)
        try:
            if "Factor" in model.__name__:
                instance = model.objects.get(
                    interval=row.name, currency=row["currency"], region=row["region"],
                )
            elif "RiskFreeRate" in model.__name__:
                instance = model.objects.get(interval=row.name, currency=row["currency"])
            elif "ExchangeRate" in model.__name__:
                instance = model.objects.get(interval=row.name)
            else:
                raise NotImplementedError(
                    "Unknown model. Please add query pattern to build_model function."
                )
            if not instance == new_instance:
                update_list.append(new_instance)
        except ObjectDoesNotExist:
            create_list.append(new_instance)

    # Only update database if there is something to update
    if update_list:
        model.objects.bulk_update(update_list, df.columns.values.to_list())
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


def build_base_dataframes(
    df_factors: pd.DataFrame, df_mom: pd.DataFrame, region: str, with_rf: bool = False,
) -> Tuple[pd.DataFrame, None]:
    """
    Clean and parse raw factor return dataframes from Kenneth French's data library.

    Args:
        df_factors: The Pandas dataframe with the raw data.
        df_mom: The Pandas dataframe with the momentum factor return data.
        region: The region the factor returns are for.
        with_rf: True if rf should be returned as separate dataframe, False if rf should be dropped.

    Returns:
        A tuple with the cleaned and with momentum merged dataframe with factor returns and the rf dataframe if with_rf is true (else None).
    """

    # Merge with momentum factor
    df_factors["MOM"] = df_mom["MOM"]
    df_factors["currency"] = "USD"
    df_factors["region"] = region

    if with_rf:
        df_rf = df_factors[["RF"]]
        df_rf["currency"] = "USD"
        df_factors.drop(["RF"], axis=1, inplace=True)
        return df_factors, df_rf

    # If rf is not needed, drop data
    df_factors.drop(["RF"], axis=1, inplace=True)

    return df_factors, None
