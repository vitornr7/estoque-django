from django.forms import Form, ModelForm, ValidationError, HiddenInput, DateField

from .models import Estoque, Produto


class ProdutoForm(ModelForm):
    class Meta():
        model = Produto
        fields = ['nome', 'codigo', 'valor']


class EstoqueForm(ModelForm):
    class Meta():
        model = Estoque
        fields = ['quantidade', 'baixo_estoque', 'alto_estoque']


class EstoqueAtualizarForm(ModelForm):
    class Meta():
        model = Estoque
        fields = ['baixo_estoque', 'alto_estoque']
