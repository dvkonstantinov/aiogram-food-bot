import django_filters

from db.models import Orders


class OrdersFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='menu__date_of_menu',
                                     lookup_expr='exact')

    class Meta:
        model = Orders
        fields = ['date']
