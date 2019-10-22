from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.db.models import Sum

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


def filtrar_data(objs, opcao_data, data1, data2):
    if opcao_data == 'entre':
        if data1 and data2:
            objs = objs.filter(data__range=[data1, data2])
        elif data1 or data2:
            objs = objs.filter(data__date=data1 or data2)

    elif opcao_data == 'maior':
        if data1 or data2:
            objs = objs.filter(data__gte=(data1 or data2))

    elif opcao_data == 'menor':
        if data1 or data2:
            objs = objs.filter(data__lte=(data1 or data2))

    return objs


def converter_data(opcao_data, d1, d2):
    if  d1 != None and d1 != '':
        data1 = datetime.strptime(d1, "%Y-%m-%d").date()
    else:
        data1 = False

    if d2 != None and d2 != '':
        data2 = datetime.strptime(d2, "%Y-%m-%d").date()
    else:
        data2 = False

    if opcao_data == 'entre':
        if data1 and data2:
            if data1 > data2:
                data1, data2 = data2, data1

    return [data1, data2]


def paginar(objs, page, n_linhas):
    paginator = Paginator(objs, n_linhas)
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    return objs


def get_info(objs):
    valor = '%.2f' % objs.aggregate(Sum('valor'))['valor__sum']
    qtd = objs.aggregate(Sum('quantidade'))['quantidade__sum']

    return [valor, qtd]
