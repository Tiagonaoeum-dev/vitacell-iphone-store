from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto, Cliente, Venda
from .forms import ProdutoForm, ClienteForm, VendaForm
from django.contrib.auth.models import User
import random

@login_required
def home(request):
    context = {
        'total_produtos': Produto.objects.count(),
        'total_clientes': Cliente.objects.count(),
        'total_vendas': Venda.objects.count(),
        'vendas_recentes': Venda.objects.select_related('cliente__usuario', 'produto')[:5],
    }
    return render(request, 'home.html', context)

# Views de Produtos
@login_required
def produto_lista(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/lista.html', {'produtos': produtos})

@login_required
def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('produto_lista')
        else:
            messages.error(request, 'Erro ao cadastrar produto.')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/form.html', {'form': form, 'titulo': 'Novo Produto'})

@login_required
def produto_edit(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('produto_lista')
        else:
            messages.error(request, 'Erro ao atualizar produto.')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/form.html', {'form': form, 'titulo': 'Editar Produto'})

@login_required
def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('produto_lista')
    return render(request, 'produtos/confirmar_delete.html', {'produto': produto})

# Views de Clientes
@login_required
def cliente_lista(request):
    clientes = Cliente.objects.select_related('usuario').all()
    return render(request, 'clientes/lista.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cliente_lista')
        else:
            messages.error(request, 'Erro ao cadastrar cliente.')
    else:
        form = ClienteForm()
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Novo Cliente'})

@login_required
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('cliente_lista')
        else:
            messages.error(request, 'Erro ao atualizar cliente.')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Editar Cliente'})

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('cliente_lista')
    return render(request, 'clientes/confirmar_delete.html', {'cliente': cliente})

# Views de Vendas
@login_required
def venda_lista(request):
    vendas = Venda.objects.select_related('cliente__usuario', 'produto').all()
    return render(request, 'vendas/lista.html', {'vendas': vendas})

@login_required
def venda_create(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            produto = venda.produto
            if produto.quantidade_estoque >= venda.quantidade:
                produto.quantidade_estoque -= venda.quantidade
                produto.save()
                venda.save()
                messages.success(request, 'Venda registrada com sucesso!')
                return redirect('venda_lista')
            else:
                messages.error(request, f'Estoque insuficiente. Disponível: {produto.quantidade_estoque}')
        else:
            messages.error(request, 'Erro ao registrar venda.')
    else:
        form = VendaForm()
    return render(request, 'vendas/form.html', {'form': form, 'titulo': 'Nova Venda'})

@login_required
def venda_edit(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    if request.method == 'POST':
        form = VendaForm(request.POST, instance=venda)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venda atualizada com sucesso!')
            return redirect('venda_lista')
        else:
            messages.error(request, 'Erro ao atualizar venda.')
    else:
        form = VendaForm(instance=venda)
    return render(request, 'vendas/form.html', {'form': form, 'titulo': 'Editar Venda'})

@login_required
def venda_delete(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    if request.method == 'POST':
        produto = venda.produto
        produto.quantidade_estoque += venda.quantidade
        produto.save()
        venda.delete()
        messages.success(request, 'Venda cancelada com sucesso!')
        return redirect('venda_lista')
    return render(request, 'vendas/confirmar_delete.html', {'venda': venda})

# Página de detalhe do produto (Loja)
def produto_detalhe(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'store/produto_detalhe.html', {'produto': produto})

# Store Views - Loja para clientes
def store_home(request):
    produtos = Produto.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'store/home.html', {'produtos': produtos})

def store_comprar(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        quantidade = int(request.POST.get('quantidade'))
        
        produto = Produto.objects.get(id=produto_id)
        
        if produto.quantidade_estoque >= quantidade:
            # Criar usuário
            username = email.split('@')[0]
            # Garantir username único
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=nome.split()[0] if nome else username,
                password=f"senha{random.randint(1000, 9999)}"
            )
            
            # Criar cliente com CPF único
            cpf_unico = str(random.randint(10000000000, 99999999999))
            
            cliente = Cliente.objects.create(
                usuario=user,
                telefone=telefone,
                endereco=endereco,
                cpf=cpf_unico,
                data_nascimento='2000-01-01'
            )
            
            # Criar venda
            venda = Venda.objects.create(
                cliente=cliente,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=produto.preco,
                status='pago'
            )
            
            # Atualizar estoque
            produto.quantidade_estoque -= quantidade
            produto.save()
            
            messages.success(request, f'Compra realizada com sucesso! Total: R$ {venda.valor_total():.2f}')
        else:
            messages.error(request, f'Estoque insuficiente! Disponível: {produto.quantidade_estoque}')
        
        return redirect('store_home')