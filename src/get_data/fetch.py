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
from get_data.config.boe import currency_identifier_map
from get_data.config.ecb import rf_identifier_map


class Fetcher:
    """
    A class with a collection of static methods to fetch data from specific endpoints.
    """

    @staticmethod
    def french_factors(
        zip_filename: str, csv_filename: str, interval: str
    ) -> pd.DataFrame:
        """
        Get factor data from Kenneth French's data library and clean it up.

        Args:
            zip_filename: A string with the zip file name.
            csv_filename: A string with the CSV file name.
            interval: The interval of factor data. Daily, monthly or annual.

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
        if interval == "daily":
            date_length = 8
        elif interval == "monthly":
            date_length = 6
        else:
            date_length = 4

        # Following code is complex due to machine incompatibility of CSV files in Kenneth French's data library
        with data as file:
            reader = csv.reader(file)
            for row in reader:
                # Look for rows with the data wanted
                if row and re.match(r"\s*\d{" + str(date_length) + r"}\s*\b", row[0]):
                    if interval == "daily":
                        row[0] = datetime.datetime.strptime(
                            row[0].strip(), "%Y%m%d"
                        ).strftime("%Y-%m-%d")
                    elif interval == "monthly":
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
            column_names = ["period", "mktrf", "smb", "hml", "rmw", "cma", "rf"]
        elif re.search(r".*Momentum.*", zip_filename) or re.search(
            r".*MOM.*", zip_filename
        ):
            column_names = ["period", "mom"]
        else:
            column_names = ["period", "mktrf", "smb", "hml", "rf"]

        df = pd.DataFrame(tuple_list, columns=column_names).set_index("period")

        if interval == "daily":
            # Get date vector without missing dates
            full_datevector = [
                date.strftime("%Y-%m-%d")
                for date in pd.date_range(start=df.index[0][:7], end=df.index[-1])
            ]
            return df.reindex(full_datevector)

        return df

    @staticmethod
    def ecb_riskfreerates(interval: str) -> pd.DataFrame:
        """
        Get riskfree rates from ECB (Daily rates: EONIA, monthly or annual rates: EURIBOR 1M)

        Args:
            interval: The interval of risk free rates. Daily, monthly or annual.

        Returns:
            A pandas dataframe with the risk free rates in EUR.

        Raises:
            ValueError: If interval given is not supported.
            ConnectionError: If ECB API endpoint returns bad answer.
        """

        try:
            identifier = rf_identifier_map[interval]
        except KeyError:
            raise ValueError("Interval not supported.")

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

            if interval == "daily":
                for obs in root_list:
                    date = obs[0].attrib["value"]
                    value = np.float64(
                        round(float(obs[1].attrib["value"]) / 100 / 360, 8)
                    )
                    tuple_list.append((date, value))
            elif interval == "monthly":
                for obs in root_list:
                    date = obs[0].attrib["value"]
                    value = np.float64(round(float(obs[1].attrib["value"]) / 100 / 12, 8))
                    tuple_list.append((date, value))
            elif interval == "annual":
                for obs in root_list:
                    # Look for december rates
                    if re.match(r"\s*\d{4}-12\s*", obs[0].attrib["value"]):
                        date = obs[0].attrib["value"][:-3]
                        value = np.float64(round(float(obs[1].attrib["value"]) / 100, 8))
                        tuple_list.append((date, value))

        df = pd.DataFrame(tuple_list, columns=["period", "rf"]).set_index("period")

        if interval == "daily":
            # Get date vector without missing dates
            full_datevector = [
                date.strftime("%Y-%m-%d")
                for date in pd.date_range(start=df.index[0][:4], end=df.index[-1])
            ]
            return df.reindex(full_datevector)

        return df

    @staticmethod
    def boe_fxrates(interval: str) -> pd.DataFrame:
        """
        Get 16.00 London time exchange rates against USD from Bank of England API.

        Args:
            interval: The interval of exchange rates. Daily, monthly or annual.

        Returns:
            A Pandas dataframe with the exchange rates.

        Raises:
            ConnectionError: If Bank of England API returns bad answer.
        """

        df = pd.DataFrame()

        for key in currency_identifier_map:
            request_string = "http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?CodeVer=new&xml.x=yes"
            params = {
                "Datefrom": "01/Jan/1963",
                "Dateto": "now",
                "SeriesCodes": currency_identifier_map[key][interval],
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

            if interval == "daily":
                for cube in root_list:
                    date = cube.attrib["TIME"]
                    value = np.float64(round(1 / float(cube.attrib["OBS_VALUE"]), 8))
                    tuple_list.append((date, value))
            elif interval == "monthly":
                for cube in root_list:
                    date = cube.attrib["TIME"][:-3]
                    value = np.float64(round(1 / float(cube.attrib["OBS_VALUE"]), 8))
                    tuple_list.append((date, value))
            elif interval == "annual":
                for cube in root_list:
                    date = cube.attrib["TIME"][:-6]
                    value = np.float64(round(1 / float(cube.attrib["OBS_VALUE"]), 8))
                    tuple_list.append((date, value))

            if df.empty:
                df = pd.DataFrame(tuple_list, columns=["period", key]).set_index("period")
            else:
                df = df.join(
                    pd.DataFrame(tuple_list, columns=["period", key]).set_index("period")
                )

        if interval == "daily":
            # Get date vector without missing dates
            full_datevector = [
                date.strftime("%Y-%m-%d")
                for date in pd.date_range(start=df.index[0][:4], end=df.index[-1])
            ]
            return df.reindex(full_datevector)

        return df
