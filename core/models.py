from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Produto(models.Model):
    CONDICAO_CHOICES = [
        ('novo', 'Novo'),
        ('usado', 'Usado'),
    ]
    
    modelo = models.CharField('Modelo', max_length=100)
    capacidade = models.CharField('Capacidade', max_length=20)
    cor = models.CharField('Cor', max_length=50)
    condicao = models.CharField('Condição', max_length=10, choices=CONDICAO_CHOICES, default='novo')
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    quantidade_estoque = models.IntegerField('Quantidade em Estoque', validators=[MinValueValidator(0)])
    descricao = models.TextField('Descrição', blank=True)
    imagem = models.ImageField('Imagem', upload_to='produtos/', blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    def __str__(self):
        return f"{self.modelo} {self.capacidade} - {self.cor}"
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    telefone = models.CharField('Telefone', max_length=20)
    endereco = models.TextField('Endereço')
    cpf = models.CharField('CPF', max_length=14, unique=True)
    data_nascimento = models.DateField('Data de Nascimento')
    
    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class Venda(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vendas')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='vendas')
    quantidade = models.IntegerField('Quantidade', validators=[MinValueValidator(1)])
    preco_unitario = models.DecimalField('Preço Unitário', max_digits=10, decimal_places=2)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_venda = models.DateTimeField('Data da Venda', auto_now_add=True)
    
    def valor_total(self):
        return self.quantidade * self.preco_unitario
    
    def __str__(self):
        return f"Venda #{self.id} - {self.cliente.usuario.get_full_name()}"
    
    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'