from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import ValidationError

from . import models, serializers


class DailyRiskFreeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyRiskFreeRate class"""

    queryset = models.DailyRiskFreeRate.objects.all()
    serializer_class = serializers.DailyRiskFreeRateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyRiskFreeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyRiskFreeRate class"""

    queryset = models.MonthlyRiskFreeRate.objects.all()

    def get_queryset(self):
        from_ = self.request.GET.get("from")
        if not from_:
            raise ValidationError({"error": "!!!"})
        to_ = self.request.GET.get("to")

        return models.MonthlyRiskFreeRate.objects.filter(interval__range=[from_, to_])

    serializer_class = serializers.MonthlyRiskFreeRateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallyRiskFreeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyRiskFreeRate class"""

    queryset = models.AnnuallyRiskFreeRate.objects.all()
    serializer_class = serializers.AnnuallyRiskFreeRateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


### Exchange Rates ###


class DailyExchangeRateUSDPerXViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyExchangeRateUSDPerX class"""

    queryset = models.DailyExchangeRateUSDPerX.objects.all()
    serializer_class = serializers.DailyExchangeRateUSDPerXSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyExchangeRateUSDPerXViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyExchangeRateUSDPerX class"""

    queryset = models.MonthlyExchangeRateUSDPerX.objects.all()

    def get_queryset(self):
        from_ = self.request.GET.get("from")
        if from_ is None:
            raise ValidationError({"error": "!!!"})

        to_ = self.request.GET.get("to")
        if to_ is None:
            raise ValidationError({})

        if self.kwargs["currency"] not in ["EUR", "JPY", "GBP"]:
            raise ValidationError({"Error": "currency not supported."})
        return models.MonthlyExchangeRateUSDPerX.objects.filter(
            interval__range=[from_, to_]
        ).values("interval", self.kwargs["currency"])

    serializer_class = serializers.MonthlyExchangeRateUSDPerXSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallyExchangeRateUSDPerXViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyExchangeRateUSDPerX class"""

    queryset = models.AnnuallyExchangeRateUSDPerX.objects.all()
    serializer_class = serializers.AnnuallyExchangeRateUSDPerXSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DailyThreeFourFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyThreeFourFactor class"""

    queryset = models.DailyThreeFourFactor.objects.all()
    serializer_class = serializers.DailyThreeFourFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyThreeFourFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyThreeFourFactor class"""

    queryset = models.MonthlyThreeFourFactor.objects.all()
    serializer_class = serializers.MonthlyThreeFourFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class YearlyThreeFourFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyThreeFourFactor class"""

    queryset = models.AnnuallyThreeFourFactor.objects.all()
    serializer_class = serializers.YearlyThreeFourFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DailyFiveSixFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyFiveSixFactor class"""

    queryset = models.DailyFiveSixFactor.objects.all()
    serializer_class = serializers.DailyFiveSixFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyFiveSixFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyFiveSixFactor class"""

    queryset = models.MonthlyFiveSixFactor.objects.all()
    serializer_class = serializers.MonthlyFiveSixFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallyFiveSixFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyFiveSixFactor class"""

    queryset = models.AnnuallyFiveSixFactor.objects.all()
    serializer_class = serializers.AnnuallyFiveSixFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
