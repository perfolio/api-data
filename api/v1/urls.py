from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register(r'dailyecbriskfreerate', api.DailyECBRiskFreeRateViewSet)
router.register(r'monthlyecbriskfreerate', api.MonthlyECBRiskFreeRateViewSet)
router.register(r'annuallyecbriskfreerate', api.AnnuallyECBRiskFreeRateViewSet)
router.register(r'dailyexchangerateusdperx', api.DailyExchangeRateUSDPerXViewSet)
router.register(r'monthlyexchangerateusdperx', api.MonthlyExchangeRateUSDPerXViewSet)
router.register(r'annuallyexchangerateusdperx', api.AnnuallyExchangeRateUSDPerXViewSet)
router.register(r'dailythreefactor', api.DailyThreeFactorViewSet)
router.register(r'monthlythreefactor', api.MonthlyThreeFactorViewSet)
router.register(r'yearlythreefactor', api.YearlyThreeFactorViewSet)
router.register(r'dailyfivefactor', api.DailyFiveFactorViewSet)
router.register(r'monthlyfivefactor', api.MonthlyFiveFactorViewSet)
router.register(r'annuallyfivefactor', api.AnnuallyFiveFactorViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('', include(router.urls)),
)

