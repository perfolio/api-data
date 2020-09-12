import csv
import io
import zipfile
from typing import Optional
from unittest import mock

import numpy as np
import pandas as pd
from django.test import TestCase

from get_data.fetch import Fetcher as fe


class FileFactory:
    """
    Offers methods to create files for testing purposes.
    """

    @staticmethod
    def get_test_csvfile(csv_name: str) -> bytes:
        """
        Imitate a csv file from Kenneth French's data library.

        Args:
            csv_name: The name for the csv file to create.

        Returns:
            A bytes object for io stream input.
        """
        csv_file = io.StringIO()
        zipped_file = io.BytesIO()

        writer = csv.writer(csv_file)
        writer.writerow(["Jane Doe", "John Doe"])
        writer.writerow(["", "Mkt-RF", "SMB", "HML", "RF"])
        writer.writerow(["200403   ", "-0.05    ", "2.38", "9.33   ", "0.01"])
        writer.writerow(["200912   ", "5.05    ", "-2.38", "0.01   ", "0.05"])
        writer.writerow(["Jane Doe", "John Doe"])
        writer.writerow(["", "Mkt-RF", "SMB", "HML", "RF"])
        writer.writerow(["1999   ", "-19.50    ", "2.38", "-40.21   ", "7.90"])
        writer.writerow(["Jane Doe", "John Doe"])
        csv_file.seek(0)

        with zipfile.ZipFile(zipped_file, "w") as file:
            file.writestr(csv_name, csv_file.read())

        zipped_file.seek(0)
        return zipped_file.read()

    @staticmethod
    def get_test_xmlfile(provider: str) -> bytes:
        """
        Imitate XML files.

        Args:
            provider: The provider for which the file should be imitated.

        Returns:
            A bytes object for io stream input.

        Raises:
            NotImplementedError: If provider is unknown.
        """
        if provider == "ecb":
            file = io.BytesIO(
                b"""<?xml version="1.0" encoding="UTF-8"?>
                    <message:GenericData xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message" xmlns:generic="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic">
                    <message:DataSet>
                    <generic:Series>
                    <generic:Obs>
                    <generic:ObsDimension value="1994-12"/>
                    <generic:ObsValue value="6.00"/>
                    </generic:Obs>
                    </generic:Series>
                    </message:DataSet>
                    </message:GenericData>"""
            )
        elif provider == "boe":
            file = io.BytesIO(
                b"""<Envelope xmlns="http://www.gesmes.org/xml/2002-08-01">
                    <Cube xmlns="http://www.bankofengland.co.uk/boeapps/iadb/agg_series">
                    <Cube TIME="2013-11-29" OBS_VALUE="0.7344" OBS_CONF="N" LAST_UPDATED="2013-12-02 14:32:42"> </Cube>
                    <Cube TIME="2013-12-01" OBS_VALUE="0.7263" OBS_CONF="N" LAST_UPDATED="2014-01-02 15:42:39"> </Cube>
                    </Cube>
                    </Envelope>"""
            )
        else:
            raise NotImplementedError("Provider not supported.")

        return file.read()


def mocked_requests_get(*args, **kwargs):
    """
    Mock of requests.get for endpoint calls.
    """

    class MockResponse:
        """
        Class for response objects.
        """

        def __init__(self, content: Optional[bytes], status_code: int) -> None:
            self.content = content
            self.status_code = status_code

    # Imitate all endpoints
    if (
        args[0]
        == "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Europe_3_Factors_CSV.zip"
    ):
        return MockResponse(FileFactory.get_test_csvfile("Europe_3_Factors.csv"), 200)
    elif (
        args[0]
        == "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/North_America_3_Factors_CSV.zip"
    ):
        return MockResponse(
            FileFactory.get_test_csvfile("North_America_3_Factors.csv"), 200
        )
    elif (
        args[0]
        == "https://sdw-wsrest.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR1MD_.HSTA"
    ):
        return MockResponse(FileFactory.get_test_xmlfile("ecb"), 200)
    elif (
        args[0]
        == "http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?CodeVer=new&xml.x=yes"
    ):
        return MockResponse(FileFactory.get_test_xmlfile("boe"), 200)
    else:
        return MockResponse(None, 404)


class FetchTests(TestCase):
    """
    Tests for fetch module.
    """

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_french_factors(self, mock_get) -> None:
        """
        It calls Kenneth French's data library and builds and returns a dataframe.
        """
        df_test_monthly = fe.french_factors("Europe_3_Factors_CSV", "monthly")
        df_test_annual = fe.french_factors("North_America_3_Factors_CSV", "annual")

        df_target_monthly = (
            pd.DataFrame(
                {
                    "period": ["2004-03", "2009-12"],
                    "mktrf": [-0.0005, 0.0505],
                    "smb": [0.0238, -0.0238],
                    "hml": [0.0933, 0.0001],
                    "rf": [0.0001, 0.0005],
                }
            )
            .set_index("period")
            .astype("float64")
        )

        df_target_annual = (
            pd.DataFrame(
                {
                    "period": ["1999"],
                    "mktrf": [-0.1950],
                    "smb": [0.0238],
                    "hml": [-0.4021],
                    "rf": [0.0790],
                }
            )
            .set_index("period")
            .astype("float64")
        )

        self.assertIn(
            mock.call(
                "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Europe_3_Factors_CSV.zip"
            ),
            mock_get.call_args_list,
        )

        self.assertIn(
            mock.call(
                "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/North_America_3_Factors_CSV.zip"
            ),
            mock_get.call_args_list,
        )

        self.assertTrue(df_test_monthly.equals(df_target_monthly))
        self.assertTrue(df_test_annual.equals(df_target_annual))

        self.assertRaises(
            ConnectionError,
            fe.french_factors,
            "nothing_CSV",
            "monthly",
        )

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_ecb_riskfreerates(self, mock_get) -> None:
        """
        It calls the ECB API and builds and returns a dataframe.
        """
        df_test_monthly = fe.ecb_riskfreerates("monthly")
        df_test_annual = fe.ecb_riskfreerates("annual")

        df_target_monthly = (
            pd.DataFrame(
                {
                    "period": ["1994-12"],
                    "rf": [0.005],
                }
            )
            .set_index("period")
            .astype("float64")
        )

        df_target_annual = (
            pd.DataFrame(
                {
                    "period": ["1994"],
                    "rf": [0.06],
                }
            )
            .set_index("period")
            .astype("float64")
        )

        self.assertIn(
            mock.call(
                "https://sdw-wsrest.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR1MD_.HSTA"
            ),
            mock_get.call_args_list,
        )

        self.assertTrue(df_test_monthly.equals(df_target_monthly))
        self.assertTrue(df_test_annual.equals(df_target_annual))

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_boe_fxrates(self, mock_get) -> None:
        """
        It calls the BOE API and builds and returns a dataframe.
        """
        df_test_daily = fe.boe_fxrates("daily")

        # Calculate example fxrates
        fxrate1 = round(1 / 0.7344, 8)
        fxrate2 = round(1 / 0.7263, 8)

        df_target_daily = (
            pd.DataFrame(
                {
                    "period": ["2013-11-29", "2013-11-30", "2013-12-01"],
                    "EUR": [fxrate1, np.float64("NaN"), fxrate2],
                    "JPY": [fxrate1, np.float64("NaN"), fxrate2],
                    "GBP": [fxrate1, np.float64("NaN"), fxrate2],
                    "CHF": [fxrate1, np.float64("NaN"), fxrate2],
                    "RUB": [fxrate1, np.float64("NaN"), fxrate2],
                    "AUD": [fxrate1, np.float64("NaN"), fxrate2],
                    "BRL": [fxrate1, np.float64("NaN"), fxrate2],
                    "CAD": [fxrate1, np.float64("NaN"), fxrate2],
                    "CNY": [fxrate1, np.float64("NaN"), fxrate2],
                    "INR": [fxrate1, np.float64("NaN"), fxrate2],
                    "DKK": [fxrate1, np.float64("NaN"), fxrate2],
                    "NZD": [fxrate1, np.float64("NaN"), fxrate2],
                    "NOK": [fxrate1, np.float64("NaN"), fxrate2],
                    "SEK": [fxrate1, np.float64("NaN"), fxrate2],
                    "PLN": [fxrate1, np.float64("NaN"), fxrate2],
                    "ILS": [fxrate1, np.float64("NaN"), fxrate2],
                    "KRW": [fxrate1, np.float64("NaN"), fxrate2],
                    "TRY": [fxrate1, np.float64("NaN"), fxrate2],
                }
            )
            .set_index("period")
            .astype("float64")
        )

        self.assertIn(
            mock.call(
                "http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?CodeVer=new&xml.x=yes",
                params={
                    "Datefrom": "01/Jan/1963",
                    "Dateto": "now",
                    "SeriesCodes": "XUDLERD",
                },
            ),
            mock_get.call_args_list,
        )

        # Compare test (only last three rows for simplicity) and target dataframes
        self.assertTrue(df_test_daily.iloc[-3:, :].equals(df_target_daily))
