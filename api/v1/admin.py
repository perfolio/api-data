from django.contrib import admin
from django import forms
from .models import DailyECBRiskFreeRate, MonthlyECBRiskFreeRate, AnnuallyECBRiskFreeRate, DailyExchangeRateUSDPerX, MonthlyExchangeRateUSDPerX, AnnuallyExchangeRateUSDPerX, DailyThreeFactor, MonthlyThreeFactor, YearlyThreeFactor, DailyFiveFactor, MonthlyFiveFactor, AnnuallyFiveFactor

class DailyECBRiskFreeRateAdminForm(forms.ModelForm):

    class Meta:
        model = DailyECBRiskFreeRate
        fields = '__all__'


class DailyECBRiskFreeRateAdmin(admin.ModelAdmin):
    form = DailyECBRiskFreeRateAdminForm
    list_display = ['created', 'last_updated', 'interval', 'RF']
    readonly_fields = ['created', 'last_updated']
admin.site.register(DailyECBRiskFreeRate, DailyECBRiskFreeRateAdmin)


class MonthlyECBRiskFreeRateAdminForm(forms.ModelForm):

    class Meta:
        model = MonthlyECBRiskFreeRate
        fields = '__all__'


class MonthlyECBRiskFreeRateAdmin(admin.ModelAdmin):
    form = MonthlyECBRiskFreeRateAdminForm
    list_display = ['created', 'last_updated', 'interval', 'RF']
    readonly_fields = ['created', 'last_updated']
admin.site.register(MonthlyECBRiskFreeRate, MonthlyECBRiskFreeRateAdmin)


class AnnuallyECBRiskFreeRateAdminForm(forms.ModelForm):

    class Meta:
        model = AnnuallyECBRiskFreeRate
        fields = '__all__'


class AnnuallyECBRiskFreeRateAdmin(admin.ModelAdmin):
    form = AnnuallyECBRiskFreeRateAdminForm
    list_display = ['created', 'last_updated', 'interval', 'RF']
    readonly_fields = ['created', 'last_updated']
admin.site.register(AnnuallyECBRiskFreeRate, AnnuallyECBRiskFreeRateAdmin)


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


class DailyThreeFactorAdminForm(forms.ModelForm):

    class Meta:
        model = DailyThreeFactor
        fields = '__all__'


class DailyThreeFactorAdmin(admin.ModelAdmin):
    form = DailyThreeFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RF']
    readonly_fields = ['created', 'last_updated']
admin.site.register(DailyThreeFactor, DailyThreeFactorAdmin)


class MonthlyThreeFactorAdminForm(forms.ModelForm):

    class Meta:
        model = MonthlyThreeFactor
        fields = '__all__'


class MonthlyThreeFactorAdmin(admin.ModelAdmin):
    form = MonthlyThreeFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RF']
    readonly_fields = ['created', 'last_updated']
admin.site.register(MonthlyThreeFactor, MonthlyThreeFactorAdmin)


class YearlyThreeFactorAdminForm(forms.ModelForm):

    class Meta:
        model = YearlyThreeFactor
        fields = '__all__'


class YearlyThreeFactorAdmin(admin.ModelAdmin):
    form = YearlyThreeFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RF']
    readonly_fields = ['created', 'last_updated']
admin.site.register(YearlyThreeFactor, YearlyThreeFactorAdmin)


class DailyFiveFactorAdminForm(forms.ModelForm):

    class Meta:
        model = DailyFiveFactor
        fields = '__all__'


class DailyFiveFactorAdmin(admin.ModelAdmin):
    form = DailyFiveFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RF', 'RMW', 'CMA']
    readonly_fields = ['created', 'last_updated']
admin.site.register(DailyFiveFactor, DailyFiveFactorAdmin)


class MonthlyFiveFactorAdminForm(forms.ModelForm):

    class Meta:
        model = MonthlyFiveFactor
        fields = '__all__'


class MonthlyFiveFactorAdmin(admin.ModelAdmin):
    form = MonthlyFiveFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RF', 'RMW', 'CMA']
    readonly_fields = ['created', 'last_updated']
admin.site.register(MonthlyFiveFactor, MonthlyFiveFactorAdmin)


class AnnuallyFiveFactorAdminForm(forms.ModelForm):

    class Meta:
        model = AnnuallyFiveFactor
        fields = '__all__'


class AnnuallyFiveFactorAdmin(admin.ModelAdmin):
    form = AnnuallyFiveFactorAdminForm
    list_display = ['created', 'last_updated', 'interval', 'MktRF', 'SMB', 'HML', 'RF', 'RMW', 'CMA']
    readonly_fields = ['created', 'last_updated']
admin.site.register(AnnuallyFiveFactor, AnnuallyFiveFactorAdmin)

