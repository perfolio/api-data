from . import models

from rest_framework import serializers


class ExchangeRateUSDPerXSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ExchangeRateUSDPerX
        fields = (
            'pk', 
            'created', 
            'last_updated', 
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


class ECBRiskFreeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ECBRiskFreeRate
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'interval', 
            'RF', 
        )


class ThreeFactorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ThreeFactor
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'interval', 
            'MktRF', 
            'SMB', 
            'HML', 
            'RF', 
        )


class FiveFactorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FiveFactor
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'RMW', 
            'CMA', 
        )

