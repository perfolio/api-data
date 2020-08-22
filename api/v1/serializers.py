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
        model = models.DailyRiskFreeRate
        fields = ["interval", "RF"]


class ExchangeRateUSDPerXSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.DailyExchangeRateUSDPerX
        fields = "__all__"


class DailyThreeFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyThreeFourFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
        )


class MonthlyThreeFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyThreeFourFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
        )


class AnnuallyThreeFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyThreeFourFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
        )


class DailyFourFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyThreeFourFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "MOM",
        )


class MonthlyFourFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyThreeFourFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "MOM",
        )


class AnnuallyFourFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyThreeFourFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "MOM",
        )


class DailyFiveFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyFiveSixFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "RMW",
            "CMA",
        )


class MonthlyFiveFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyFiveSixFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "RMW",
            "CMA",
        )


class AnnuallyFiveFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyFiveSixFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "RMW",
            "CMA",
        )


class DailySixFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyFiveSixFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "RMW",
            "CMA",
            "MOM",
        )


class MonthlySixFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyFiveSixFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "RMW",
            "CMA",
            "MOM",
        )


class AnnuallySixFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyFiveSixFactor
        fields = (
            "interval",
            "MktRF",
            "SMB",
            "HML",
            "RMW",
            "CMA",
            "MOM",
        )


class DailyMktRFFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyFiveSixFactor
        fields = (
            "interval",
            "MktRF",
        )


class MonthlyMktRFFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyFiveSixFactor
        fields = (
            "interval",
            "MktRF",
        )


class AnnuallyMktRFFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyFiveSixFactor
        fields = (
            "interval",
            "MktRF",
        )


class DailySMBFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyFiveSixFactor
        fields = (
            "interval",
            "SMB",
        )


class MonthlySMBFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyFiveSixFactor
        fields = (
            "interval",
            "SMB",
        )


class AnnuallySMBFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyFiveSixFactor
        fields = (
            "interval",
            "SMB",
        )


class DailyHMLFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyFiveSixFactor
        fields = (
            "interval",
            "HML",
        )


class MonthlyHMLFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyFiveSixFactor
        fields = (
            "interval",
            "HML",
        )


class AnnuallyHMLFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyFiveSixFactor
        fields = (
            "interval",
            "HML",
        )


class DailyRMWFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyFiveSixFactor
        fields = (
            "interval",
            "RMW",
        )


class MonthlyRMWFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyFiveSixFactor
        fields = (
            "interval",
            "RMW",
        )


class AnnuallyRMWFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyFiveSixFactor
        fields = (
            "interval",
            "RMW",
        )


class DailyCMAFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyFiveSixFactor
        fields = (
            "interval",
            "CMA",
        )


class MonthlyCMAFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyFiveSixFactor
        fields = (
            "interval",
            "CMA",
        )


class AnnuallyCMAFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyFiveSixFactor
        fields = (
            "interval",
            "CMA",
        )


class DailyMOMFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyFiveSixFactor
        fields = (
            "interval",
            "MOM",
        )


class MonthlyMOMFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonthlyFiveSixFactor
        fields = (
            "interval",
            "MOM",
        )


class AnnuallyMOMFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnuallyFiveSixFactor
        fields = (
            "interval",
            "MOM",
        )
