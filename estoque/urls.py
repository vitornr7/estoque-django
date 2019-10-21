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

    path('filial_vender/<int:pk>', views.filial_vender, name='filial_vender'),
    path('filial_pedido/<int:pk>', views.filial_pedido, name='filial_pedido'),


    # path('acrescentar_estoque/<int:pk>', views.acrescentar_estoque, name='acrescentar_estoque'),


    # path('relatorio_venda/', views.relatorio_venda, name='relatorio_venda'),
    # path('relatorio_acrescimo/', views.relatorio_acrescimo, name='relatorio_acrescimo'),
    # path('relatorio_produto/<int:pk>', views.relatorio_produto, name='relatorio_produto'),

    # path('cadastrar_filial/', views.cadastar_filial, name='cadastrar_filial'),

    # path('download_csv/<int:pk>', views.gerar_arquivo_csv, name='download_csv'),

]
