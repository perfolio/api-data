from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError, Throttled
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from . import models, serializers

# Config #


intervals = ["daily", "monthly", "annually"]
currencies_rf = ["USD", "EUR"]
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
factors = ["MktRF", "SMB", "HML", "MOM", "RMW", "CMA"]
regions = [
    "USA",
    "Developed",
    "Developed_ex_US",
    "Europe",
    "Japan",
    "Asia_Pacific_ex_Japan",
    "North_America",
]

# Helpers #


def errorhandler(message):
    raise ValidationError({"Error": message})


def throttle_handler(wait):
    raise Throttled(
        detail={
            "Error": f"Request limit exceeded. Reset in {int(wait/60)} min. Create a user account and get your token or contact us for further options.",
        }
    )


def factors_validate_and_filter(obj, factor_model):

    factor = obj.kwargs["factor"]
    region = obj.kwargs["region"]
    currency = obj.kwargs["currency"].upper()
    interval = obj.kwargs["interval"].lower()

    if interval == "daily" and factor_model in [3, 4]:
        model = models.DailyThreeFourFactor
    elif interval == "daily" and factor_model in [5, 6]:
        model = models.DailyFiveSixFactor
    elif interval == "monthly" and factor_model in [3, 4]:
        model = models.MonthlyThreeFourFactor
    elif interval == "monthly" and factor_model in [5, 6]:
        model = models.MonthlyFiveSixFactor
    elif interval == "annually" and factor_model in [3, 4]:
        model = models.AnnuallyThreeFourFactor
    elif interval == "annually" and factor_model in [5, 6]:
        model = models.AnnuallyFiveSixFactor

    from_ = obj.request.GET.get("from")
    to_ = obj.request.GET.get("to")
    dropna_ = obj.request.GET.get("dropna")

    if factor not in factors[:factor_model] and factor != "all":
        errorhandler("Invalid factor. See docs for factors supported.")
    if region not in regions:
        errorhandler("Invalid region. See docs for regions supported")
    if currency not in currencies_fxrates:
        errorhandler("Currency not supported (yet). See docs for currencies supported.")
    if interval.lower() not in intervals:
        errorhandler("Invalid interval. Choose daily, monthly or annually.")

    if from_ is None and to_ is None:
        objects = model.objects.all()
    elif not from_:
        errorhandler("Please select a valid 'from' parameter.")
    elif not to_:
        errorhandler("Please select a valid 'to' parameter.")
    else:
        objects = model.objects.filter(interval__range=[from_, to_])

    objects = objects.filter(currency__exact=currency, region__exact=region)

    if factor != "all":
        objects = objects.values("interval", factor)

    if dropna_ and dropna_.lower() == "false":
        return objects

    if factor != "all":
        return objects.exclude(**{factor + "__isnull": True})

    filter_fields = {}

    for f in factors[:factor_model]:
        filter_fields[f + "__isnull"] = True

    return objects.exclude(**filter_fields)


class QueryTokenAuthentication(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support authentication
    via token parameter in querystring.
    """

    def authenticate(self, request):
        token = request.query_params.get("token")

        if token:
            return self.authenticate_credentials(token.strip())

        return None


class ReadOnlyAPI(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


# Views #

# Risk Free Rate #


class RiskFreeRateView(generics.ListAPIView):
    """View for the RiskFreeRate class"""

    serializer_class = serializers.RiskFreeRateSerializer
    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]

    def get_queryset(self):
        currency = self.kwargs["currency"]
        interval = self.kwargs["interval"].lower()

        if currency not in currencies_rf:
            errorhandler(
                "Currency not supported (yet). See docs for currencies supported."
            )
        if interval.lower() not in intervals:
            errorhandler("Invalid interval. Choose daily, monthly or annually.")

        if interval == "daily":
            model = models.DailyRiskFreeRate
        elif interval == "monthly":
            model = models.MonthlyRiskFreeRate
        elif interval == "annually":
            model = models.AnnuallyRiskFreeRate

        from_ = self.request.GET.get("from")
        to_ = self.request.GET.get("to")
        dropna_ = self.request.GET.get("dropna")

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

    def throttled(self, request, wait):
        throttle_handler(wait)


# Exchange Rates #


class ExchangeRateUSDPerXView(generics.ListAPIView):
    """View for the DailyExchangeRateUSDPerX class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]

    # Overwrite list method to make use of dynamic serializer
    def list(self, request, currency, interval):
        queryset = self.get_queryset()
        serializer = serializers.ExchangeRateUSDPerXSerializer(
            queryset, many=True, fields=["interval", currency]
        )
        return Response(serializer.data)

    def get_queryset(self):
        currency = self.kwargs["currency"]
        interval = self.kwargs["interval"].lower()

        if currency not in currencies_fxrates:
            errorhandler(
                "Currency not supported (yet). See docs for currencies supported."
            )
        if interval.lower() not in intervals:
            errorhandler("Invalid interval. Choose daily, monthly or annually.")

        if interval == "daily":
            model = models.DailyExchangeRateUSDPerX
        elif interval == "monthly":
            model = models.MonthlyExchangeRateUSDPerX
        elif interval == "annually":
            model = models.AnnuallyExchangeRateUSDPerX

        from_ = self.request.GET.get("from")
        to_ = self.request.GET.get("to")
        dropna_ = self.request.GET.get("dropna")

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

    def throttled(self, request, wait):
        throttle_handler(wait)


# Factor returns #


class ThreeFactorView(generics.ListAPIView):
    """View for the ThreeFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]

    def list(self, request, factor, region, currency, interval):
        queryset = self.get_queryset()
        fields = {}

        if factor.lower() != "all":
            fields = {"fields": ["interval", factor]}

        serializer = serializers.ThreeFactorSerializer(queryset, many=True, **fields)
        return Response(serializer.data)

    def get_queryset(self):
        return factors_validate_and_filter(self, 3)

    def throttled(self, request, wait):
        throttle_handler(wait)


class FourFactorView(generics.ListAPIView):
    """View for the DailyFourFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]

    def list(self, request, factor, region, currency, interval):
        queryset = self.get_queryset()
        fields = {}

        if factor.lower() != "all":
            fields = {"fields": ["interval", factor]}

        serializer = serializers.FourFactorSerializer(queryset, many=True, **fields)
        return Response(serializer.data)

    def get_queryset(self):
        return factors_validate_and_filter(self, 4)

    def throttled(self, request, wait):
        throttle_handler(wait)


class FiveFactorView(generics.ListAPIView):
    """View for the DailyFiveFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]

    def list(self, request, factor, region, currency, interval):
        queryset = self.get_queryset()
        fields = {}

        if factor.lower() != "all":
            fields = {"fields": ["interval", factor]}

        serializer = serializers.FiveFactorSerializer(queryset, many=True, **fields)
        return Response(serializer.data)

    def get_queryset(self):
        return factors_validate_and_filter(self, 5)

    def throttled(self, request, wait):
        throttle_handler(wait)


class SixFactorView(generics.ListAPIView):
    """View for the DailySixFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]

    def list(self, request, factor, region, currency, interval):
        queryset = self.get_queryset()
        fields = {}

        if factor.lower() != "all":
            fields = {"fields": ["interval", factor]}

        serializer = serializers.SixFactorSerializer(queryset, many=True, **fields)
        return Response(serializer.data)

    def get_queryset(self):
        return factors_validate_and_filter(self, 6)

    def throttled(self, request, wait):
        throttle_handler(wait)
