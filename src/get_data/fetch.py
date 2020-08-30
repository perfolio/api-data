import io
import csv
import zipfile
import datetime
import re
import requests
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from typing import List, Tuple


class Fetchers:
    """
    A class with a collection of static methods to fetch data from specific endpoints.
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
            ValueError: If frequency given is not supported.
            ConnectionError: If ECB API endpoint returns bad answer.
        """

        if freq == "D":
            identifier = "EON/D.EONIA_TO.RATE"
        elif freq == "M":
            identifier = "FM/M.U2.EUR.RT.MM.EURIBOR1MD_.HSTA"
        elif freq == "A":
            identifier = "FM/M.U2.EUR.RT.MM.EURIBOR1MD_.HSTA"
        else:
            raise ValueError("Frequency not supported.")

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
