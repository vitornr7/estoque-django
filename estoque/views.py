from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime
from django.utils import formats, timezone
from django.db.models import Sum, F, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import csv

from .models import Estoque, Empresa, Produto
from .utilidades import paginar, filtrar_valor


class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    redirect_field_name = 'estoque:avisos'
    paginate_by = 3

    def get_queryset(self):
        produtos = Produto.objects.all().order_by('nome')

        query = self.request.GET.get('q')
        valor1 = self.request.GET.get('valor1')
        valor2 = self.request.GET.get('valor2')
        opcao_valor = self.request.GET.get('opcao_valor')

        if query:
            produtos = Produto.objects.filter(Q(nome__icontains=query) | Q(codigo__icontains=query)).order_by('nome')
        if produtos:
            produtos = filtrar_valor(produtos, opcao_valor, valor1, valor2)

        return produtos


@login_required
def detalhes_produto(request, pk):
    usuario = get_object_or_404(Empresa, usuario=request.user)

    produto = get_object_or_404(Produto, pk=pk)
    try:
        estoque = Estoque.objects.get(Q(empresa=usuario) & Q(produto=produto))
    except Estoque.DoesNotExist:
        estoque = None

    return render(request, 'estoque/custom/detalhes_produto.html', {'produto': produto, 'estoque': estoque})


@login_required
def avisos(request):
    page1 = request.GET.get('bpage', 1)
    page2 = request.GET.get('apage', 1)

    usuario = get_object_or_404(Empresa, usuario=request.user)
    baixo = Estoque.objects.filter(Q(empresa=usuario) & Q(quantidade__lte=F('baixo_estoque')))
    alto = Estoque.objects.filter(Q(empresa=usuario) & Q(quantidade__gte=F('alto_estoque')))

    baixo = paginar(baixo, page1, 7)
    alto = paginar(alto, page2, 7)

    return render(request, 'estoque/custom/avisos.html', {'baixo': baixo, 'alto': alto})
