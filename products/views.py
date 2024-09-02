from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.paginators import Paginator
from products.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    """ Вьюсет для товаров """

    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('id')
    pagination_class = Paginator
    permission_classes = [IsAuthenticated]
