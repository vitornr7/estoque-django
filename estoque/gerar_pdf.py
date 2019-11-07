from django.http import HttpResponse
from fpdf import FPDF
from django.utils import formats, timezone
import os


def comprovante_carrinho(carrinho, produtos):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_font('Times', 'B', 20)

    data = formats.date_format(timezone.localtime(carrinho.data), "d/m/Y")
    hora = formats.date_format(timezone.localtime(carrinho.data), "H:i")

    local = carrinho.empresa.endereco
    pk = str(carrinho.pk)
    data = data
    hora = hora
    valor = str(carrinho.valor)
    quantidade = str(carrinho.quantidade)

    titulo = 'Comprovante da compra'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folder = os.path.join(BASE_DIR, 'static')
    logo = folder + '/logo_preto.png'
    pdf.image(logo, x = 10, y = 10, w = 30, h = 30)

    pdf.cell(50, 15, txt = '', border = 0, ln =1)
    pdf.cell(50, 10)
    pdf.cell(pdf.get_string_width(titulo) + 3, 10, titulo, 'B', 0)

    pdf.ln()
    pdf.ln()

    pdf.set_font('Times', '', 16)

    pdf.cell(95, 10, 'Local', 'B', 0)
    pdf.cell(95, 10, local, 'B', 1)

    pdf.cell(95, 10, 'Nº Carrinho', 'B', 0)
    pdf.cell(95, 10, pk, 'B', 1)

    pdf.cell(95, 10, 'Data', 'B', 0)
    pdf.cell(95, 10, data, 'B', 1)

    pdf.cell(95, 10, 'Hora', 'B', 0)
    pdf.cell(95, 10, hora, 'B', 1)

    pdf.cell(95, 10, 'Total', 'B', 0)
    pdf.cell(95, 10, valor, 'B', 1)

    pdf.cell(95,10, 'Quantidade', 'B', 0)
    pdf.cell(95,10, quantidade, 'B', 1)

    pdf.ln()

    pdf.set_font('Times', 'B', 16)
    titulo = 'Produtos comprados'
    pdf.cell(65, 10)
    pdf.cell(pdf.get_string_width(titulo) + 2, 10, titulo, 'B', 1)

    pdf.ln()

    pdf.set_font_size(14)
    pdf.cell(110, 10, 'Produto', 'B', 0)
    pdf.cell(30, 10, 'Quantidade', 'B', 0)
    pdf.cell(50, 10, 'Valor Individual', 'B', 1)

    pdf.set_font('Times', '', 12)
    for produto in produtos:
        pdf.cell(110, 10, produto.produto.nome, 'B', 0)
        pdf.cell(30, 10, str(produto.quantidade), 'B', 0)
        pdf.cell(50, 10, str(produto.valor), 'B', 1)

    pdf = pdf.output(dest='S').encode('latin-1')

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="comprovante.pdf"'

    return response
