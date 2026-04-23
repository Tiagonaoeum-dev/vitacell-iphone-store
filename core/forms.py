from django import forms
from django.contrib.auth.models import User

class ProdutoForm(forms.ModelForm):
    class Meta:
        from .models import Produto
        model = Produto
        fields = '__all__'
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

class ClienteForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='Nome de usuário')
    first_name = forms.CharField(max_length=30, label='Nome')
    last_name = forms.CharField(max_length=30, label='Sobrenome')
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Senha')
    
    class Meta:
        from .models import Cliente
        model = Cliente
        fields = ['telefone', 'endereco', 'cpf', 'data_nascimento']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('As senhas não coincidem')
        return cleaned_data
    
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        from .models import Cliente
        cliente = super().save(commit=False)
        cliente.usuario = user
        if commit:
            cliente.save()
        return cliente

class VendaForm(forms.ModelForm):
    class Meta:
        from .models import Venda
        model = Venda
        fields = ['cliente', 'produto', 'quantidade', 'status']