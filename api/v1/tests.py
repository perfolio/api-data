import unittest

from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from django.urls import reverse

from .models import (
    AnnuallyECBRiskFreeRate,
    AnnuallyExchangeRateUSDPerX,
    AnnuallyFiveFactor,
    DailyECBRiskFreeRate,
    DailyExchangeRateUSDPerX,
    DailyFiveFactor,
    DailyThreeFactor,
    MonthlyECBRiskFreeRate,
    MonthlyExchangeRateUSDPerX,
    MonthlyFiveFactor,
    MonthlyThreeFactor,
    YearlyThreeFactor,
)


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_dailyecbriskfreerate(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["RF"] = "RF"
    defaults.update(**kwargs)
    return DailyECBRiskFreeRate.objects.create(**defaults)


def create_monthlyecbriskfreerate(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["RF"] = "RF"
    defaults.update(**kwargs)
    return MonthlyECBRiskFreeRate.objects.create(**defaults)


def create_annuallyecbriskfreerate(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["RF"] = "RF"
    defaults.update(**kwargs)
    return AnnuallyECBRiskFreeRate.objects.create(**defaults)


def create_dailyexchangerateusdperx(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["EUR"] = "EUR"
    defaults["JPY"] = "JPY"
    defaults["GBP"] = "GBP"
    defaults["CHF"] = "CHF"
    defaults["RUB"] = "RUB"
    defaults["AUD"] = "AUD"
    defaults["BRL"] = "BRL"
    defaults["CAD"] = "CAD"
    defaults["CNY"] = "CNY"
    defaults["INR"] = "INR"
    defaults.update(**kwargs)
    return DailyExchangeRateUSDPerX.objects.create(**defaults)


def create_monthlyexchangerateusdperx(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["EUR"] = "EUR"
    defaults["JPY"] = "JPY"
    defaults["GBP"] = "GBP"
    defaults["CHF"] = "CHF"
    defaults["RUB"] = "RUB"
    defaults["AUD"] = "AUD"
    defaults["BRL"] = "BRL"
    defaults["CAD"] = "CAD"
    defaults["CNY"] = "CNY"
    defaults["INR"] = "INR"
    defaults.update(**kwargs)
    return MonthlyExchangeRateUSDPerX.objects.create(**defaults)


def create_annuallyexchangerateusdperx(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["EUR"] = "EUR"
    defaults["JPY"] = "JPY"
    defaults["GBP"] = "GBP"
    defaults["CHF"] = "CHF"
    defaults["RUB"] = "RUB"
    defaults["AUD"] = "AUD"
    defaults["BRL"] = "BRL"
    defaults["CAD"] = "CAD"
    defaults["CNY"] = "CNY"
    defaults["INR"] = "INR"
    defaults.update(**kwargs)
    return AnnuallyExchangeRateUSDPerX.objects.create(**defaults)


def create_dailythreefactor(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["MktRF"] = "MktRF"
    defaults["SMB"] = "SMB"
    defaults["HML"] = "HML"
    defaults["RF"] = "RF"
    defaults.update(**kwargs)
    return DailyThreeFactor.objects.create(**defaults)


def create_monthlythreefactor(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["MktRF"] = "MktRF"
    defaults["SMB"] = "SMB"
    defaults["HML"] = "HML"
    defaults["RF"] = "RF"
    defaults.update(**kwargs)
    return MonthlyThreeFactor.objects.create(**defaults)


def create_yearlythreefactor(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["MktRF"] = "MktRF"
    defaults["SMB"] = "SMB"
    defaults["HML"] = "HML"
    defaults["RF"] = "RF"
    defaults.update(**kwargs)
    return YearlyThreeFactor.objects.create(**defaults)


def create_dailyfivefactor(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["MktRF"] = "MktRF"
    defaults["SMB"] = "SMB"
    defaults["HML"] = "HML"
    defaults["RF"] = "RF"
    defaults["RMW"] = "RMW"
    defaults["CMA"] = "CMA"
    defaults.update(**kwargs)
    return DailyFiveFactor.objects.create(**defaults)


def create_monthlyfivefactor(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["MktRF"] = "MktRF"
    defaults["SMB"] = "SMB"
    defaults["HML"] = "HML"
    defaults["RF"] = "RF"
    defaults["RMW"] = "RMW"
    defaults["CMA"] = "CMA"
    defaults.update(**kwargs)
    return MonthlyFiveFactor.objects.create(**defaults)


def create_annuallyfivefactor(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["MktRF"] = "MktRF"
    defaults["SMB"] = "SMB"
    defaults["HML"] = "HML"
    defaults["RF"] = "RF"
    defaults["RMW"] = "RMW"
    defaults["CMA"] = "CMA"
    defaults.update(**kwargs)
    return AnnuallyFiveFactor.objects.create(**defaults)


class DailyECBRiskFreeRateViewTest(unittest.TestCase):
    """
    Tests for DailyECBRiskFreeRate
    """

    def setUp(self):
        self.client = Client()

    def test_list_dailyecbriskfreerate(self):
        url = reverse("v1_dailyecbriskfreerate_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_dailyecbriskfreerate(self):
        url = reverse("v1_dailyecbriskfreerate_create")
        data = {
            "interval": "interval",
            "RF": "RF",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_dailyecbriskfreerate(self):
        dailyecbriskfreerate = create_dailyecbriskfreerate()
        url = reverse(
            "v1_dailyecbriskfreerate_detail", args=[dailyecbriskfreerate.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_dailyecbriskfreerate(self):
        dailyecbriskfreerate = create_dailyecbriskfreerate()
        data = {
            "interval": "interval",
            "RF": "RF",
        }
        url = reverse(
            "v1_dailyecbriskfreerate_update", args=[dailyecbriskfreerate.pk]
        )
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class MonthlyECBRiskFreeRateViewTest(unittest.TestCase):
    """
    Tests for MonthlyECBRiskFreeRate
    """

    def setUp(self):
        self.client = Client()

    def test_list_monthlyecbriskfreerate(self):
        url = reverse("v1_monthlyecbriskfreerate_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_monthlyecbriskfreerate(self):
        url = reverse("v1_monthlyecbriskfreerate_create")
        data = {
            "interval": "interval",
            "RF": "RF",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_monthlyecbriskfreerate(self):
        monthlyecbriskfreerate = create_monthlyecbriskfreerate()
        url = reverse(
            "v1_monthlyecbriskfreerate_detail",
            args=[monthlyecbriskfreerate.pk],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_monthlyecbriskfreerate(self):
        monthlyecbriskfreerate = create_monthlyecbriskfreerate()
        data = {
            "interval": "interval",
            "RF": "RF",
        }
        url = reverse(
            "v1_monthlyecbriskfreerate_update",
            args=[monthlyecbriskfreerate.pk],
        )
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class AnnuallyECBRiskFreeRateViewTest(unittest.TestCase):
    """
    Tests for AnnuallyECBRiskFreeRate
    """

    def setUp(self):
        self.client = Client()

    def test_list_annuallyecbriskfreerate(self):
        url = reverse("v1_annuallyecbriskfreerate_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_annuallyecbriskfreerate(self):
        url = reverse("v1_annuallyecbriskfreerate_create")
        data = {
            "interval": "interval",
            "RF": "RF",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_annuallyecbriskfreerate(self):
        annuallyecbriskfreerate = create_annuallyecbriskfreerate()
        url = reverse(
            "v1_annuallyecbriskfreerate_detail",
            args=[annuallyecbriskfreerate.pk],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_annuallyecbriskfreerate(self):
        annuallyecbriskfreerate = create_annuallyecbriskfreerate()
        data = {
            "interval": "interval",
            "RF": "RF",
        }
        url = reverse(
            "v1_annuallyecbriskfreerate_update",
            args=[annuallyecbriskfreerate.pk],
        )
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class DailyExchangeRateUSDPerXViewTest(unittest.TestCase):
    """
    Tests for DailyExchangeRateUSDPerX
    """

    def setUp(self):
        self.client = Client()

    def test_list_dailyexchangerateusdperx(self):
        url = reverse("v1_dailyexchangerateusdperx_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_dailyexchangerateusdperx(self):
        url = reverse("v1_dailyexchangerateusdperx_create")
        data = {
            "interval": "interval",
            "EUR": "EUR",
            "JPY": "JPY",
            "GBP": "GBP",
            "CHF": "CHF",
            "RUB": "RUB",
            "AUD": "AUD",
            "BRL": "BRL",
            "CAD": "CAD",
            "CNY": "CNY",
            "INR": "INR",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_dailyexchangerateusdperx(self):
        dailyexchangerateusdperx = create_dailyexchangerateusdperx()
        url = reverse(
            "v1_dailyexchangerateusdperx_detail",
            args=[dailyexchangerateusdperx.pk],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_dailyexchangerateusdperx(self):
        dailyexchangerateusdperx = create_dailyexchangerateusdperx()
        data = {
            "interval": "interval",
            "EUR": "EUR",
            "JPY": "JPY",
            "GBP": "GBP",
            "CHF": "CHF",
            "RUB": "RUB",
            "AUD": "AUD",
            "BRL": "BRL",
            "CAD": "CAD",
            "CNY": "CNY",
            "INR": "INR",
        }
        url = reverse(
            "v1_dailyexchangerateusdperx_update",
            args=[dailyexchangerateusdperx.pk],
        )
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class MonthlyExchangeRateUSDPerXViewTest(unittest.TestCase):
    """
    Tests for MonthlyExchangeRateUSDPerX
    """

    def setUp(self):
        self.client = Client()

    def test_list_monthlyexchangerateusdperx(self):
        url = reverse("v1_monthlyexchangerateusdperx_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_monthlyexchangerateusdperx(self):
        url = reverse("v1_monthlyexchangerateusdperx_create")
        data = {
            "interval": "interval",
            "EUR": "EUR",
            "JPY": "JPY",
            "GBP": "GBP",
            "CHF": "CHF",
            "RUB": "RUB",
            "AUD": "AUD",
            "BRL": "BRL",
            "CAD": "CAD",
            "CNY": "CNY",
            "INR": "INR",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_monthlyexchangerateusdperx(self):
        monthlyexchangerateusdperx = create_monthlyexchangerateusdperx()
        url = reverse(
            "v1_monthlyexchangerateusdperx_detail",
            args=[monthlyexchangerateusdperx.pk],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_monthlyexchangerateusdperx(self):
        monthlyexchangerateusdperx = create_monthlyexchangerateusdperx()
        data = {
            "interval": "interval",
            "EUR": "EUR",
            "JPY": "JPY",
            "GBP": "GBP",
            "CHF": "CHF",
            "RUB": "RUB",
            "AUD": "AUD",
            "BRL": "BRL",
            "CAD": "CAD",
            "CNY": "CNY",
            "INR": "INR",
        }
        url = reverse(
            "v1_monthlyexchangerateusdperx_update",
            args=[monthlyexchangerateusdperx.pk],
        )
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class AnnuallyExchangeRateUSDPerXViewTest(unittest.TestCase):
    """
    Tests for AnnuallyExchangeRateUSDPerX
    """

    def setUp(self):
        self.client = Client()

    def test_list_annuallyexchangerateusdperx(self):
        url = reverse("v1_annuallyexchangerateusdperx_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_annuallyexchangerateusdperx(self):
        url = reverse("v1_annuallyexchangerateusdperx_create")
        data = {
            "interval": "interval",
            "EUR": "EUR",
            "JPY": "JPY",
            "GBP": "GBP",
            "CHF": "CHF",
            "RUB": "RUB",
            "AUD": "AUD",
            "BRL": "BRL",
            "CAD": "CAD",
            "CNY": "CNY",
            "INR": "INR",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_annuallyexchangerateusdperx(self):
        annuallyexchangerateusdperx = create_annuallyexchangerateusdperx()
        url = reverse(
            "v1_annuallyexchangerateusdperx_detail",
            args=[annuallyexchangerateusdperx.pk],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_annuallyexchangerateusdperx(self):
        annuallyexchangerateusdperx = create_annuallyexchangerateusdperx()
        data = {
            "interval": "interval",
            "EUR": "EUR",
            "JPY": "JPY",
            "GBP": "GBP",
            "CHF": "CHF",
            "RUB": "RUB",
            "AUD": "AUD",
            "BRL": "BRL",
            "CAD": "CAD",
            "CNY": "CNY",
            "INR": "INR",
        }
        url = reverse(
            "v1_annuallyexchangerateusdperx_update",
            args=[annuallyexchangerateusdperx.pk],
        )
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class DailyThreeFactorViewTest(unittest.TestCase):
    """
    Tests for DailyThreeFactor
    """

    def setUp(self):
        self.client = Client()

    def test_list_dailythreefactor(self):
        url = reverse("v1_dailythreefactor_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_dailythreefactor(self):
        url = reverse("v1_dailythreefactor_create")
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_dailythreefactor(self):
        dailythreefactor = create_dailythreefactor()
        url = reverse("v1_dailythreefactor_detail", args=[dailythreefactor.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_dailythreefactor(self):
        dailythreefactor = create_dailythreefactor()
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
        }
        url = reverse("v1_dailythreefactor_update", args=[dailythreefactor.pk])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class MonthlyThreeFactorViewTest(unittest.TestCase):
    """
    Tests for MonthlyThreeFactor
    """

    def setUp(self):
        self.client = Client()

    def test_list_monthlythreefactor(self):
        url = reverse("v1_monthlythreefactor_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_monthlythreefactor(self):
        url = reverse("v1_monthlythreefactor_create")
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_monthlythreefactor(self):
        monthlythreefactor = create_monthlythreefactor()
        url = reverse(
            "v1_monthlythreefactor_detail", args=[monthlythreefactor.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_monthlythreefactor(self):
        monthlythreefactor = create_monthlythreefactor()
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
        }
        url = reverse(
            "v1_monthlythreefactor_update", args=[monthlythreefactor.pk]
        )
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class YearlyThreeFactorViewTest(unittest.TestCase):
    """
    Tests for YearlyThreeFactor
    """

    def setUp(self):
        self.client = Client()

    def test_list_yearlythreefactor(self):
        url = reverse("v1_yearlythreefactor_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_yearlythreefactor(self):
        url = reverse("v1_yearlythreefactor_create")
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_yearlythreefactor(self):
        yearlythreefactor = create_yearlythreefactor()
        url = reverse(
            "v1_yearlythreefactor_detail", args=[yearlythreefactor.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_yearlythreefactor(self):
        yearlythreefactor = create_yearlythreefactor()
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
        }
        url = reverse(
            "v1_yearlythreefactor_update", args=[yearlythreefactor.pk]
        )
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class DailyFiveFactorViewTest(unittest.TestCase):
    """
    Tests for DailyFiveFactor
    """

    def setUp(self):
        self.client = Client()

    def test_list_dailyfivefactor(self):
        url = reverse("v1_dailyfivefactor_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_dailyfivefactor(self):
        url = reverse("v1_dailyfivefactor_create")
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
            "RMW": "RMW",
            "CMA": "CMA",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_dailyfivefactor(self):
        dailyfivefactor = create_dailyfivefactor()
        url = reverse("v1_dailyfivefactor_detail", args=[dailyfivefactor.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_dailyfivefactor(self):
        dailyfivefactor = create_dailyfivefactor()
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
            "RMW": "RMW",
            "CMA": "CMA",
        }
        url = reverse("v1_dailyfivefactor_update", args=[dailyfivefactor.pk])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class MonthlyFiveFactorViewTest(unittest.TestCase):
    """
    Tests for MonthlyFiveFactor
    """

    def setUp(self):
        self.client = Client()

    def test_list_monthlyfivefactor(self):
        url = reverse("v1_monthlyfivefactor_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_monthlyfivefactor(self):
        url = reverse("v1_monthlyfivefactor_create")
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
            "RMW": "RMW",
            "CMA": "CMA",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_monthlyfivefactor(self):
        monthlyfivefactor = create_monthlyfivefactor()
        url = reverse(
            "v1_monthlyfivefactor_detail", args=[monthlyfivefactor.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_monthlyfivefactor(self):
        monthlyfivefactor = create_monthlyfivefactor()
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
            "RMW": "RMW",
            "CMA": "CMA",
        }
        url = reverse(
            "v1_monthlyfivefactor_update", args=[monthlyfivefactor.pk]
        )
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class AnnuallyFiveFactorViewTest(unittest.TestCase):
    """
    Tests for AnnuallyFiveFactor
    """

    def setUp(self):
        self.client = Client()

    def test_list_annuallyfivefactor(self):
        url = reverse("v1_annuallyfivefactor_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_annuallyfivefactor(self):
        url = reverse("v1_annuallyfivefactor_create")
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
            "RMW": "RMW",
            "CMA": "CMA",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_annuallyfivefactor(self):
        annuallyfivefactor = create_annuallyfivefactor()
        url = reverse(
            "v1_annuallyfivefactor_detail", args=[annuallyfivefactor.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_annuallyfivefactor(self):
        annuallyfivefactor = create_annuallyfivefactor()
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
            "RMW": "RMW",
            "CMA": "CMA",
        }
        url = reverse(
            "v1_annuallyfivefactor_update", args=[annuallyfivefactor.pk]
        )
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
