from rest_framework import serializers

from sales_network.models import NetworkNode, Product


class NetworkNodeSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()

    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ['debt']

    def get_level(self, obj):
        return obj.get_level()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
