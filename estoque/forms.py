from django.shortcuts import render, get_object_or_404
from django.forms import Form, ModelForm, ValidationError, HiddenInput, DateField

from .models import Estoque, Produto, ComprasCentral, VendasFilial, Empresa


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


class ComprasCentralForm(ModelForm):
    class Meta():
        model = ComprasCentral
        fields = ['quantidade', 'valor']


class VendasFilialForm(ModelForm):
    class Meta():
        model = VendasFilial
        fields = ['quantidade']

    def __init__(self, estoque, *args, **kwargs):
        self.estoque = estoque
        super().__init__(*args, **kwargs)

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        estoque_qtd = self.estoque.quantidade

        if quantidade > estoque_qtd:
            raise ValidationError("Tentativa de venda com quantidade maior que a disponivel: " + str(estoque_qtd))

        return quantidade
