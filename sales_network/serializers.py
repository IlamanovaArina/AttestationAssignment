from rest_framework import serializers

from sales_network.models import NetworkNode, Product


class NetworkNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
