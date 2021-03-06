from rest_framework import serializers

from . import models


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.

    Code from https://www.django-rest-framework.org/api-guide/serializers/
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class RiskFreeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RiskFreeRate
        fields = ("period", "rf")


class ExchangeRateUSDPerXSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.ExchangeRateUSDPerX
        fields = "__all__"


class ThreeFactorSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.ThreeFourFactor
        fields = (
            "period",
            "mktrf",
            "smb",
            "hml",
        )


class FourFactorSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.ThreeFourFactor
        fields = (
            "period",
            "mktrf",
            "smb",
            "hml",
            "mom",
        )


class FiveFactorSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.FiveSixFactor
        fields = (
            "period",
            "mktrf",
            "smb",
            "hml",
            "rmw",
            "cma",
        )


class SixFactorSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.FiveSixFactor
        fields = (
            "period",
            "mktrf",
            "smb",
            "hml",
            "rmw",
            "cma",
            "mom",
        )
