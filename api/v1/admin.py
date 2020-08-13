from django import forms
from django.contrib import admin

from .models import (
    AnnuallyExchangeRateUSDPerX,
    AnnuallyFiveSixFactor,
    AnnuallyRiskFreeRate,
    AnnuallyThreeFourFactor,
    DailyExchangeRateUSDPerX,
    DailyFiveSixFactor,
    DailyRiskFreeRate,
    DailyThreeFourFactor,
    MonthlyExchangeRateUSDPerX,
    MonthlyFiveSixFactor,
    MonthlyRiskFreeRate,
    MonthlyThreeFourFactor,
)

"""
class DailyRiskFreeRateAdminForm(forms.ModelForm):

    class Meta:
        model = DailyRiskFreeRate
        fields = '__all__'


class DailyRiskFreeRateAdmin(admin.ModelAdmin):
    form = DailyRiskFreeRateAdminForm
    list_display = ['created', 'last_updated', 'interval', 'RF']
    readonly_fields = ['created', 'last_updated']
admin.site.register(DailyRiskFreeRate, DailyRiskFreeRateAdmin)


class MonthlyRiskFreeRateAdminForm(forms.ModelForm):

    class Meta:
        model = MonthlyRiskFreeRate
        fields = '__all__'


class MonthlyRiskFreeRateAdmin(admin.ModelAdmin):
    form = MonthlyRiskFreeRateAdminForm
    list_display = ['created', 'last_updated', 'interval', 'RF']
    readonly_fields = ['created', 'last_updated']
admin.site.register(MonthlyRiskFreeRate, MonthlyRiskFreeRateAdmin)


class AnnuallyRiskFreeRateAdminForm(forms.ModelForm):

    class Meta:
        model = AnnuallyRiskFreeRate
        fields = '__all__'


class AnnuallyRiskFreeRateAdmin(admin.ModelAdmin):
    form = AnnuallyRiskFreeRateAdminForm
    list_display = ['created', 'last_updated', 'interval', 'RF']
    readonly_fields = ['created', 'last_updated']
admin.site.register(AnnuallyRiskFreeRate, AnnuallyRiskFreeRateAdmin)


class DailyExchangeRateUSDPerXAdminForm(forms.ModelForm):

    class Meta:
        model = DailyExchangeRateUSDPerX
        fields = '__all__'


class DailyExchangeRateUSDPerXAdmin(admin.ModelAdmin):
    form = DailyExchangeRateUSDPerXAdminForm
    list_display = ['created', 'last_updated', 'interval', 'EUR', 'JPY', 'GBP', 'CHF', 'RUB', 'AUD', 'BRL', 'CAD', 'CNY', 'INR']
    readonly_fields = ['created', 'last_updated']
admin.site.register(DailyExchangeRateUSDPerX, DailyExchangeRateUSDPerXAdmin)


class MonthlyExchangeRateUSDPerXAdminForm(forms.ModelForm):

    class Meta:
        model = MonthlyExchangeRateUSDPerX
        fields = '__all__'


class MonthlyExchangeRateUSDPerXAdmin(admin.ModelAdmin):
    form = MonthlyExchangeRateUSDPerXAdminForm
    list_display = ['created', 'last_updated', 'interval', 'EUR', 'JPY', 'GBP', 'CHF', 'RUB', 'AUD', 'BRL', 'CAD', 'CNY', 'INR']
    readonly_fields = ['created', 'last_updated']
admin.site.register(MonthlyExchangeRateUSDPerX, MonthlyExchangeRateUSDPerXAdmin)


class AnnuallyExchangeRateUSDPerXAdminForm(forms.ModelForm):

    class Meta:
        model = AnnuallyExchangeRateUSDPerX
        fields = '__all__'


class AnnuallyExchangeRateUSDPerXAdmin(admin.ModelAdmin):
    form = AnnuallyExchangeRateUSDPerXAdminForm
    list_display = ['created', 'last_updated', 'interval', 'EUR', 'JPY', 'GBP', 'CHF', 'RUB', 'AUD', 'BRL', 'CAD', 'CNY', 'INR']
    readonly_fields = ['created', 'last_updated']
admin.site.register(AnnuallyExchangeRateUSDPerX, AnnuallyExchangeRateUSDPerXAdmin)


class DailyThreeFourFactorAdminForm(forms.ModelForm):

    class Meta:
        model = DailyThreeFourFactor
        fields = '__all__'


class DailyThreeFourFactorAdmin(admin.ModelAdmin):
    form = DailyThreeFourFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RF']
    readonly_fields = ['created', 'last_updated']
admin.site.register(DailyThreeFourFactor, DailyThreeFourFactorAdmin)


class MonthlyThreeFourFactorAdminForm(forms.ModelForm):

    class Meta:
        model = MonthlyThreeFourFactor
        fields = '__all__'


class MonthlyThreeFourFactorAdmin(admin.ModelAdmin):
    form = MonthlyThreeFourFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RF']
    readonly_fields = ['created', 'last_updated']
admin.site.register(MonthlyThreeFourFactor, MonthlyThreeFourFactorAdmin)


class YearlyThreeFourFactorAdminForm(forms.ModelForm):

    class Meta:
        model = AnnuallyThreeFourFactor
        fields = '__all__'


class YearlyThreeFourFactorAdmin(admin.ModelAdmin):
    form = YearlyThreeFourFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RF']
    readonly_fields = ['created', 'last_updated']
admin.site.register(AnnuallyThreeFourFactor, YearlyThreeFourFactorAdmin)


class DailyFiveSixFactorAdminForm(forms.ModelForm):

    class Meta:
        model = DailyFiveSixFactor
        fields = '__all__'


class DailyFiveSixFactorAdmin(admin.ModelAdmin):
    form = DailyFiveSixFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RMW', 'CMA']
    readonly_fields = ['created', 'last_updated']
admin.site.register(DailyFiveSixFactor, DailyFiveSixFactorAdmin)


class MonthlyFiveSixFactorAdminForm(forms.ModelForm):

    class Meta:
        model = MonthlyFiveSixFactor
        fields = '__all__'


class MonthlyFiveSixFactorAdmin(admin.ModelAdmin):
    form = MonthlyFiveSixFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RMW', 'CMA']
    readonly_fields = ['created', 'last_updated']
admin.site.register(MonthlyFiveSixFactor, MonthlyFiveSixFactorAdmin)


class AnnuallyFiveSixFactorAdminForm(forms.ModelForm):

    class Meta:
        model = AnnuallyFiveSixFactor
        fields = '__all__'


class AnnuallyFiveSixFactorAdmin(admin.ModelAdmin):
    form = AnnuallyFiveSixFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RMW', 'CMA']
    readonly_fields = ['created', 'last_updated']
admin.site.register(AnnuallyFiveSixFactor, AnnuallyFiveSixFactorAdmin)

"""
