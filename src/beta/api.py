from drf_renderer_xlsx.mixins import XLSXFileMixin
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from get_data.config.general import currencies_fxrates, factors, intervals, regions

from . import models, serializers
from .util import ReadOnlyAPI, get_params, range_filter

# Views #

# Risk Free Rate #


class RiskFreeRateView(XLSXFileMixin, generics.ListAPIView):
    """View for the RiskFreeRate class"""

    serializer_class = serializers.RiskFreeRateSerializer
    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
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


# Exchange Rates #


class ExchangeRateUSDPerXView(XLSXFileMixin, generics.ListAPIView):
    """View for the DailyExchangeRateUSDPerX class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
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


# Factor returns #


class ThreeFactorView(XLSXFileMixin, generics.ListAPIView):
    """View for the ThreeFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
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


class FourFactorView(XLSXFileMixin, generics.ListAPIView):
    """View for the DailyFourFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
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


class FiveFactorView(XLSXFileMixin, generics.ListAPIView):
    """View for the DailyFiveFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
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


class SixFactorView(XLSXFileMixin, generics.ListAPIView):
    """View for the DailySixFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
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


class InvalidUrlPath(generics.ListAPIView):
    """View for invalid UrlPaths"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]

    def get_queryset(self):
        raise ValidationError(
            {"Error": "No data at this location. Please check URL path."}
        )


class EndpointsView(APIView):
    """View for possible endpoints"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]

    def get(self, request, format=None):
        """"""
        return Response(
            {
                "factorModels": [
                    {
                        "value": "3factor",
                        "display": "3 factor model by Fama & French 1993",
                        "factors": [
                            {
                                "value": "mktrf",
                                "display": "Mkt-RF",
                            },
                            {
                                "value": "smb",
                                "display": "SMB",
                            },
                            {
                                "value": "hml",
                                "display": "HML",
                            },
                            {
                                "value": "all",
                                "display": "All factors",
                            },
                        ],
                    },
                    {
                        "value": "4factor",
                        "display": "4 factor model by Carhart 1997",
                        "factors": [
                            {
                                "value": "mktrf",
                                "display": "Mkt-RF",
                            },
                            {
                                "value": "smb",
                                "display": "SMB",
                            },
                            {
                                "value": "hml",
                                "display": "HML",
                            },
                            {
                                "value": "mom",
                                "display": "MOM",
                            },
                            {
                                "value": "all",
                                "display": "All factors",
                            },
                        ],
                    },
                    {
                        "value": "5factor",
                        "display": "5 factor model by Fama & French 2015",
                        "factors": [
                            {
                                "value": "mktrf",
                                "display": "Mkt-RF",
                            },
                            {
                                "value": "smb",
                                "display": "SMB",
                            },
                            {
                                "value": "hml",
                                "display": "HML",
                            },
                            {
                                "value": "rmw",
                                "display": "RMW",
                            },
                            {
                                "value": "cma",
                                "display": "CMA",
                            },
                            {
                                "value": "all",
                                "display": "All factors",
                            },
                        ],
                    },
                    {
                        "value": "6factor",
                        "display": "6 factor model by Fama & French 2018",
                        "factors": [
                            {
                                "value": "mktrf",
                                "display": "Mkt-RF",
                            },
                            {
                                "value": "smb",
                                "display": "SMB",
                            },
                            {
                                "value": "hml",
                                "display": "HML",
                            },
                            {
                                "value": "rmw",
                                "display": "RMW",
                            },
                            {
                                "value": "cma",
                                "display": "CMA",
                            },
                            {
                                "value": "mom",
                                "display": "MOM",
                            },
                            {
                                "value": "all",
                                "display": "All factors",
                            },
                        ],
                    },
                ],
                "regions": regions,
                "currencies": currencies_fxrates,
                "intervals": intervals,
            }
        )
