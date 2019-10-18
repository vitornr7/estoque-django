from django.contrib import admin

from .models import Produto, Empresa, Estoque, Vendas, PedidosFilial, ComprasCentral

admin.site.register(Produto)
admin.site.register(Empresa)
admin.site.register(Estoque)
admin.site.register(Vendas)
admin.site.register(PedidosFilial)
admin.site.register(ComprasCentral)
