from rest_framework.routers import DefaultRouter

from sales_network.apps import SalesNetworkConfig
from sales_network.views import NetworkNodeViewSet, ProductViewSet


app_name = SalesNetworkConfig.name

router = DefaultRouter()
router.register(r'network', NetworkNodeViewSet, basename='network')
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [] + router.urls
