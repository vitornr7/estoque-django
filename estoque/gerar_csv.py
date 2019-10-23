import csv

def arq_vendas():
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'


def gerar_arquivo_csv(objs, info, opcao_valor, valor1, valor2, opcao_data, opcao):
    data1 = info['data1']
    data2 = info['data2']
    if data1:
        data1 = formats.date_format(data1, "d/m/Y")
    if data2:
        data2 = formats.date_format(data2, "d/m/Y")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'

    writer = csv.writer(response)

    if opcao == 'venda':
        writer.writerow(['Relatorio', 'Vendas'])
        writer.writerow(['Produto', 'Todos'])
    elif opcao == 'acrescimo':
        writer.writerow(['Relatorio', 'Acrescimos'])
        writer.writerow(['Produto', 'Todos'])
    elif opcao == 'produto_venda':
        nome = objs.first().produto.nome
        writer.writerow(['Relatorio', 'Vendas'])
        writer.writerow(['Produto', nome])
    elif opcao == 'produto_acrescimo':
        nome = objs.first().produto.nome
        writer.writerow(['Relatorio', 'Acrescimos'])
        writer.writerow(['Produto', nome])

    writer.writerow([])


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


    writer.writerow([])

    writer.writerow(['Total Ganho', info['valor']])
    writer.writerow(['Quantidade vendida', info['qtd']])

    writer.writerow([])

    writer.writerow(['Nome', 'Quantidade', 'Total', 'Data', 'Hora'])
    for obj in objs:
        data = formats.date_format(timezone.localtime(obj.data), "d/m/Y")
        hora = formats.date_format(timezone.localtime(obj.data), "H:i")
        writer.writerow([obj.produto.nome, obj.quantidade, obj.valor, data, hora])

    return response
