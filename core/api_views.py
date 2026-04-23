from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Produto, Cliente, Venda
from .serializers import ProdutoSerializer, ClienteSerializer, VendaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    
    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        produtos = Produto.objects.filter(quantidade_estoque__gt=0)
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.select_related('usuario').all()
    serializer_class = ClienteSerializer

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.select_related('cliente__usuario', 'produto').all()
    serializer_class = VendaSerializer