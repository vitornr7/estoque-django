from django.urls import path

from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.avisos, name='index'),
    path('avisos', views.avisos, name='avisos'),

    path('listar_produtos/', views.listar_produtos, name='listar_produtos'),
    path('detalhes_produto/<int:pk>', views.detalhes_produto, name='detalhes_produto'),
    path('alterar_estoque/<int:pk>', views.atualizar_estoque, name='alterar_estoque'),
    path('listar_pedidos/', views.listar_pedidos, name='listar_pedidos'),

    path('cadastrar_produto/', views.cadastrar_produto, name='cadastrar_produto'),
    path('alterar_produto/<int:pk>', views.atualizar_produto, name='alterar_produto'),

    path('acrescentar_estoque_central/<int:pk>', views.acrescentar_estoque_central, name='acrescentar_estoque_central'),
    path('aprovar_pedido/<int:pk>', views.aprovar_pedido, name='aprovar_pedido'),
    path('reprovar_pedido/<int:pk>', views.reprovar_pedido, name='reprovar_pedido'),
    path('cadastrar_filial/', views.cadastrar_filial, name='cadastrar_filial'),
    path('listar_filiais/', views.listar_filiais, name='listar_filiais'),
    path('listar_vendas/', views.listar_vendas, name='listar_vendas'),

    path('listar_compras_central/', views.listar_compras_central, name='listar_compras_central'),

    path('filial_vender/<int:pk>', views.filial_vender, name='filial_vender'),
    path('filial_pedido/<int:pk>', views.filial_pedido, name='filial_pedido'),

    path('estatisticas', views.estatisticas, name='estatisticas'),
]
