from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime
from django.db.models import Sum, F, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Estoque, Empresa, Produto, PedidosFilial, VendasFilial, ComprasCentral, Carrinho, CarrinhoProdutos
from .utilidades import paginar, filtrar_valor, converter_data, filtrar_data, get_info
from .forms import ProdutoForm, EstoqueForm, EstoqueAtualizarForm, ComprasCentralForm, VendasFilialForm, PedidosFilialForm, UsuarioForm, FilialForm, ValorCompraCentralForm, CarrinhoProdutosForm
from .gerar_csv import arq_carrinho, arq_compras_central, arq_pedidos, arq_carrinho_produtos


@login_required
def listar_produtos(request):
    produtos = Produto.objects.all().order_by('nome')

    page = request.GET.get('page', 1)
    query = request.GET.get('q')
    valor1 = request.GET.get('valor1')
    valor2 = request.GET.get('valor2')
    opcao_valor = request.GET.get('opcao_valor')

    if valor1:
        valor1 = float(valor1)
    if valor2:
        valor2 = float(valor2)

    if query:
        if query.isdigit():
            produtos = produtos.filter(codigo=query)
        else:
            produtos = produtos.filter(nome__icontains=query)

    if produtos:
        produtos = filtrar_valor(produtos, opcao_valor, valor1, valor2)

    produtos = paginar(produtos, page, 3)

    return render(request, 'estoque/listar_produtos.html', {'produtos': produtos})


@login_required
def atualizar_produto(request, pk):
    if request.user.is_superuser:
        produto = get_object_or_404(Produto, pk=pk)

        form = ProdutoForm(instance=produto)

        if request.method == "POST":
            form = ProdutoForm(data=request.POST, instance=produto)

            if form.is_valid():
                form.save()

                return HttpResponseRedirect(reverse('estoque:detalhes_produto', kwargs={'pk': produto.pk}))

        return render(request, 'estoque/alterar_produto.html', {'form': form, 'produto': produto})

    return render(request, 'estoque/alterar_produto.html')


@login_required
def atualizar_estoque(request, pk):
    usuario = get_object_or_404(Empresa, usuario=request.user)
    produto = get_object_or_404(Produto, pk=pk)

    try:
        estoque = Estoque.objects.get(empresa=usuario, produto=produto)
    except Estoque.DoesNotExist:
        return HttpResponseRedirect(reverse('estoque:detalhes_produto', kwargs={'pk': produto.pk}))

    form = EstoqueAtualizarForm(instance=estoque)

    if request.method == "POST":
        form = EstoqueAtualizarForm(data=request.POST, instance=estoque)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('estoque:detalhes_produto', kwargs={'pk': produto.pk}))

    return render(request, 'estoque/alterar_estoque.html', {'form': form, 'produto': produto})


@login_required
def cadastrar_produto(request):
    if request.user.is_superuser:
        if request.method == "POST":
            empresa = get_object_or_404(Empresa, usuario=request.user)
            produto_form = ProdutoForm(data=request.POST)
            estoque_form = EstoqueForm(data=request.POST)
            valor_compra_form = ValorCompraCentralForm(data=request.POST)

            if produto_form.is_valid() and estoque_form.is_valid() and valor_compra_form:
                produto = produto_form.save()

                estoque = estoque_form.save(commit=False)
                estoque.empresa = empresa
                estoque.produto = produto
                estoque.save()

                if estoque.quantidade > 0:
                    valor_compra = valor_compra_form.save(commit=False)
                    valor_compra.produto = produto
                    valor_compra.quantidade = estoque.quantidade
                    valor_compra.save()

                return HttpResponseRedirect(reverse('estoque:detalhes_produto', kwargs={'pk': produto.pk}))
        else:
            produto_form = ProdutoForm()
            estoque_form = EstoqueForm()
            valor_compra_form = ValorCompraCentralForm()

        return render(request, 'estoque/cadastro_produto.html', {'produto_form': produto_form, 'estoque_form': estoque_form, 'valor_compra_form': valor_compra_form})

    return render(request, 'estoque/cadastro_produto.html')


@login_required
def detalhes_produto(request, pk):
    usuario = get_object_or_404(Empresa, usuario=request.user)

    produto = get_object_or_404(Produto, pk=pk)
    try:
        estoque = Estoque.objects.get(empresa=usuario, produto=produto)
    except Estoque.DoesNotExist:
        estoque = None

    return render(request, 'estoque/detalhes_produto.html', {'produto': produto, 'estoque': estoque})


@login_required
def avisos(request):
    page1 = request.GET.get('bpage', 1)
    page2 = request.GET.get('apage', 1)

    usuario = get_object_or_404(Empresa, usuario=request.user)
    baixo = Estoque.objects.filter(
        Q(empresa=usuario) & Q(quantidade__lte=F('baixo_estoque'))).order_by('quantidade')
    alto = Estoque.objects.filter(
        Q(empresa=usuario) & Q(quantidade__gte=F('alto_estoque'))).order_by('-quantidade')

    baixo = paginar(baixo, page1, 3)
    alto = paginar(alto, page2, 3)

    return render(request, 'estoque/avisos.html', {'baixo': baixo, 'alto': alto})


@login_required
def acrescentar_estoque_central(request, pk):
    form = ComprasCentralForm()
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == "POST":
        form = ComprasCentralForm(data=request.POST)

        if form.is_valid():
            usuario = get_object_or_404(Empresa, usuario=request.user)

            try:
                estoque = Estoque.objects.get(empresa=usuario, produto=produto)
            except Estoque.DoesNotExist:
                return HttpResponseRedirect(reverse('estoque:detalhes_produto', kwargs={'pk': produto.pk}))

            data = form.save(commit=False)
            data.produto = produto
            data.save()

            estoque.quantidade += data.quantidade
            estoque.save()

            return HttpResponseRedirect(reverse('estoque:detalhes_produto', kwargs={'pk': produto.pk}))

    return render(request, 'estoque/alterar_estoque.html', {'form': form, 'produto': produto, 'acrescentar': True})


@login_required
def filial_vender(request, pk):
    if request.user.is_superuser:
        return render(request, 'estoque/filial_vender.html')

    produto = get_object_or_404(Produto, pk=pk)
    empresa = get_object_or_404(Empresa, usuario=request.user)

    try:
        estoque = Estoque.objects.get(empresa=empresa, produto=produto)
    except Estoque.DoesNotExist:
        return HttpResponseRedirect(reverse('estoque:detalhes_produto', kwargs={'pk': produto.pk}))

    form = VendasFilialForm(estoque)

    if request.method == "POST":
        form = VendasFilialForm(estoque, data=request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            data.empresa = empresa
            data.produto = produto

            valor = produto.valor * data.quantidade
            data.valor = valor

            data.save()

            estoque.quantidade -= data.quantidade
            estoque.save()

            return HttpResponseRedirect(reverse('estoque:detalhes_produto', kwargs={'pk': produto.pk}))

    return render(request, 'estoque/filial_vender.html', {'form': form, 'produto': produto})


@login_required
def filial_pedido(request, pk):
    if request.user.is_superuser:
        return render(request, 'estoque/filial_pedido.html')

    form = PedidosFilialForm()
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == "POST":
        form = PedidosFilialForm(data=request.POST)

        if form.is_valid():
            empresa = get_object_or_404(Empresa, usuario=request.user)

            data = form.save(commit=False)
            data.empresa = empresa
            data.produto = produto

            valor = produto.valor * data.quantidade
            data.valor = valor

            data.save()

            return HttpResponseRedirect(reverse('estoque:detalhes_produto', kwargs={'pk': produto.pk}))

    return render(request, 'estoque/filial_pedido.html', {'form': form, 'produto': produto})


@login_required
def listar_pedidos(request):
    page = request.GET.get('page', 1)
    status_pedido = request.GET.get('status_pedido')
    nome_produto = request.GET.get('nome_produto')
    nome_empresa = request.GET.get('nome_empresa')
    d1 = request.GET.get('d1')
    d2 = request.GET.get('d2')
    opcao_data = request.GET.get('opcao_data')
    valor1 = request.GET.get('valor1')
    valor2 = request.GET.get('valor2')
    opcao_valor = request.GET.get('opcao_valor')
    imprimir = request.GET.get('imprimir')

    if valor1:
        valor1 = float(valor1)
    if valor2:
        valor2 = float(valor2)

    valor = qtd = 0
    data1, data2 = converter_data(opcao_data, d1, d2)

    if status_pedido == 'aprovado':
        status_pedido = PedidosFilial.APROVADO
    elif status_pedido == 'reprovado':
        status_pedido = PedidosFilial.REPROVADO
    else:
        status_pedido = PedidosFilial.ABERTO

    if request.user.is_superuser:
        pedidos = PedidosFilial.objects.filter(status=status_pedido)
    else:
        usuario = get_object_or_404(Empresa, usuario=request.user)
        pedidos = PedidosFilial.objects.filter(
            Q(status=status_pedido) & Q(empresa=usuario))

    if nome_produto:
        if nome_produto.isdigit():
            pedidos = pedidos.filter(produto__codigo=nome_produto)
        else:
            pedidos = pedidos.filter(produto__nome__icontains=nome_produto)

    if nome_empresa and request.user.is_superuser:
        pedidos = pedidos.filter(Q(empresa__usuario__username=nome_empresa))

    if pedidos:
        pedidos = filtrar_data(pedidos, opcao_data, data1, data2)
        if pedidos:
            pedidos = filtrar_valor(pedidos, opcao_valor, valor1, valor2)
            if pedidos:
                valor, qtd = get_info(pedidos)

        pedidos = pedidos.order_by('-data')

    info = {
        'valor': valor,
        'qtd': qtd,
        'data1': data1,
        'data2': data2,
    }

    if imprimir:
        return arq_pedidos(pedidos, info, opcao_valor, valor1, valor2, opcao_data, nome_produto, nome_empresa, request.user, status_pedido)

    pedidos = paginar(pedidos, page, 3)

    return render(request, 'estoque/listar_pedidos.html', {'pedidos': pedidos, 'status_pedido': status_pedido, 'info': info})


@login_required
def aprovar_pedido(request, pk):
    if request.user.is_superuser:
        pedido = PedidosFilial.objects.get(pk=pk)

        if pedido.status == PedidosFilial.APROVADO:
            return render(request, 'estoque/aprovar_pedido.html', {'pedido': pedido, 'ja_aprovado': True})

        if request.method == "POST":
            filial = get_object_or_404(Empresa, pk=pedido.empresa.pk)
            central = get_object_or_404(Empresa, usuario=request.user)

            try:
                estoque_central = Estoque.objects.get(
                    empresa=central, produto=pedido.produto)
            except Estoque.DoesNotExist:
                return HttpResponseRedirect(reverse('estoque:listar_pedidos'))

            if pedido.quantidade > estoque_central.quantidade:
                return render(request, 'estoque/aprovar_pedido.html', {'pedido': pedido, 'aprovar': True, 'quantidade_maior': True, 'quantidade': estoque_central.quantidade})

            estoque_filial, criado = Estoque.objects.get_or_create(
                empresa=filial, produto=pedido.produto)

            estoque_central.quantidade -= pedido.quantidade
            estoque_central.save()

            estoque_filial.quantidade += pedido.quantidade
            estoque_filial.save()

            pedido.status = PedidosFilial.APROVADO
            pedido.save()

            return HttpResponseRedirect(reverse('estoque:listar_pedidos'))

        return render(request, 'estoque/aprovar_pedido.html', {'pedido': pedido, 'aprovar': True})

    return render(request, 'estoque/aprovar_pedido.html')


@login_required
def reprovar_pedido(request, pk):
    if request.user.is_superuser:
        pedido = PedidosFilial.objects.get(pk=pk)

        if pedido.status == PedidosFilial.REPROVADO:
            return render(request, 'estoque/aprovar_pedido.html', {'pedido': pedido, 'ja_aprovado': True})

        if request.method == "POST":
            pedido.status = PedidosFilial.REPROVADO
            pedido.save()

            return HttpResponseRedirect(reverse('estoque:listar_pedidos'))

        return render(request, 'estoque/aprovar_pedido.html', {'pedido': pedido, 'aprovar': False})

    return render(request, 'estoque/aprovar_pedido.html')


@login_required
def cadastrar_filial(request):
    if request.user.is_superuser:
        registrado = False

        if request.method == "POST":
            usuario_form = UsuarioForm(data=request.POST)
            filial_form = FilialForm(data=request.POST)

            if usuario_form.is_valid() and filial_form.is_valid():
                usuario = usuario_form.save()
                usuario.set_password(usuario.password)
                usuario.save()

                filial = filial_form.save(commit=False)
                filial.usuario = usuario

                filial.save()

                registrado = True
        else:
            usuario_form = UsuarioForm()
            filial_form = FilialForm()

        return render(request, 'estoque/cadastrar_filial.html', {'usuario_form': usuario_form, 'filial_form': filial_form, 'registrado': registrado})
    return render(request, 'estoque/cadastrar_filial.html')


@login_required
def listar_filiais(request):
    if request.user.is_superuser:
        filiais = Empresa.objects.exclude(usuario__is_superuser=True)

        page = request.GET.get('page', 1)
        usuario = request.GET.get('usuario')
        email = request.GET.get('email')
        endereco = request.GET.get('endereco')

        if usuario:
            filiais = filiais.filter(usuario__username__icontains=usuario)
        if email:
            filiais = filiais.filter(usuario__email__icontains=email)
        if endereco:
            filiais = filiais.filter(Q(endereco__icontains=endereco))

        filiais = paginar(filiais, page, 3)

        return render(request, 'estoque/listar_filiais.html', {'filiais': filiais})
    return render(request, 'estoque/listar_filiais.html')


@login_required
def listar_compras_central(request):
    if request.user.is_superuser:
        page = request.GET.get('page', 1)
        nome_produto = request.GET.get('nome_produto')
        d1 = request.GET.get('d1')
        d2 = request.GET.get('d2')
        opcao_data = request.GET.get('opcao_data')
        valor1 = request.GET.get('valor1')
        valor2 = request.GET.get('valor2')
        opcao_valor = request.GET.get('opcao_valor')
        imprimir = request.GET.get('imprimir')

        if valor1:
            valor1 = float(valor1)
        if valor2:
            valor2 = float(valor2)

        valor = qtd = 0
        data1, data2 = converter_data(opcao_data, d1, d2)

        compras = ComprasCentral.objects.all()

        if nome_produto:
            if nome_produto.isdigit():
                compras = compras.filter(produto__codigo=nome_produto)
            else:
                compras = compras.filter(produto__nome__icontains=nome_produto)

        if compras:
            compras = filtrar_data(compras, opcao_data, data1, data2)
            if compras:
                compras = filtrar_valor(compras, opcao_valor, valor1, valor2)
                if compras:
                    valor, qtd = get_info(compras)

            compras = compras.order_by('-data')

        info = {
            'valor': valor,
            'qtd': qtd,
            'data1': data1,
            'data2': data2,
        }

        if imprimir:
            return arq_compras_central(compras, info, opcao_valor, valor1, valor2, opcao_data, nome_produto)

        compras = paginar(compras, page, 3)

        return render(request, 'estoque/listar_compras_central.html', {'compras': compras, 'info': info})

    return render(request, 'estoque/listar_compras_central.html')


@login_required
def adicionar_ao_carrinho(request, pk):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('estoque:carrinho'))

    produto = get_object_or_404(Produto, pk=pk)
    empresa = get_object_or_404(Empresa, usuario=request.user)

    try:
        estoque = Estoque.objects.get(empresa=empresa, produto=produto)
    except Estoque.DoesNotExist:
        return HttpResponseRedirect(reverse('estoque:detalhes_produto', kwargs={'pk': produto.pk}))

    form = CarrinhoProdutosForm(estoque)

    if request.method == "POST":
        form = CarrinhoProdutosForm(estoque, data=request.POST)

        if form.is_valid():
            carrinho, criado = Carrinho.objects.get_or_create(
                empresa=empresa, status=Carrinho.ABERTO)

            try:
                car_prod = CarrinhoProdutos.objects.get(
                    carrinho=carrinho, produto=produto)
                quantidade = form.cleaned_data['quantidade']

                car_prod.quantidade += quantidade
                car_prod.valor = car_prod.quantidade * produto.valor
                car_prod.save()

                msg = 'Quantidade (' + str(quantidade) + \
                    ') adicionada ao produto ' + produto.nome
                messages.info(request, msg)

                return HttpResponseRedirect(reverse('estoque:carrinho'))
            except CarrinhoProdutos.DoesNotExist:
                pass

            data = form.save(commit=False)
            data.carrinho = carrinho
            data.produto = produto

            data.valor = produto.valor * data.quantidade

            data.save()

            return HttpResponseRedirect(reverse('estoque:carrinho'))

    return render(request, 'estoque/adicionar_carrinho.html', {'form': form, 'produto': produto})


@login_required
def carrinho(request):
    if request.user.is_superuser:
        return render(request, 'estoque/carrinho.html')

    empresa = get_object_or_404(Empresa, usuario=request.user)
    carrinho, criado = Carrinho.objects.get_or_create(
        empresa=empresa, status=Carrinho.ABERTO)

    car_prod = CarrinhoProdutos.objects.filter(carrinho=carrinho)
    total = 0
    if car_prod:
        total = '%.2f' % car_prod.aggregate(Sum('valor'))['valor__sum']

    return render(request, 'estoque/carrinho.html', {'car_prod': car_prod, 'total': total})


@login_required
def alterar_quantidade_carrinho(request, pk):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('estoque:carrinho'))

    produto = get_object_or_404(Produto, pk=pk)
    empresa = get_object_or_404(Empresa, usuario=request.user)

    try:
        estoque = Estoque.objects.get(empresa=empresa, produto=produto)
    except Estoque.DoesNotExist:
        return HttpResponseRedirect(reverse('estoque:detalhes_produto', kwargs={'pk': produto.pk}))

    carrinho = get_object_or_404(
        Carrinho, empresa=empresa, status=Carrinho.ABERTO)
    car_prod = get_object_or_404(
        CarrinhoProdutos, carrinho=carrinho, produto=produto)

    form = CarrinhoProdutosForm(estoque, instance=car_prod)

    if request.method == "POST":
        form = CarrinhoProdutosForm(
            estoque, data=request.POST, instance=car_prod)

        if form.is_valid():
            data = form.save(commit=False)
            data.valor = produto.valor * data.quantidade
            data.save()
            return HttpResponseRedirect(reverse('estoque:carrinho'))

    return render(request, 'estoque/adicionar_carrinho.html', {'form': form, 'produto': produto})


@login_required
def remover_do_carrinho(request, pk):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('estoque:carrinho'))

    empresa = get_object_or_404(Empresa, usuario=request.user)
    carrinho, criado = Carrinho.objects.get_or_create(
        empresa=empresa, status=Carrinho.ABERTO)

    car_prod = CarrinhoProdutos.objects.filter(carrinho=carrinho, produto=pk)
    car_prod.delete()

    return HttpResponseRedirect(reverse('estoque:carrinho'))


@login_required
def finalizar_carrinho(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('estoque:carrinho'))

    empresa = get_object_or_404(Empresa, usuario=request.user)
    carrinho = get_object_or_404(
        Carrinho, empresa=empresa, status=Carrinho.ABERTO)

    car_prod = CarrinhoProdutos.objects.filter(carrinho=carrinho)
    total = 0
    qtd = 0

    if car_prod:
        total = '%.2f' % car_prod.aggregate(Sum('valor'))['valor__sum']
        qtd = car_prod.aggregate(Sum('quantidade'))['quantidade__sum']

        if qtd > 0:
            carrinho.quantidade = qtd
            carrinho.valor = total
            carrinho.data = datetime.now()
            carrinho.status = Carrinho.FECHADO

            for produto in car_prod:
                estoque = get_object_or_404(
                    Estoque, empresa=empresa, produto=produto.produto)

                estoque.quantidade -= produto.quantidade
                estoque.save()

            carrinho.save()

    return HttpResponseRedirect(reverse('estoque:detalhes_carrinho', kwargs={'pk': carrinho.pk}))


@login_required
def detalhes_carrinho(request, pk):
    empresa = get_object_or_404(Empresa, usuario=request.user)

    if request.user.is_superuser:
        carrinho = get_object_or_404(Carrinho, pk=pk)
    else:
        carrinho = get_object_or_404(Carrinho, pk=pk, empresa=empresa)

    if carrinho.status == Carrinho.ABERTO:
        return HttpResponseRedirect(reverse('estoque:carrinho'))

    car_prod = CarrinhoProdutos.objects.filter(carrinho=carrinho)

    return render(request, 'estoque/detalhes_carrinho_finalizado.html', {'carrinho': carrinho, 'car_prod': car_prod})


@login_required
def listar_carrinhos(request):
    page = request.GET.get('page', 1)
    n_carrinho = request.GET.get('n_carrinho')
    nome_empresa = request.GET.get('nome_empresa')
    d1 = request.GET.get('d1')
    d2 = request.GET.get('d2')
    opcao_data = request.GET.get('opcao_data')
    valor1 = request.GET.get('valor1')
    valor2 = request.GET.get('valor2')
    opcao_valor = request.GET.get('opcao_valor')
    imprimir = request.GET.get('imprimir')

    if valor1:
        valor1 = float(valor1)
    if valor2:
        valor2 = float(valor2)

    valor = qtd = 0
    data1, data2 = converter_data(opcao_data, d1, d2)

    empresa = get_object_or_404(Empresa, usuario=request.user)

    if request.user.is_superuser:
        carrinhos = Carrinho.objects.filter(
            status=Carrinho.FECHADO).order_by('-data')
    else:
        carrinhos = Carrinho.objects.filter(
            empresa=empresa, status=Carrinho.FECHADO).order_by('-data')

    if n_carrinho:
        carrinhos = carrinhos.filter(pk=n_carrinho)

    if nome_empresa and request.user.is_superuser:
        carrinhos = carrinhos.filter(
            Q(empresa__usuario__username=nome_empresa))

    if carrinhos:
        carrinhos = filtrar_data(carrinhos, opcao_data, data1, data2)
        if carrinhos:
            carrinhos = filtrar_valor(carrinhos, opcao_valor, valor1, valor2)
            if carrinhos:
                valor, qtd = get_info(carrinhos)

        carrinhos = carrinhos.order_by('-data')

    info = {
        'valor': valor,
        'qtd': qtd,
        'data1': data1,
        'data2': data2,
    }

    if imprimir == 'imprimir_carrinho':
        return arq_carrinho(carrinhos, info, opcao_valor, valor1, valor2, opcao_data, n_carrinho, nome_empresa, request.user)
    elif imprimir == 'imprimir_car_prod':
        produtos = CarrinhoProdutos.objects.all()
        return arq_carrinho_produtos(carrinhos, produtos, info, opcao_valor, valor1, valor2, opcao_data, n_carrinho, nome_empresa, request.user)

    carrinhos = paginar(carrinhos, page, 3)

    return render(request, 'estoque/listar_carrinhos.html', {'carrinhos': carrinhos, 'info': info})


@login_required
def estatisticas(request):
    page = request.GET.get('page', 1)
    nome_empresa = request.GET.get('nome_empresa')
    mes = request.GET.get('mes')
    menos_vendidos = request.GET.get('menos_vendidos')

    empresa = get_object_or_404(Empresa, usuario=request.user)

    # if request.user.is_superuser:
    #     if nome_empresa:
    #         carrinhos = Carrinho.objects.filter(
    #             empresa__usuario__username=nome_empresa, status=Carrinho.FECHADO).order_by('-data')
    #     else:
    #         carrinhos = Carrinho.objects.filter(
    #             status=Carrinho.FECHADO).order_by('-data')
    # else:
    #     carrinhos = Carrinho.objects.filter(
    #         empresa=empresa, status=Carrinho.FECHADO).order_by('-data')

    produtos = CarrinhoProdutos.objects.filter()
    # nome_empresa=F('empresa__usuario__username')
    # teste = produtos.values(prod=F('produto')).aggregate(qtd_vendida=Sum('quantidade')).order_by('-qtd_vendida')
    teste = produtos.values('produto__pk').annotate(qtd=Sum('quantidade'), nomeprod=F('produto__nome')).order_by('-qtd')

    # if mes:
    #     mes = int(mes)
    # else:
    #     mes = 0

    # if mes != 0:
    #     carrinhos = carrinhos.filter(data__month=mes)

    # if carrinhos:
    #     produtos = CarrinhoProdutos.objects.filter(carrinho=carrinhos)
    # else:
    #     produtos = CarrinhoProdutos.objects.all()


    # print('---------------------------------------------------------------------------------')
    # print('---------------------------------------------------------------------------------')
    # # print('chegou')
    # # print(produtos)
    # print('---------------------------------------------------------------------------------')
    # print('---------------------------------------------------------------------------------')


    # if menos_vendidos:
    #     produtos = produtos.values(nome_empresa=F('empresa__usuario__username'), id_prod=F('produto'), nome_prod=F(
    #         'produto__nome')).annotate(qtd_vendida=Sum('quantidade')).order_by('qtd_vendida')
    # else:
    #     produtos = produtos.values(nome_empresa=F('empresa__usuario__username'), id_prod=F('produto'), nome_prod=F(
    #         'produto__nome')).annotate(qtd_vendida=Sum('quantidade')).order_by('-qtd_vendida')

    # produtos = paginar(produtos, page, 3)

    return render(request, 'estoque/estatisticas.html', {'produtos': produtos, 'teste': teste})


# @login_required
# def estatisticas(request):
#     page = request.GET.get('page', 1)
#     nome_empresa = request.GET.get('nome_empresa')
#     mes = request.GET.get('mes')
#     menos_vendidos = request.GET.get('menos_vendidos')

#     if request.user.is_superuser:
#         if nome_empresa:
#             vendas = VendasFilial.objects.all()
#             vendas = vendas.filter(empresa__usuario__username=nome_empresa)
#         else:
#             vendas = VendasFilial.objects.all()
#     else:
#         usuario = get_object_or_404(Empresa, usuario=request.user)
#         vendas = VendasFilial.objects.filter(empresa=usuario)

#     if mes:
#         mes = int(mes)
#     else:
#         mes = 0

#     if mes != 0:
#         vendas = vendas.filter(data__month=mes)

#     if menos_vendidos:
#         vendas = vendas.values(nome_empresa=F('empresa__usuario__username'), id_prod=F('produto'), nome_prod=F(
#             'produto__nome')).annotate(qtd_vendida=Sum('quantidade')).order_by('qtd_vendida')
#     else:
#         vendas = vendas.values(nome_empresa=F('empresa__usuario__username'), id_prod=F('produto'), nome_prod=F(
#             'produto__nome')).annotate(qtd_vendida=Sum('quantidade')).order_by('-qtd_vendida')

#     vendas = paginar(vendas, page, 3)

#     return render(request, 'estoque/estatisticas.html', {'vendas': vendas})
