from . import models

from rest_framework import serializers


class DailyECBRiskFreeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DailyECBRiskFreeRate
        fields = (
            'interval', 
            'RF', 
        )


class MonthlyECBRiskFreeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonthlyECBRiskFreeRate
        fields = (
            'interval', 
            'RF', 
        )


class AnnuallyECBRiskFreeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AnnuallyECBRiskFreeRate
        fields = (
            'interval', 
            'RF', 
        )


class DailyExchangeRateUSDPerXSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DailyExchangeRateUSDPerX
        fields = (
            'interval', 
            'EUR', 
            'JPY', 
            'GBP', 
            'CHF', 
            'RUB', 
            'AUD', 
            'BRL', 
            'CAD', 
            'CNY', 
            'INR', 
        )


class MonthlyExchangeRateUSDPerXSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonthlyExchangeRateUSDPerX
        fields = (
            'interval', 
            'EUR', 
            'JPY', 
            'GBP', 
            'CHF', 
            'RUB', 
            'AUD', 
            'BRL', 
            'CAD', 
            'CNY', 
            'INR', 
        )


class AnnuallyExchangeRateUSDPerXSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AnnuallyExchangeRateUSDPerX
        fields = (
            'interval', 
            'EUR', 
            'JPY', 
            'GBP', 
            'CHF', 
            'RUB', 
            'AUD', 
            'BRL', 
            'CAD', 
            'CNY', 
            'INR', 
        )


class DailyThreeFactorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DailyThreeFactor
        fields = (
            'interval', 
            'MktRF', 
            'SMB', 
            'HML', 
            'RF', 
        )


class MonthlyThreeFactorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonthlyThreeFactor
        fields = (
            'interval', 
            'MktRF', 
            'SMB', 
            'HML', 
            'RF', 
        )


class YearlyThreeFactorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.YearlyThreeFactor
        fields = (
            'interval', 
            'MktRF', 
            'SMB', 
            'HML', 
            'RF', 
        )


class DailyFiveFactorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DailyFiveFactor
        fields = (
            'interval', 
            'MktRF', 
            'SMB', 
            'HML', 
            'RF', 
            'RMW', 
            'CMA', 
        )


class MonthlyFiveFactorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonthlyFiveFactor
        fields = (
            'interval', 
            'MktRF', 
            'SMB', 
            'HML', 
            'RF', 
            'RMW', 
            'CMA', 
        )


class AnnuallyFiveFactorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AnnuallyFiveFactor
        fields = (
            'interval', 
            'MktRF', 
            'SMB', 
            'HML', 
            'RF', 
            'RMW', 
            'CMA', 
        )

