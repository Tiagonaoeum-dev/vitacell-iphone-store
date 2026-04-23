from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'produtos', api_views.ProdutoViewSet)
router.register(r'clientes', api_views.ClienteViewSet)
router.register(r'vendas', api_views.VendaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]