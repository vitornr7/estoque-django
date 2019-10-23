import csv
from django.http import HttpResponse
from django.utils import formats, timezone


def arq_vendas(objs, info, opcao_valor, valor1, valor2, opcao_data, nome_produto, nome_empresa, usuario):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'
    writer = csv.writer(response)

    writer.writerow(['Relatorio', 'Vendas'])

    escrever_empresa(writer, nome_empresa, usuario)
    escrever_produto(writer, nome_produto)
    escrever_info(writer, info)
    escrever_data(writer, opcao_data, info['data1'], info['data2'])
    escrever_valor(writer, opcao_valor, valor1, valor2)

    writer.writerow([])

    if usuario.is_superuser:
        writer.writerow(['Produto', 'Quantidade', 'Total', 'Data', 'Hora', 'Empresa'])
        for obj in objs:
            data = formats.date_format(timezone.localtime(obj.data), "d/m/Y")
            hora = formats.date_format(timezone.localtime(obj.data), "H:i")
            writer.writerow([obj.produto.nome, obj.quantidade, obj.valor, data, hora, obj.empresa])
    else:
        writer.writerow(['Produto', 'Quantidade', 'Total', 'Data', 'Hora'])
        for obj in objs:
            data = formats.date_format(timezone.localtime(obj.data), "d/m/Y")
            hora = formats.date_format(timezone.localtime(obj.data), "H:i")
            writer.writerow([obj.produto.nome, obj.quantidade, obj.valor, data, hora])

    return response


def escrever_info(writer, info):
    writer.writerow(['Total Ganho', info['valor']])
    writer.writerow(['Quantidade vendida', info['qtd']])


def escrever_produto(writer, nome_produto):
    if nome_produto:
        writer.writerow(['Produto', nome_produto])
    else:
        writer.writerow(['Produto', 'Todos'])


def escrever_empresa(writer, nome_empresa, usuario):
    if usuario.is_superuser:
        if nome_empresa:
            writer.writerow(['Empresa', nome_empresa])
        else:
            writer.writerow(['Empresa', 'Todas'])
    else:
        writer.writerow(['Empresa', usuario])


def escrever_data(writer, opcao_data, data1, data2):
    if data1:
        data1 = formats.date_format(data1, "d/m/Y")
    if data2:
        data2 = formats.date_format(data2, "d/m/Y")

    if opcao_data == 'entre':
        if data1 and data2:
            writer.writerow(['Datas entre', str(data1) + ' e ' + str(data2) ])
        elif data1 or data2:
            writer.writerow(['Data', data1 or data2])
        else:
            writer.writerow(['Data', 'Tudo'])

    elif opcao_data == 'maior':
        if data1 or data2:
            writer.writerow(['Data maior que', data1 or data2])
        else:
            writer.writerow(['Data', 'Tudo'])

    elif opcao_data == 'menor':
        if data1 or data2:
            writer.writerow(['Data menor que', data1 or data2])
        else:
            writer.writerow(['Data', 'Tudo'])
    else:
        writer.writerow(['Data', 'Tudo'])


def escrever_valor(writer, opcao_valor, valor1, valor2):
    if opcao_valor == 'entre':
        if valor1 and valor2:
            writer.writerow(['Valores entre', str(valor1) + ' e ' + str(valor2) ])
        elif valor1 or valor2:
            writer.writerow(['Valor', valor1 or valor2])
        else:
            writer.writerow(['Valor', 'Tudo'])

    elif opcao_valor == 'maior':
        if valor1 or valor2:
            writer.writerow(['Valor maior que', valor1 or valor2])
        else:
            writer.writerow(['Valor', 'Tudo'])

    elif opcao_valor == 'menor':
        if valor1 or valor2:
            writer.writerow(['Valor menor que', valor1 or valor2])
        else:
            writer.writerow(['Valor', 'Tudo'])
    else:
        writer.writerow(['Valor', 'Tudo'])
