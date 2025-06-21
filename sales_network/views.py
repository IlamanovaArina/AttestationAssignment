from rest_framework import viewsets

from sales_network.models import NetworkNode, Product
from sales_network.paginators import SalesNetworkPagination
from sales_network.serializers import NetworkNodeSerializer, ProductSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all().order_by('id')
    serializer_class = NetworkNodeSerializer
    pagination_class = SalesNetworkPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    pagination_class = SalesNetworkPagination
