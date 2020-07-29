from django import forms
from .models import ExchangeRateUSDPerX, ECBRiskFreeRate, ThreeFactor, FiveFactor


class ExchangeRateUSDPerXForm(forms.ModelForm):
    class Meta:
        model = ExchangeRateUSDPerX
        fields = ['interval', 'EUR', 'JPY', 'GBP', 'CHF', 'RUB', 'AUD', 'BRL', 'CAD', 'CNY', 'INR']


class ECBRiskFreeRateForm(forms.ModelForm):
    class Meta:
        model = ECBRiskFreeRate
        fields = ['interval', 'RF']


class ThreeFactorForm(forms.ModelForm):
    class Meta:
        model = ThreeFactor
        fields = ['interval', 'MktRF', 'SMB', 'HML', 'RF']


class FiveFactorForm(forms.ModelForm):
    class Meta:
        model = FiveFactor
        fields = ['RMW', 'CMA']

