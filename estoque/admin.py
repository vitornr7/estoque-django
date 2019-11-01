from django.contrib import admin

from .models import Produto, Empresa, Estoque, PedidosFilial, ComprasCentral, Carrinho, CarrinhoProdutos

admin.site.register(Produto)
admin.site.register(Empresa)
admin.site.register(Estoque)
admin.site.register(PedidosFilial)
admin.site.register(ComprasCentral)
admin.site.register(Carrinho)
admin.site.register(CarrinhoProdutos)
