from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from drf_renderer_xlsx.mixins import XLSXFileMixin
from . import models, serializers
from .util import ReadOnlyAPI, QueryTokenAuthentication, get_params, range_filter
from get_data.config.general import factors

# Views #

# Risk Free Rate #


class RiskFreeRateView(XLSXFileMixin, generics.ListAPIView):
    """View for the RiskFreeRate class"""

    serializer_class = serializers.RiskFreeRateSerializer
    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]
    filename = "rf_perfolio.xlsx"

    def get_queryset(self):
        params_dict = get_params(self, True)

        objects = range_filter(
            params_dict["from"],
            params_dict["to"],
            params_dict["interval"],
            models.RiskFreeRate,
        )

        objects = objects.filter(
            currency__exact=params_dict["currency"],
            interval__exact=params_dict["interval"],
        )

        if params_dict["dropna"] and params_dict["dropna"].lower() == "false":
            return objects

        return objects.exclude(rf__isnull=True)

    def throttled(self, request, wait):
        throttle_handler(wait)


# Exchange Rates #


class ExchangeRateUSDPerXView(XLSXFileMixin, generics.ListAPIView):
    """View for the DailyExchangeRateUSDPerX class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]
    filename = "fx_perfolio.xlsx"

    # Overwrite list method to make use of dynamic serializer
    def list(self, request, currency, interval):
        queryset = self.get_queryset()
        serializer = serializers.ExchangeRateUSDPerXSerializer(
            queryset, many=True, fields=["period", currency.upper()]
        )
        return Response(serializer.data)

    def get_queryset(self):

        params_dict = get_params(self)

        objects = range_filter(
            params_dict["from"],
            params_dict["to"],
            params_dict["interval"],
            models.ExchangeRateUSDPerX,
        )

        objects = objects.values("period", params_dict["currency"]).filter(
            interval__exact=params_dict["interval"]
        )

        if params_dict["dropna"] and params_dict["dropna"].lower() == "false":
            return objects

        return objects.exclude(**{params_dict["currency"] + "__isnull": True})

    def throttled(self, request, wait):
        throttle_handler(wait)


# Factor returns #


class ThreeFactorView(XLSXFileMixin, generics.ListAPIView):
    """View for the ThreeFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]
    filename = "3factor_perfolio.xlsx"

    def list(self, request, factor, region, currency, interval):
        queryset = self.get_queryset()
        fields = {}

        if factor.lower() != "all":
            fields = {"fields": ["period", factor]}

        serializer = serializers.ThreeFactorSerializer(queryset, many=True, **fields)
        return Response(serializer.data)

    def get_queryset(self):
        params_dict = get_params(self, False, 3)

        objects = range_filter(
            params_dict["from"],
            params_dict["to"],
            params_dict["interval"],
            models.ThreeFourFactor,
        )

        objects = objects.filter(
            currency__exact=params_dict["currency"],
            region__exact=params_dict["region"],
            interval__exact=params_dict["interval"],
        )

        if params_dict["factor"] != "all":
            objects = objects.values("period", params_dict["factor"])

        if params_dict["dropna"] and params_dict["dropna"].lower() == "false":
            return objects

        if params_dict["factor"] != "all":
            return objects.exclude(**{params_dict["factor"] + "__isnull": True})

        filter_fields = {}

        for f in factors[:3]:
            filter_fields[f + "__isnull"] = True

        return objects.exclude(**filter_fields)

    def throttled(self, request, wait):
        throttle_handler(wait)


class FourFactorView(XLSXFileMixin, generics.ListAPIView):
    """View for the DailyFourFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]
    filename = "4factor_perfolio.xlsx"

    def list(self, request, factor, region, currency, interval):
        queryset = self.get_queryset()
        fields = {}

        if factor.lower() != "all":
            fields = {"fields": ["period", factor]}

        serializer = serializers.FourFactorSerializer(queryset, many=True, **fields)
        return Response(serializer.data)

    def get_queryset(self):
        params_dict = get_params(self, False, 4)

        objects = range_filter(
            params_dict["from"],
            params_dict["to"],
            params_dict["interval"],
            models.ThreeFourFactor,
        )

        objects = objects.filter(
            currency__exact=params_dict["currency"],
            region__exact=params_dict["region"],
            interval__exact=params_dict["interval"],
        )

        if params_dict["factor"] != "all":
            objects = objects.values("period", params_dict["factor"])

        if params_dict["dropna"] and params_dict["dropna"].lower() == "false":
            return objects

        if params_dict["factor"] != "all":
            return objects.exclude(**{params_dict["factor"] + "__isnull": True})

        filter_fields = {}

        for f in factors[:4]:
            filter_fields[f + "__isnull"] = True

        return objects.exclude(**filter_fields)

    def throttled(self, request, wait):
        throttle_handler(wait)


class FiveFactorView(XLSXFileMixin, generics.ListAPIView):
    """View for the DailyFiveFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]
    filename = "5factor_perfolio.xlsx"

    def list(self, request, factor, region, currency, interval):
        queryset = self.get_queryset()
        fields = {}

        if factor.lower() != "all":
            fields = {"fields": ["period", factor]}

        serializer = serializers.FiveFactorSerializer(queryset, many=True, **fields)
        return Response(serializer.data)

    def get_queryset(self):
        params_dict = get_params(self, False, 5)

        objects = range_filter(
            params_dict["from"],
            params_dict["to"],
            params_dict["interval"],
            models.FiveSixFactor,
        )

        objects = objects.filter(
            currency__exact=params_dict["currency"],
            region__exact=params_dict["region"],
            interval__exact=params_dict["interval"],
        )

        if params_dict["factor"] != "all":
            objects = objects.values("period", params_dict["factor"])

        if params_dict["dropna"] and params_dict["dropna"].lower() == "false":
            return objects

        if params_dict["factor"] != "all":
            return objects.exclude(**{params_dict["factor"] + "__isnull": True})

        filter_fields = {}

        for f in factors[:5]:
            filter_fields[f + "__isnull"] = True

        return objects.exclude(**filter_fields)

    def throttled(self, request, wait):
        throttle_handler(wait)


class SixFactorView(XLSXFileMixin, generics.ListAPIView):
    """View for the DailySixFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]
    filename = "6factor_perfolio.xlsx"

    def list(self, request, factor, region, currency, interval):
        queryset = self.get_queryset()
        fields = {}

        if factor.lower() != "all":
            fields = {"fields": ["period", factor]}

        serializer = serializers.SixFactorSerializer(queryset, many=True, **fields)
        return Response(serializer.data)

    def get_queryset(self):
        params_dict = get_params(self, False, 6)

        objects = range_filter(
            params_dict["from"],
            params_dict["to"],
            params_dict["interval"],
            models.FiveSixFactor,
        )

        objects = objects.filter(
            currency__exact=params_dict["currency"],
            region__exact=params_dict["region"],
            interval__exact=params_dict["interval"],
        )

        if params_dict["factor"] != "all":
            objects = objects.values("period", params_dict["factor"])

        if params_dict["dropna"] and params_dict["dropna"].lower() == "false":
            return objects

        if params_dict["factor"] != "all":
            return objects.exclude(**{params_dict["factor"] + "__isnull": True})

        filter_fields = {}

        for f in factors[:6]:
            filter_fields[f + "__isnull"] = True

        return objects.exclude(**filter_fields)

    def throttled(self, request, wait):
        throttle_handler(wait)


class InvalidUrlPath(generics.ListAPIView):
    """View for invalid UrlPaths"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]

    def get_queryset(self):
        raise ValidationError(
            {"Error": "No data at this location. Please check URL path."}
        )

    def throttled(self, request, wait):
        throttle_handler(wait)
