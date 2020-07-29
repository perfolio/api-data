from . import models
from . import serializers
from rest_framework import viewsets, permissions


class ExchangeRateUSDPerXViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for the ExchangeRateUSDPerX class"""

    queryset = models.ExchangeRateUSDPerX.objects.all()
    serializer_class = serializers.ExchangeRateUSDPerXSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ECBRiskFreeRateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for the ECBRiskFreeRate class"""

    queryset = models.ECBRiskFreeRate.objects.all()
    serializer_class = serializers.ECBRiskFreeRateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ThreeFactorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for the ThreeFactor class"""

    queryset = models.ThreeFactor.objects.all()
    serializer_class = serializers.ThreeFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FiveFactorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for the FiveFactor class"""

    queryset = models.FiveFactor.objects.all()
    serializer_class = serializers.FiveFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

