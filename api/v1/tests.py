import unittest
from django.urls import reverse
from django.test import Client
from .models import ExchangeRateUSDPerX, ECBRiskFreeRate, ThreeFactor, FiveFactor
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


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


def create_exchangerateusdperx(**kwargs):
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
    return ExchangeRateUSDPerX.objects.create(**defaults)


def create_ecbriskfreerate(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["RF"] = "RF"
    defaults.update(**kwargs)
    return ECBRiskFreeRate.objects.create(**defaults)


def create_threefactor(**kwargs):
    defaults = {}
    defaults["interval"] = "interval"
    defaults["MktRF"] = "MktRF"
    defaults["SMB"] = "SMB"
    defaults["HML"] = "HML"
    defaults["RF"] = "RF"
    defaults.update(**kwargs)
    return ThreeFactor.objects.create(**defaults)


def create_fivefactor(**kwargs):
    defaults = {}
    defaults["RMW"] = "RMW"
    defaults["CMA"] = "CMA"
    defaults.update(**kwargs)
    return FiveFactor.objects.create(**defaults)


class ExchangeRateUSDPerXViewTest(unittest.TestCase):
    '''
    Tests for ExchangeRateUSDPerX
    '''
    def setUp(self):
        self.client = Client()

    def test_list_exchangerateusdperx(self):
        url = reverse('v1_exchangerateusdperx_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_exchangerateusdperx(self):
        url = reverse('v1_exchangerateusdperx_create')
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

    def test_detail_exchangerateusdperx(self):
        exchangerateusdperx = create_exchangerateusdperx()
        url = reverse('v1_exchangerateusdperx_detail', args=[exchangerateusdperx.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_exchangerateusdperx(self):
        exchangerateusdperx = create_exchangerateusdperx()
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
        url = reverse('v1_exchangerateusdperx_update', args=[exchangerateusdperx.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ECBRiskFreeRateViewTest(unittest.TestCase):
    '''
    Tests for ECBRiskFreeRate
    '''
    def setUp(self):
        self.client = Client()

    def test_list_ecbriskfreerate(self):
        url = reverse('v1_ecbriskfreerate_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_ecbriskfreerate(self):
        url = reverse('v1_ecbriskfreerate_create')
        data = {
            "interval": "interval",
            "RF": "RF",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_ecbriskfreerate(self):
        ecbriskfreerate = create_ecbriskfreerate()
        url = reverse('v1_ecbriskfreerate_detail', args=[ecbriskfreerate.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_ecbriskfreerate(self):
        ecbriskfreerate = create_ecbriskfreerate()
        data = {
            "interval": "interval",
            "RF": "RF",
        }
        url = reverse('v1_ecbriskfreerate_update', args=[ecbriskfreerate.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ThreeFactorViewTest(unittest.TestCase):
    '''
    Tests for ThreeFactor
    '''
    def setUp(self):
        self.client = Client()

    def test_list_threefactor(self):
        url = reverse('v1_threefactor_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_threefactor(self):
        url = reverse('v1_threefactor_create')
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_threefactor(self):
        threefactor = create_threefactor()
        url = reverse('v1_threefactor_detail', args=[threefactor.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_threefactor(self):
        threefactor = create_threefactor()
        data = {
            "interval": "interval",
            "MktRF": "MktRF",
            "SMB": "SMB",
            "HML": "HML",
            "RF": "RF",
        }
        url = reverse('v1_threefactor_update', args=[threefactor.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class FiveFactorViewTest(unittest.TestCase):
    '''
    Tests for FiveFactor
    '''
    def setUp(self):
        self.client = Client()

    def test_list_fivefactor(self):
        url = reverse('v1_fivefactor_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_fivefactor(self):
        url = reverse('v1_fivefactor_create')
        data = {
            "RMW": "RMW",
            "CMA": "CMA",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_fivefactor(self):
        fivefactor = create_fivefactor()
        url = reverse('v1_fivefactor_detail', args=[fivefactor.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_fivefactor(self):
        fivefactor = create_fivefactor()
        data = {
            "RMW": "RMW",
            "CMA": "CMA",
        }
        url = reverse('v1_fivefactor_update', args=[fivefactor.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

