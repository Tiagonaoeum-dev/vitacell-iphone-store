from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store_home, name='store_home'),
    path('store/comprar/', views.store_comprar, name='store_comprar'),
    path('produto/<int:pk>/', views.produto_detalhe, name='produto_detalhe'),
    path('produtos/', views.produto_lista, name='produto_lista'),
    path('produtos/novo/', views.produto_create, name='produto_create'),
    path('produtos/editar/<int:pk>/', views.produto_edit, name='produto_edit'),
    path('produtos/deletar/<int:pk>/', views.produto_delete, name='produto_delete'),
    path('clientes/', views.cliente_lista, name='cliente_lista'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/editar/<int:pk>/', views.cliente_edit, name='cliente_edit'),
    path('clientes/deletar/<int:pk>/', views.cliente_delete, name='cliente_delete'),
    path('vendas/', views.venda_lista, name='venda_lista'),
    path('vendas/nova/', views.venda_create, name='venda_create'),
    path('vendas/editar/<int:pk>/', views.venda_edit, name='venda_edit'),
    path('vendas/deletar/<int:pk>/', views.venda_delete, name='venda_delete'),
]