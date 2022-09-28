from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filters import OrdersFilter
from .models import User, Dishes, Menu, Orders
from .serializers import (UserSerializer, DishesSerializer,
                          OrdersSerializer, MenuSerializer,
                          OrdersCreateUpdateSerializer,
                          MenuCreateUpdateSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


class DishesViewSet(viewsets.ModelViewSet):
    queryset = Dishes.objects.all()
    serializer_class = DishesSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        ids = self.request.query_params.get('ids', None)
        if ids:
            ids_list = ids.split(',')
            queryset = queryset.filter(id__in=ids_list)

        return queryset


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    # serializer_class = MenuSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MenuCreateUpdateSerializer
        return MenuSerializer

class OrdersViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Orders.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrdersFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrdersCreateUpdateSerializer
        return OrdersSerializer
