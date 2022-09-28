from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from db.views import UserViewSet, DishesViewSet, OrdersViewSet, MenuViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'dishes', DishesViewSet)
router.register(r'orders', OrdersViewSet)
router.register(r'menus', MenuViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
