from rest_framework import serializers

from . import models


class DailyRiskFreeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyRiskFreeRate
        fields = (
            "interval",
            "RF",
        )


class MonthlyRiskFreeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyRiskFreeRate
        fields = (
            "interval",
            "RF",
        )


class AnnuallyRiskFreeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyRiskFreeRate
        fields = (
            "interval",
            "RF",
        )


class DailyExchangeRateUSDPerXSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyExchangeRateUSDPerX
        fields = (
            "interval",
            "EUR",
            "JPY",
            "GBP",
            "CHF",
            "RUB",
            "AUD",
            "BRL",
            "CAD",
            "CNY",
            "INR",
        )


class MonthlyExchangeRateUSDPerXSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyExchangeRateUSDPerX
        fields = (
            "interval",
            "EUR",
            "JPY",
            "GBP",
            "CHF",
            "RUB",
            "AUD",
            "BRL",
            "CAD",
            "CNY",
            "INR",
        )


class AnnuallyExchangeRateUSDPerXSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyExchangeRateUSDPerX
        fields = (
            "interval",
            "EUR",
            "JPY",
            "GBP",
            "CHF",
            "RUB",
            "AUD",
            "BRL",
            "CAD",
            "CNY",
            "INR",
        )


class DailyThreeFourFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyThreeFourFactor
        fields = ("interval", "MktRF", "SMB", "HML", "MOM", "region", "currency")


class MonthlyThreeFourFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyThreeFourFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "RF",
        )


class YearlyThreeFourFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyThreeFourFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "RF",
        )


class DailyFiveSixFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyFiveSixFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "RF",
            "RMW",
            "CMA",
        )


class MonthlyFiveSixFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyFiveSixFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "RF",
            "RMW",
            "CMA",
        )


class AnnuallyFiveSixFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyFiveSixFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "RF",
            "RMW",
            "CMA",
        )
