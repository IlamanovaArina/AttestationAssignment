import logging
import django_filters.rest_framework

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from sales_network.models import NetworkNode, Product
from sales_network.paginators import SalesNetworkPagination
from sales_network.permissions import IsActiveUser
from sales_network.serializers import NetworkNodeSerializer, ProductSerializer

logger = logging.getLogger('sales_network')


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    API для работы с узлами сети.

    Предоставляет стандартные CRUD-операции, а также дополнительные
    кастомные действия:

    - by_level: Получение всех узлов определенного уровня (завод, розничная сеть, ИП).
    - chain: Получение цепочки узлов, начиная с выбранного узла и поднимаясь вверх по иерархии.
    """
    serializer_class = NetworkNodeSerializer
    pagination_class = SalesNetworkPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['country']
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        """
        Возвращает отсортированный по ID queryset узлов сети.
        Можно расширить для фильтрации или сортировки по другим параметрам.
        """
        logger.info(f"Output of model objects NetworkNode (NetworkNodeViewSet)")
        return NetworkNode.objects.all().order_by('id')

    @action(detail=False, methods=['get'])
    def by_level(self, request):
        """
        Получает список узлов сети, находящихся на указанном уровне иерархии.

        URL-параметры:
        - level (int): уровень узлов, который нужно получить.

        Пример запроса:
        GET /network/by_level/?level=1

        Возвращает:
        - JSON-массив узлов, соответствующих уровню.
        """
        # http://127.0.0.1:8000/network/by_level/?level=1
        # пример запроса с уровнем
        level = int(request.query_params.get('level', 0))
        nodes = [node for node in self.queryset if node.get_level() == level]
        serializer = self.get_serializer(nodes, many=True)
        return Response(serializer.data)

    # Получение цепочки узлов (например, по ID)
    @action(detail=True, methods=['get'])
    def chain(self, request, pk=None):
        """
        Получает цепочку узлов, начиная с выбранного узла и поднимаясь вверх по иерархии.

        URL-параметры:
        - pk (int): ID узла, с которого начинается цепочка.

        Пример запроса:
        GET /network/1/chain/

        Возвращает:
        - JSON-массив узлов, начиная с корневого и заканчивая выбранным.
        """
        node = self.get_object()
        chain = []
        current = node
        while current:
            chain.append(current)
            current = current.provider
        serializer = self.get_serializer(chain[::-1], many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API для работы объектами модели Product.
    Предоставляет стандартные CRUD-операции
    """
    serializer_class = ProductSerializer
    pagination_class = SalesNetworkPagination
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        """
        Возвращает отсортированный по ID queryset узлов сети.
        Можно расширить для фильтрации или сортировки по другим параметрам.
        """
        logger.info(f"Output of model objects (ProductViewSet)")
        return Product.objects.all().order_by('id')
