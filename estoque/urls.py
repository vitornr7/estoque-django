from django.urls import path

from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.avisos, name='index'),
    path('avisos', views.avisos, name='avisos'),


    # path('listar_produtos/', views.listar_produtos, name='listar_produtos'),
    path('listar_produtos/', views.ProdutoListView.as_view(), name='listar_produtos'),
    # path('cadastrar_produto/', views.ProdutoCreateView.as_view(), name='cadastrar_produto'),
    path('detalhes_produto/<int:pk>', views.detalhes_produto, name='detalhes_produto'),
    # path('alterar_produto/<int:pk>', views.ProdutoUpdateView.as_view(), name='alterar_produto'),


    # path('realizar_venda/<int:pk>', views.realizar_venda, name='realizar_venda'),

    # path('acrescentar_estoque/<int:pk>', views.acrescentar_estoque, name='acrescentar_estoque'),


    # path('relatorio_venda/', views.relatorio_venda, name='relatorio_venda'),
    # path('relatorio_acrescimo/', views.relatorio_acrescimo, name='relatorio_acrescimo'),
    # path('relatorio_produto/<int:pk>', views.relatorio_produto, name='relatorio_produto'),

    # path('cadastrar_filial/', views.cadastar_filial, name='cadastrar_filial'),

    # path('download_csv/<int:pk>', views.gerar_arquivo_csv, name='download_csv'),

]
