from . import models
from . import serializers
from rest_framework import viewsets, permissions


class DailyECBRiskFreeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyECBRiskFreeRate class"""

    queryset = models.DailyECBRiskFreeRate.objects.all()
    serializer_class = serializers.DailyECBRiskFreeRateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyECBRiskFreeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyECBRiskFreeRate class"""

    queryset = models.MonthlyECBRiskFreeRate.objects.all()
    serializer_class = serializers.MonthlyECBRiskFreeRateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallyECBRiskFreeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyECBRiskFreeRate class"""

    queryset = models.AnnuallyECBRiskFreeRate.objects.all()
    serializer_class = serializers.AnnuallyECBRiskFreeRateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DailyExchangeRateUSDPerXViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyExchangeRateUSDPerX class"""

    queryset = models.DailyExchangeRateUSDPerX.objects.all()
    serializer_class = serializers.DailyExchangeRateUSDPerXSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyExchangeRateUSDPerXViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyExchangeRateUSDPerX class"""

    queryset = models.MonthlyExchangeRateUSDPerX.objects.all()
    serializer_class = serializers.MonthlyExchangeRateUSDPerXSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallyExchangeRateUSDPerXViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyExchangeRateUSDPerX class"""

    queryset = models.AnnuallyExchangeRateUSDPerX.objects.all()
    serializer_class = serializers.AnnuallyExchangeRateUSDPerXSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DailyThreeFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyThreeFactor class"""

    queryset = models.DailyThreeFactor.objects.all()
    serializer_class = serializers.DailyThreeFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyThreeFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyThreeFactor class"""

    queryset = models.MonthlyThreeFactor.objects.all()
    serializer_class = serializers.MonthlyThreeFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class YearlyThreeFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the YearlyThreeFactor class"""

    queryset = models.YearlyThreeFactor.objects.all()
    serializer_class = serializers.YearlyThreeFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DailyFiveFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyFiveFactor class"""

    queryset = models.DailyFiveFactor.objects.all()
    serializer_class = serializers.DailyFiveFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyFiveFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyFiveFactor class"""

    queryset = models.MonthlyFiveFactor.objects.all()
    serializer_class = serializers.MonthlyFiveFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallyFiveFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyFiveFactor class"""

    queryset = models.AnnuallyFiveFactor.objects.all()
    serializer_class = serializers.AnnuallyFiveFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

