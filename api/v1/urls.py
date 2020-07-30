from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register(r'eurrf/daily', api.DailyECBRiskFreeRateViewSet)
router.register(r'eurrf/monthly', api.MonthlyECBRiskFreeRateViewSet)
router.register(r'eurrf/annually', api.AnnuallyECBRiskFreeRateViewSet)
router.register(r'fxrate/daily', api.DailyExchangeRateUSDPerXViewSet)
router.register(r'fxrate/monthly', api.MonthlyExchangeRateUSDPerXViewSet)
router.register(r'fxrate/annually', api.AnnuallyExchangeRateUSDPerXViewSet)
router.register(r'3factor/daily', api.DailyThreeFactorViewSet)
router.register(r'3factor/monthly', api.MonthlyThreeFactorViewSet)
router.register(r'3factor/annually', api.YearlyThreeFactorViewSet)
router.register(r'5factor/daily', api.DailyFiveFactorViewSet)
router.register(r'5factor/monthly', api.MonthlyFiveFactorViewSet)
router.register(r'5factor/annually', api.AnnuallyFiveFactorViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('', include(router.urls)),
)

