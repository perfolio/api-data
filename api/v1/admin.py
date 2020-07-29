from django.contrib import admin
from django import forms
from .models import ExchangeRateUSDPerX, ECBRiskFreeRate, ThreeFactor, FiveFactor

class ExchangeRateUSDPerXAdminForm(forms.ModelForm):

    class Meta:
        model = ExchangeRateUSDPerX
        fields = '__all__'


class ExchangeRateUSDPerXAdmin(admin.ModelAdmin):
    form = ExchangeRateUSDPerXAdminForm
    list_display = ['created', 'last_updated', 'interval', 'EUR', 'JPY', 'GBP', 'CHF', 'RUB', 'AUD', 'BRL', 'CAD', 'CNY', 'INR']
    readonly_fields = ['created', 'last_updated', 'interval', 'EUR', 'JPY', 'GBP', 'CHF', 'RUB', 'AUD', 'BRL', 'CAD', 'CNY', 'INR']

admin.site.register(ExchangeRateUSDPerX, ExchangeRateUSDPerXAdmin)


class ECBRiskFreeRateAdminForm(forms.ModelForm):

    class Meta:
        model = ECBRiskFreeRate
        fields = '__all__'


class ECBRiskFreeRateAdmin(admin.ModelAdmin):
    form = ECBRiskFreeRateAdminForm
    list_display = ['created', 'last_updated', 'interval', 'RF']
    readonly_fields = ['created', 'last_updated', 'interval', 'RF']

admin.site.register(ECBRiskFreeRate, ECBRiskFreeRateAdmin)


class ThreeFactorAdminForm(forms.ModelForm):

    class Meta:
        model = ThreeFactor
        fields = '__all__'


class ThreeFactorAdmin(admin.ModelAdmin):
    form = ThreeFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RF']
    readonly_fields = ['created', 'last_updated']

admin.site.register(ThreeFactor, ThreeFactorAdmin)


class FiveFactorAdminForm(forms.ModelForm):

    class Meta:
        model = FiveFactor
        fields = '__all__'


class FiveFactorAdmin(admin.ModelAdmin):
    form = FiveFactorAdminForm
    list_display = ['created', 'last_updated', 'RMW', 'CMA']
    readonly_fields = ['created', 'last_updated', 'RMW', 'CMA']

admin.site.register(FiveFactor, FiveFactorAdmin)

