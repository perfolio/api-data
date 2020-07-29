from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register(r'exchangerateusdperx', api.ExchangeRateUSDPerXViewSet)
router.register(r'ecbriskfreerate', api.ECBRiskFreeRateViewSet)
router.register(r'threefactor', api.ThreeFactorViewSet)
router.register(r'fivefactor', api.FiveFactorViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('', include(router.urls)),
)

