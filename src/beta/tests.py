import json

import pandas as pd
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.settings import REST_FRAMEWORK
from beta import api, models
from get_data.config.general import (
    currencies_fxrates,
    currencies_rf,
    factors,
    intervals,
    regions,
)


class APIRouteTestsAnon(APITestCase):
    """
    Tests for API routes and rate limit as an anonymous user.
    """

    def test_routes(self):
        """
        It returns http 200 for some valid routes.
        """
        # Mock throttle
        api.FiveFactorView.throttle_classes = ()
        api.ExchangeRateUSDPerXView.throttle_classes = ()

        # fxrate
        url = reverse(
            "fxrate",
            kwargs={
                "currency": "ils",
                "interval": "annual",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 5factor
        url = reverse(
            "5factor",
            kwargs={
                "factor": "all",
                "region": "japan",
                "currency": "ils",
                "interval": "annual",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_route(self):
        """
        It returns http 400 for invalid URL paths.
        """
        api.InvalidUrlPath.throttle_classes = ()

        url = reverse(
            "fxrate",
            kwargs={
                "currency": "nzd",
                "interval": "daily",
            },
        )
        response = self.client.get(url[:9])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_limit(self):
        """
        It returns http 429 with proper message after hitting rate limit
        """
        # Parse throttle rate from settings dynamically, no need to change manually
        rate_limit = int(REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["anon"].rsplit("/")[0])  # type: ignore

        for i in range(0, rate_limit):
            url = reverse(
                "rf",
                kwargs={"currency": "EUR", "interval": "m"},
            )
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Next http get should return http 429
        url = reverse(
            "3factor",
            kwargs={
                "factor": "SMB",
                "region": "Developed",
                "currency": "USD",
                "interval": "daily",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertTrue("Error" in json.loads(response.content).keys())


class APIRouteTestsUser(APITestCase):
    """
    Tests for API routes providing a valid token
    """

    def setUp(self):
        """
        Create a user and a token and mock rate limit for exhaustive testing.
        """
        self.user = User.objects.create(username="testuser")
        self.token = Token.objects.create(user=self.user)
        api.RiskFreeRateView.throttle_classes = ()
        api.ThreeFactorView.throttle_classes = ()

    def test_routes_rf(self):
        """
        It returns http 200 for all valid rf routes.
        """
        test_currencies = currencies_rf + ["eur", "EuR", "usd", "USd"]
        test_intervals = intervals + ["d", "m", "a"]

        for currency in test_currencies:
            for interval in test_intervals:
                url = reverse(
                    "rf",
                    kwargs={"currency": currency, "interval": interval},
                )
                response = self.client.get(url, {"token": self.token})
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routes_fxrate(self):
        """
        It returns http 200 for all valid fxrate routes.
        """
        test_currencies = currencies_fxrates + [
            "eur",
            "EuR",
            "cad",
            "CaD",
            "ILs",
            "iLS",
        ]
        test_intervals = intervals + ["d", "m", "a"]

        for currency in test_currencies:
            for interval in test_intervals:
                url = reverse(
                    "fxrate", kwargs={"currency": currency, "interval": interval}
                )
                response = self.client.get(url, {"token": self.token})
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routes_3factor(self):
        """
        It returns http 200 for all valid 3 factor model routes.
        """
        test_currencies = currencies_fxrates
        test_intervals = intervals
        test_factors = factors[:-3]
        test_regions = regions

        for factor in test_factors:
            for region in test_regions:
                for currency in test_currencies:
                    for interval in test_intervals:
                        url = reverse(
                            "3factor",
                            kwargs={
                                "factor": factor,
                                "region": region,
                                "currency": currency,
                                "interval": interval,
                            },
                        )
                        response = self.client.get(
                            url,
                            {
                                "token": self.token,
                                "from": "2019-12-31",
                                "to": "2020-03-31",
                            },
                        )
                        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routes_4factor(self):
        """
        It returns http 200 for some valid 4 factor model routes.
        """
        test_currency = "SEK"
        test_interval = "m"
        test_factors = factors[:-4]
        test_regions = regions[:3]

        for factor in test_factors:
            for region in test_regions:
                url = reverse(
                    "4factor",
                    kwargs={
                        "factor": factor,
                        "region": region,
                        "currency": test_currency,
                        "interval": test_interval,
                    },
                )
                response = self.client.get(
                    url,
                    {
                        "token": self.token,
                        "from": "1999-12",
                        "to": "2005-08",
                    },
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routes_5factor(self):
        """
        It returns http 200 for a valid 5 factor model route.
        """
        test_currency = "nzd"
        test_interval = "a"
        test_factor = "all"
        test_region = "Emerging"

        url = reverse(
            "5factor",
            kwargs={
                "factor": test_factor,
                "region": test_region,
                "currency": test_currency,
                "interval": test_interval,
            },
        )
        response = self.client.get(
            url,
            {
                "token": self.token,
                "dropna": "False",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routes_6factor(self):
        """
        It returns http 200 for a valid 6 factor model route.
        """
        test_currency = "GbP"
        test_interval = "daily"
        test_factor = "all"
        test_region = "developed_EX_Us"

        url = reverse(
            "6factor",
            kwargs={
                "factor": test_factor,
                "region": test_region,
                "currency": test_currency,
                "interval": test_interval,
            },
        )
        response = self.client.get(
            url,
            {
                "token": self.token,
                "dropna": "true",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ModelFieldsTests(APITestCase):
    """
    Tests for ORM models and their methods.
    """

    def test_rf_model(self):
        """
        It creates an instance and updates it via dataframe import.
        """
        self.rf = models.RiskFreeRate(
            period="2018-12-29", interval="daily", currency="EUR", rf=0.00001
        )
        self.rf.save()

        df_test = pd.DataFrame({"rf": 0.00002}, index=["2018-12-29"])
        models.RiskFreeRate.from_dataframe(df_test, "daily", "EUR")

        self.assertTrue(
            models.RiskFreeRate.objects.get(
                period="2018-12-29", interval="daily", currency="EUR"
            )
            == models.RiskFreeRate(
                period="2018-12-29", interval="daily", currency="EUR", rf=0.00002
            ),
        )

    def test_fxrate_model(self):
        """
        It creates an instance via dataframe import and updates it.
        """
        fxrates = {
            "EUR": 1.1013,
            "JPY": 0.0133,
            "GBP": 1.2456,
            "CHF": 1.0112,
            "RUB": 10.4563,
            "AUD": 1.0934,
            "BRL": 5.3243,
            "CAD": 2.3476,
            "CNY": 19.6743,
            "INR": 30.5792,
            "DKK": 0.1459,
            "NZD": 0.4623,
            "NOK": 0.0924,
            "SEK": 0.1385,
            "PLN": 0.1945,
            "ILS": 1.5632,
            "KRW": 0.0024,
            "TRY": 0.0012,
        }

        df_test = pd.DataFrame(fxrates, index=["2017-09"])
        models.ExchangeRateUSDPerX.from_dataframe(df_test, "monthly")

        self.fxrate = models.ExchangeRateUSDPerX.objects.get(
            period="2017-09", interval="monthly"
        )
        self.fxrate.EUR = 1.1337
        self.fxrate.save()

        fxrates["EUR"] = 1.1337
        self.assertTrue(
            models.ExchangeRateUSDPerX.objects.get(period="2017-09", interval="monthly")
            == models.ExchangeRateUSDPerX(
                period="2017-09", interval="monthly", **fxrates
            ),
        )

    def test_threefourfactor_model(self):
        """
        It creates an instance via dataframe import.
        """

        factors = {"mktrf": 30.4563, "smb": 10.7765, "hml": 17.1337, "mom": 23.4545}
        df_test = pd.DataFrame(factors, index=["2019"])
        models.ThreeFourFactor.from_dataframe(df_test, "annual", "EUR", "developed")

        self.threefourfactor = models.ThreeFourFactor(
            period="2018",
            interval="annual",
            region="developed",
            currency="EUR",
            **factors,
        )
        self.threefourfactor.save()

        self.assertFalse(
            self.threefourfactor
            == models.ThreeFourFactor.objects.get(
                period="2019", interval="annual", region="developed", currency="EUR"
            )
        )

    def test_fivesixfactor_model(self):
        """
        It creates an instance and updates it via dataframe import.
        """

        factors = {
            "mktrf": 30.4563,
            "smb": 10.7765,
            "hml": 17.1337,
            "rmw": 4.2514,
            "cma": 2.0931,
            "mom": 23.4545,
        }
        self.fivesixfactor = models.FiveSixFactor(
            period="2015",
            interval="annual",
            region="japan",
            currency="JPY",
            **factors,
        )
        self.fivesixfactor.save()

        factors["rmw"] = 4.5214
        df_test = pd.DataFrame(factors, index=["2015"])
        models.FiveSixFactor.from_dataframe(df_test, "annual", "JPY", "japan")

        self.assertTrue(
            models.FiveSixFactor.objects.get(
                period="2015", interval="annual", region="japan", currency="JPY"
            )
            == models.FiveSixFactor(
                period="2015",
                interval="annual",
                region="japan",
                currency="JPY",
                **factors,
            )
        )
