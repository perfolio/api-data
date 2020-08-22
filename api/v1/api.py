from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from . import models, serializers


def errorhandler(message):
    raise ValidationError({"Error": message})


def fxrates_validate_and_filter(currency, from_, to_, dropna_, model):
    if from_ is None and to_ is None:
        objects = model.objects.all()
    elif not from_:
        errorhandler("Please select a valid 'from' parameter.")
    elif not to_:
        errorhandler("Please select a valid 'to' parameter.")
    else:
        objects = model.objects.filter(interval__range=[from_, to_])

    objects = objects.values("interval", currency)

    if dropna_ and dropna_.lower() == "false":
        return objects

    return objects.exclude(**{currency + "__isnull": True})


def rf_validate_and_filter(currency, from_, to_, dropna_, model):
    if from_ is None and to_ is None:
        objects = model.objects.all()
    elif not from_:
        errorhandler("Please select a valid 'from' parameter.")
    elif not to_:
        errorhandler("Please select a valid 'to' parameter.")
    else:
        objects = model.objects.filter(interval__range=[from_, to_])

    objects = objects.filter(currency__exact=currency)

    if dropna_ and dropna_.lower() == "false":
        return objects

    return objects.exclude(RF__isnull=True)


### Risk Free Rate ###

currencies_rf = ["USD", "EUR"]


class DailyRiskFreeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyRiskFreeRate class"""

    def get_queryset(self):
        currency = self.kwargs["currency"]
        if currency not in currencies_rf:
            errorhandler(
                "Currency not supported (yet). See docs for currencies supported."
            )

        from_ = self.request.GET.get("from")
        to_ = self.request.GET.get("to")
        dropna_ = self.request.GET.get("dropna")

        return rf_validate_and_filter(
            currency, from_, to_, dropna_, models.DailyRiskFreeRate
        )

    # Fallback queryset and serializer class
    queryset = models.DailyRiskFreeRate.objects.all()
    serializer_class = serializers.RiskFreeRateSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyRiskFreeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyRiskFreeRate class"""

    def get_queryset(self):
        currency = self.kwargs["currency"]
        if currency not in currencies_rf:
            errorhandler(
                "Currency not supported (yet). See docs for currencies supported."
            )

        from_ = self.request.GET.get("from")
        to_ = self.request.GET.get("to")
        dropna_ = self.request.GET.get("dropna")

        return rf_validate_and_filter(
            currency, from_, to_, dropna_, models.MonthlyRiskFreeRate
        )

    # Fallback queryset and serializer class
    queryset = models.MonthlyRiskFreeRate.objects.all()
    serializer_class = serializers.RiskFreeRateSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallyRiskFreeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyRiskFreeRate class"""

    def get_queryset(self):
        currency = self.kwargs["currency"]
        if currency not in currencies_rf:
            errorhandler(
                "Currency not supported (yet). See docs for currencies supported."
            )

        from_ = self.request.GET.get("from")
        to_ = self.request.GET.get("to")
        dropna_ = self.request.GET.get("dropna")

        return rf_validate_and_filter(
            currency, from_, to_, dropna_, models.AnnuallyRiskFreeRate
        )

    # Fallback queryset and serializer class
    queryset = models.AnnuallyRiskFreeRate.objects.all()
    serializer_class = serializers.RiskFreeRateSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


### Exchange Rates ###

currencies_fxrates = [
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
    "DKK",
    "NZD",
    "NOK",
    "SEK",
    "PLN",
    "ILS",
    "KRW",
    "TRY",
]


class DailyExchangeRateUSDPerXViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for the DailyExchangeRateUSDPerX class"""

    # Overwrite list method to make use of dynamic serializer
    def list(self, request, currency):
        queryset = self.get_queryset()
        serializer = serializers.ExchangeRateUSDPerXSerializer(
            queryset, many=True, fields=["interval", currency]
        )
        return Response(serializer.data)

    def get_queryset(self):
        currency = self.kwargs["currency"]
        if currency not in currencies_fxrates:
            errorhandler(
                "Currency not supported (yet). See docs for currencies supported."
            )

        from_ = self.request.GET.get("from")
        to_ = self.request.GET.get("to")
        dropna_ = self.request.GET.get("dropna")

        return validate_and_filter(
            currency, from_, to_, dropna_, models.DailyExchangeRateUSDPerX
        )

    # Fallback queryset and serializer class
    queryset = models.DailyExchangeRateUSDPerX.objects.all()
    serializer_class = serializers.ExchangeRateUSDPerXSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyExchangeRateUSDPerXViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyExchangeRateUSDPerX class"""

    def list(self, request, currency):
        queryset = self.get_queryset()
        serializer = serializers.ExchangeRateUSDPerXSerializer(
            queryset, many=True, fields=["interval", currency]
        )
        return Response(serializer.data)

    def get_queryset(self):
        currency = self.kwargs["currency"]
        if currency not in currencies_fxrates:
            errorhandler(
                "Currency not supported (yet). See docs for currencies supported."
            )

        from_ = self.request.GET.get("from")
        to_ = self.request.GET.get("to")
        dropna_ = self.request.GET.get("dropna")

        return validate_and_filter(
            currency, from_, to_, dropna_, models.MonthlyExchangeRateUSDPerX
        )

    # Fallback queryset and serializer class
    queryset = models.MonthlyExchangeRateUSDPerX.objects.all()
    serializer_class = serializers.ExchangeRateUSDPerXSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallyExchangeRateUSDPerXViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyExchangeRateUSDPerX class"""

    def list(self, request, currency):
        queryset = self.get_queryset()
        serializer = serializers.ExchangeRateUSDPerXSerializer(
            queryset, many=True, fields=["interval", currency]
        )
        return Response(serializer.data)

    def get_queryset(self):
        currency = self.kwargs["currency"]
        if currency not in currencies_fxrates:
            errorhandler(
                "Currency not supported (yet). See docs for currencies supported."
            )

        from_ = self.request.GET.get("from")
        to_ = self.request.GET.get("to")
        dropna_ = self.request.GET.get("dropna")

        return validate_and_filter(
            currency, from_, to_, dropna_, models.AnnuallyExchangeRateUSDPerX
        )

    # Fallback queryset and serializer class
    queryset = models.AnnuallyExchangeRateUSDPerX.objects.all()
    serializer_class = serializers.ExchangeRateUSDPerXSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DailyThreeFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyThreeFactor class"""

    queryset = models.DailyThreeFourFactor.objects.all()
    serializer_class = serializers.DailyThreeFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyThreeFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyThreeFactor class"""

    queryset = models.MonthlyThreeFourFactor.objects.all()
    serializer_class = serializers.MonthlyThreeFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallyThreeFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyThreeFactor class"""

    queryset = models.AnnuallyThreeFourFactor.objects.all()
    serializer_class = serializers.AnnuallyThreeFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DailyFourFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyFourFactor class"""

    queryset = models.DailyThreeFourFactor.objects.all()
    serializer_class = serializers.DailyFourFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyFourFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyFourFactor class"""

    queryset = models.MonthlyThreeFourFactor.objects.all()
    serializer_class = serializers.MonthlyFourFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallyFourFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyFourFactor class"""

    queryset = models.AnnuallyThreeFourFactor.objects.all()
    serializer_class = serializers.AnnuallyFourFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DailyFiveFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyFiveFactor class"""

    queryset = models.DailyFiveSixFactor.objects.all()
    serializer_class = serializers.DailyFiveFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyFiveFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyFiveFactor class"""

    queryset = models.MonthlyFiveSixFactor.objects.all()
    serializer_class = serializers.MonthlyFiveFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallyFiveFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyFiveFactor class"""

    queryset = models.AnnuallyFiveSixFactor.objects.all()
    serializer_class = serializers.AnnuallyFiveFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DailySixFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailySixFactor class"""

    queryset = models.DailyFiveSixFactor.objects.all()
    serializer_class = serializers.DailySixFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlySixFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlySixFactor class"""

    queryset = models.MonthlyFiveSixFactor.objects.all()
    serializer_class = serializers.MonthlySixFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallySixFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallySixFactor class"""

    queryset = models.AnnuallyFiveSixFactor.objects.all()
    serializer_class = serializers.AnnuallySixFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


### Single factors ###

factors = ["MktRF", "SMB", "HML", "RMW", "CMA", "MOM"]


class DailyFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the DailyFactor class"""

    queryset = models.DailyFiveSixFactor.objects.all()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MonthlyFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the MonthlyFactor class"""

    queryset = models.MonthlyFiveSixFactor.objects.all()
    serializer_class = serializers.MonthlyMktRFFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnuallyFactorViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnnuallyFactor class"""

    queryset = models.AnnuallyFiveSixFactor.objects.all()
    serializer_class = serializers.AnnuallyMktRFFactorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
