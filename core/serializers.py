from rest_framework import serializers
from .models import Produto, Cliente, Venda

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    nome_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Cliente
        fields = '__all__'
    
    def get_nome_completo(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.username

class VendaSerializer(serializers.ModelSerializer):
    valor_total = serializers.SerializerMethodField()
    cliente_nome = serializers.CharField(source='cliente.usuario.get_full_name', read_only=True)
    produto_nome = serializers.CharField(source='produto.modelo', read_only=True)
    
    class Meta:
        model = Venda
        fields = '__all__'
    
    def get_valor_total(self, obj):
        return obj.quantidade * obj.preco_unitario