from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def filtrar_valor(objs, opcao_valor, valor1, valor2):
    if opcao_valor == 'entre':
        if valor1 and valor2:
            if valor1 > valor2:
                valor1, valor2 = valor2, valor1
            objs = objs.filter(valor__range=(valor1, valor2))
        elif valor1 or valor2:
            objs = objs.filter(valor=valor1 or valor2)

    elif opcao_valor == 'maior':
        if valor1 or valor2:
            objs = objs.filter(valor__gte=(valor1 or valor2))

    elif opcao_valor == 'menor':
        if valor1 or valor2:
            objs = objs.filter(valor__lte=(valor1 or valor2))

    return objs


def paginar(objs, page, n_linhas):
    paginator = Paginator(objs, n_linhas)
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    return objs
