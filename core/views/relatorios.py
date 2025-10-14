from fpdf import FPDF
import requests
from django.http import HttpResponse, JsonResponse
from io import BytesIO
from django.contrib.auth.decorators import login_required
from core.models import CadEmpresa, Locacao, EntregaLocacao, Devolucao, ItemDevolucao

def formatar_moeda(valor):
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return "0,00"

    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@login_required(login_url='login')
def imprimir_cotacao(request, locacao_id):
    locacao = Locacao.objects.get(pk=locacao_id)
    pdf_bytes = gerar_cotacao(request, locacao)

    response = HttpResponse(bytes(pdf_bytes), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cotacao.pdf"'
    return response

@login_required(login_url='login')
def gerar_cotacao(request, locacao):
    itens   = locacao.itens.all()
    empresa = CadEmpresa.objects.last()

    endereco = empresa.logradouro + " " + empresa.numero + ", " + empresa.bairro + ", " + empresa.cidade + " - " + empresa.uf

    # Criação do PDF
    class PDF(FPDF):
        def header(self):
            # Cabeçalho do documento
            self.set_fill_color(44, 39, 98)
            self.set_text_color(255, 255, 255)
            self.set_font("Arial", style='B', size=14)
            self.cell(150, 20, "COTAÇÃO DE PREÇO", align='L', fill=True)
            self.cell(40, 20, "LOC-002546145", ln=True, align='L', fill=True)
            self.ln(10)  # Espaçamento após o cabeçalho

        def footer(self):
            # Posição a 15 mm do rodapé
            self.set_y(-30)  # ou ajuste conforme preferir
            self.set_fill_color(44, 39, 98)
            self.set_text_color(255, 255, 255)
            #self.set_draw_color(255, 255, 255)
            self.set_font("Arial", size=8)
            #self.cell(50, 21, "SUA LOGO AQUI", fill=True)
            self.cell(190, 5, f"Empresa: {empresa.razao}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Endereço: {endereco}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Telefone: {empresa.telefone}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Email: {empresa.email}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Data: {locacao.data.strftime('%d/%m/%Y H:m')}", ln=True, align='R', fill=True)

    # Usa a nova classe PDF
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(25, 8, "Solicitante:", border=0, align='L')
    pdf.set_font("Arial", size=10)
    pdf.cell(80, 8, locacao.solicitante, ln=True)
    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(25, 8, "Observação:", border=0, align='L')
    pdf.set_font("Arial", size=10)
    pdf.cell(80, 8, locacao.observacoes, ln=True)
    pdf.ln(10)

    # Dados de Equipamentos
    pdf.set_fill_color(44, 39, 98)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(190, 10, "Informações do(s) Equipamento(s)", ln=True, fill=True)
    pdf.ln(5)

    pdf.set_fill_color(169, 170, 172)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(70, 8, "Produto", border=1, fill=True)
    pdf.cell(30, 8, "Qtd", border=1, fill=True, align='C')
    pdf.cell(40, 8, "Preço Unit.", border=1, fill=True, align='L')
    pdf.cell(10, 8, "Dias", border=1, fill=True, align='L')
    pdf.cell(40, 8, "Preço Total", border=1, ln=True, fill=True, align='L')

    pdf.set_font("Arial", size=10)
    total_geral = 0
    total_qtd = 0

    for item in itens:
        preco_total = item.quantidade * item.preco * locacao.dias
        total_geral += preco_total
        total_qtd += item.quantidade
        pdf.cell(70, 8, f"{item.produto.descricao}", border=1)
        pdf.cell(30, 8, f"{item.quantidade}", border=1, align='C')
        pdf.cell(40, 8, f"R$ {formatar_moeda(item.preco)}", border=1, align='L')
        pdf.cell(10, 8, f"{locacao.dias}", border=1, align='L')
        pdf.cell(40, 8, f"R$ {formatar_moeda(preco_total)}", border=1, ln=True, align='L')

    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(70, 8, "Total Geral:", border=1)
    pdf.cell(30, 8, f"{total_qtd}", border=1, align='C')
    pdf.cell(50, 8, "", border=1)
    pdf.cell(40, 8, f"R$ {formatar_moeda(total_geral)}", border=1, align='L')
    pdf.ln(15)

    # Informações da Locação
    pdf.set_fill_color(44, 39, 98)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(190, 10, "Informações da Locação", ln=True, fill=True)

    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Início: {locacao.inicio.strftime('%d/%m/%Y')}", ln=True, align='L')
    pdf.cell(0, 8, f"Fim: {locacao.fim.strftime('%d/%m/%Y')}", ln=True, align='L')
    pdf.cell(0, 8, f"Forma de Pagamento: {locacao.pagamento}", ln=True, align='L')
    #pdf.cell(0, 8, "Recorrência: ", ln=True, align='L')
    pdf.ln(5)

    pdf.set_fill_color(44, 39, 98)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(190, 10, "Termos e Condições", ln=True, fill=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=7)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 5,
        "Estimativa aproximada, baseado em cima das informações que foram passadas para "+empresa+", "
        "caso necessite de mais material, terá que ser solicitado novo orçamento para saber o novo valor. "
        "O material estará disponível para retirada em nosso depósito em 24HS mediante confirmação e fechamento da locação. "
        "A devolução também deverá ser realizada no nosso depósito. Prazo de locação de 30 dias. "
        "Material sujeito a disponibilidade em estoque. A "+empresa+" é apenas locadora de equipamentos não responsável "
        "por montagem ou projetos de montagem.\n\n"
        "É PROIBIDA A TRANSFERÊNCIA P/ OUTRAS OBRAS E/OU A SUBLOCAÇÃO S/ AUTORIZAÇÃO DA "+empresa+"\n"
        "OBS: DESCONTO CONCEDIDO É VÁLIDO ATÉ DATA DE VENCIMENTO."
    )

    pdf_str_or_bytes = pdf.output(dest='S')
    pdf_bytes = pdf_str_or_bytes.encode('latin1') if isinstance(pdf_str_or_bytes, str) else pdf_str_or_bytes
    return pdf_bytes

@login_required(login_url='login')
def imprimir_espelho(request, locacao_id):
    locacao = Locacao.objects.get(pk=locacao_id)
    pdf_bytes = gerar_espelho(request, locacao)

    response = HttpResponse(bytes(pdf_bytes), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="espelho.pdf"'
    return response

@login_required(login_url='login')
def gerar_espelho(request, locacao):
    cliente = locacao.cliente
    itens   = locacao.itens.all()
    empresa = CadEmpresa.objects.last()

    endereco = empresa.logradouro + " " + empresa.numero + ", " + empresa.bairro + ", " + empresa.cidade + " - " + empresa.uf
    endereco_cliente = cliente.logradouro + " " + cliente.numero + ", " + cliente.bairro + ", " + cliente.cidade + " - " + cliente.uf

    # Criação do PDF
    class PDF(FPDF):
        def header(self):
            # Cabeçalho do documento
            self.set_fill_color(44, 39, 98)
            self.set_text_color(255, 255, 255)
            self.set_font("Arial", style='B', size=14)
            self.cell(135, 20, "ESPELHO DE LOCAÇÃO DE EQUIPAMENTOS", align='L', fill=True)
            self.cell(55, 20, locacao.codigo, ln=True, align='L', fill=True)
            self.ln(5)  # Espaçamento após o cabeçalho

        def footer(self):
            # Posição a 15 mm do rodapé
            self.set_y(-30)  # ou ajuste conforme preferir
            self.set_fill_color(44, 39, 98)
            self.set_text_color(255, 255, 255)
            self.set_draw_color(255, 255, 255)
            self.set_font("Arial", size=8)
            #self.cell(50, 21, "SUA LOGO AQUI", fill=True)
            self.cell(190, 5, f"Empresa: {empresa.razao}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Endereço: {endereco}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Telefone: {empresa.telefone}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Email: {empresa.email}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Data: {locacao.data.strftime('%d/%m/%Y H:m')}", ln=True, align='R', fill=True)

    # Usa a nova classe PDF
    pdf = PDF()
    pdf.add_page()

    # O conteúdo principal permanece igual (exceto cabeçalho e rodapé removidos daqui)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, f"Pelo presente instrumento particular de Contrato de Medição, de um lado a empresa: {cliente.razao},\n"
f"situada á {endereco_cliente}, CNPJ/CPF: {cliente.cnpj_cpf} - neste ato denominada "
f"Locatária, do outro lado a locadora: {empresa.razao}, CNPJ: {empresa.cnpj}, situada à {endereco},"
"denominada Locadora, tem avençado o seguinte que mutuamente aceitam, a saber:"
"\nCláusula Primeira: Medição do Contrato e Pagamento, Parágrafo Primeiro: A Locadora locou à Locatária, os seguintes equipamentos,"
"conforme a tabela abaixo demonstra, bem como o respectivo Pedido de Locação assinado pela Locatária ou por um de seus representantes."
"Nesta tabela estão constando: Itens Locados; Período da Locação; Quantidade; Valor da Locação. O aceite dado pela locadora indica sua"
"concordância com o valor total cobrado."
"Cláusula Segunda: Do prazo."
"Parágrafo Primeiro: O prazo inicia-se com a retirada dos equipamentos da loja da Locadora, e finda-se por ocasião da devolução dos"
"equipamentos para a mesma. Sua prorrogação é automática, conforme acordo entre Locador e Locatária.",ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.set_fill_color(44, 39, 98)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(190, 10, "Informações do Cliente", ln=True, align='L', fill=True)

    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Nome: {cliente}", ln=True, align='L')
    pdf.cell(0, 8, f"E-mail: {cliente.email}", ln=True, align='L')
    pdf.cell(0, 8, f"Telefone: {cliente.telefone}", ln=True, align='L')
    pdf.cell(0, 8, f"Endereço: {cliente.logradouro}", ln=True, align='L')
    pdf.ln(5)

    # Dados de Equipamentos
    pdf.set_fill_color(44, 39, 98)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(190, 10, "Informações do(s) Equipamento(s)", ln=True, fill=True)
    pdf.ln(5)

    pdf.set_fill_color(169, 170, 172)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(80, 8, "Produto", border=1, fill=True)
    pdf.cell(30, 8, "Qtd", border=1, fill=True, align='C')
    pdf.cell(40, 8, "Preço Unit.", border=1, fill=True, align='L')
    pdf.cell(40, 8, "Preço Total", border=1, ln=True, fill=True, align='L')

    pdf.set_font("Arial", size=10)
    total_geral = 0
    total_qtd = 0

    for item in itens:
        preco_total = item.quantidade * item.preco
        total_geral += preco_total
        total_qtd += item.quantidade
        pdf.cell(80, 8, f"{item.produto.descricao}", border=1)
        pdf.cell(30, 8, f"{item.quantidade}", border=1, align='C')
        pdf.cell(40, 8, f"R$ {item.preco:.2f}", border=1, align='L')
        pdf.cell(40, 8, f"R$ {preco_total:.2f}", border=1, ln=True, align='L')

    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(80, 8, "Total Geral:", border=1)
    pdf.cell(30, 8, f"{total_qtd:.2f}", border=1, align='C')
    pdf.cell(40, 8, "", border=1)
    pdf.cell(40, 8, f"R$ {total_geral:.2f}", border=1, align='L')
    pdf.ln(15)

    # Informações da Locação
    pdf.set_fill_color(44, 39, 98)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(190, 10, "Informações da Locação", ln=True, fill=True)

    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Início: {locacao.inicio.strftime('%d/%m/%Y')}", ln=True, align='L')
    pdf.cell(0, 8, f"Fim: {locacao.fim.strftime('%d/%m/%Y')}", ln=True, align='L')
    pdf.cell(0, 8, f"Forma de Pagamento: {locacao.pagamento}", ln=True, align='L')
    #pdf.cell(0, 8, "Recorrência: ", ln=True, align='L')
    pdf.ln(5)

    pdf.set_font("Arial", size=7)
    pdf.set_text_color(0, 0, 0)

    pdf_str_or_bytes = pdf.output(dest='S')
    pdf_bytes = pdf_str_or_bytes.encode('latin1') if isinstance(pdf_str_or_bytes, str) else pdf_str_or_bytes
    return pdf_bytes

@login_required(login_url='login')
def imprimir_cautela_entrega(request, locacao_id):
    locacao = Locacao.objects.get(pk=locacao_id)
    pdf_bytes = gerar_cautela_entrega(request, locacao)

    response = HttpResponse(bytes(pdf_bytes), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cautela_entrega.pdf"'
    return response

@login_required(login_url='login')
def gerar_cautela_entrega(request, locacao):
    cliente          = locacao.cliente
    itens            = EntregaLocacao.objects.filter(locacao=locacao)
    empresa          = CadEmpresa.objects.last()

    data_hora        = EntregaLocacao.objects.filter(locacao=locacao).first().created_at
    codigo           = EntregaLocacao.objects.filter(locacao=locacao).first().codigo if EntregaLocacao.objects.filter(locacao=locacao).exists() else "N/A"

    endereco         = empresa.logradouro + " " + empresa.numero + ", " + empresa.bairro + ", " + empresa.cidade + " - " + empresa.uf
    endereco_cliente = cliente.logradouro + " " + cliente.numero + ", " + cliente.bairro + ", " + cliente.cidade + " - " + cliente.uf

    # Criação do PDF
    class PDF(FPDF):
        def header(self):
            # Cabeçalho do documento
            self.set_fill_color(44, 39, 98)
            self.set_text_color(255, 255, 255)
            self.set_font("Arial", style='B', size=14)
            self.cell(135, 20, "CAUTELA DE ENTREGA", align='L', fill=True)
            self.cell(55, 20, codigo, ln=True, align='L', fill=True)
            self.ln(5)  # Espaçamento após o cabeçalho

        def footer(self):
            # Posição a 15 mm do rodapé
            self.set_y(-30)  # ou ajuste conforme preferir
            self.set_fill_color(44, 39, 98)
            self.set_text_color(255, 255, 255)
            self.set_draw_color(255, 255, 255)
            self.set_font("Arial", size=8)
            #self.cell(50, 21, "SUA LOGO AQUI", fill=True)
            self.cell(190, 5, f"Empresa: {empresa.razao}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Endereço: {endereco}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Telefone: {empresa.telefone}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Email: {empresa.email}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Data: {data_hora.strftime("%d/%m/%Y %H:%M")}", ln=True, align='R', fill=True)

    # Usa a nova classe PDF
    pdf = PDF()
    pdf.add_page()

    # O conteúdo principal permanece igual (exceto cabeçalho e rodapé removidos daqui)
    pdf.set_font("Arial", size=10)
    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.set_fill_color(44, 39, 98)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(190, 10, "Informações do Cliente", ln=True, align='L', fill=True)

    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Nome: {cliente}", ln=True, align='L')
    pdf.cell(0, 8, f"E-mail: {cliente.email}", ln=True, align='L')
    pdf.cell(0, 8, f"Telefone: {cliente.telefone}", ln=True, align='L')
    pdf.cell(0, 8, f"Endereço: {cliente.logradouro}", ln=True, align='L')
    pdf.ln(5)

    # Dados de Equipamentos
    pdf.set_fill_color(44, 39, 98)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(190, 10, "Informações do(s) Equipamento(s)", ln=True, fill=True)
    pdf.ln(5)

    pdf.set_fill_color(169, 170, 172)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(80, 8, "Produto", border=1, fill=True)
    pdf.cell(30, 8, "Qtd", border=1, fill=True, align='C')
    pdf.ln(10)

    for item in itens:
        pdf.cell(80, 8, f"{item.produto.descricao}", border=1)
        pdf.cell(30, 8, f"{item.quantidade}", border=1, align='C')
        pdf.ln(10)

    # Informações da Locação
    pdf.set_fill_color(44, 39, 98)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(190, 10, "Termo de Retirada de Equipamentos", ln=True, fill=True)

    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Declaro que minha conferência da carga, está de acordo com o quantitativo descrito acima.", ln=True, align='L')
    pdf.ln(20)

    pdf.cell(0, 8, f"Manaus, _____\_____________\_____", ln=True, align='C')
    pdf.ln(20)

    pdf.cell(0, 8, "________________________", align='L')
    pdf.cell(0, 8, "________________________", ln=True, align='R')
    pdf.cell(0, 8, f"{item.motorista} (Motorista)", align='L')
    pdf.cell(0, 8, f"{locacao.solicitante} (Responsável)", align='R')
    

    pdf.set_font("Arial", size=7)
    pdf.set_text_color(0, 0, 0)

    pdf_str_or_bytes = pdf.output(dest='S')
    pdf_bytes = pdf_str_or_bytes.encode('latin1') if isinstance(pdf_str_or_bytes, str) else pdf_str_or_bytes
    return pdf_bytes

@login_required(login_url='login')
def imprimir_cautela_devolucao(request, locacao_id):
    locacao = Locacao.objects.get(pk=locacao_id)
    pdf_bytes = gerar_cautela_devolucao(request, locacao)

    response = HttpResponse(bytes(pdf_bytes), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cautela_devolucao.pdf"'
    return response

@login_required(login_url='login')
def gerar_cautela_devolucao(request, locacao):
    cliente     = locacao.cliente
    devolucao   = Devolucao.objects.filter(locacao=locacao)
    empresa     = CadEmpresa.objects.last()
    itens       = ItemDevolucao.objects.filter(devolucao=devolucao.first()) if devolucao.exists() else []

    #codigo = Devolucao.objects.filter(locacao=locacao).first().id if Devolucao.objects.filter(locacao=locacao).exists() else "N/A"

    endereco = empresa.logradouro + " " + empresa.numero + ", " + empresa.bairro + ", " + empresa.cidade + " - " + empresa.uf
    endereco_cliente = cliente.logradouro + " " + cliente.numero + ", " + cliente.bairro + ", " + cliente.cidade + " - " + cliente.uf

    # Criação do PDF
    class PDF(FPDF):
        def header(self):
            # Cabeçalho do documento
            self.set_fill_color(44, 39, 98)
            self.set_text_color(255, 255, 255)
            self.set_font("Arial", style='B', size=14)
            self.cell(135, 20, "CAUTELA DE DEVOLUÇÃO", align='L', fill=True)
            self.cell(55, 20, locacao.codigo, ln=True, align='L', fill=True)
            self.ln(5)  # Espaçamento após o cabeçalho

        def footer(self):
            # Posição a 15 mm do rodapé
            self.set_y(-30)  # ou ajuste conforme preferir
            self.set_fill_color(44, 39, 98)
            self.set_text_color(255, 255, 255)
            self.set_draw_color(255, 255, 255)
            self.set_font("Arial", size=8)
            #self.cell(50, 21, "SUA LOGO AQUI", fill=True)
            self.cell(190, 5, f"Empresa: {empresa.razao}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Endereço: {endereco}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Telefone: {empresa.telefone}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Email: {empresa.email}", ln=True, align='R', fill=True)
            self.cell(190, 5, f"Data: {locacao.data.strftime('%d/%m/%Y H:m')}", ln=True, align='R', fill=True)

    # Usa a nova classe PDF
    pdf = PDF()
    pdf.add_page()

    # O conteúdo principal permanece igual (exceto cabeçalho e rodapé removidos daqui)
    pdf.set_font("Arial", size=10)
    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.set_fill_color(44, 39, 98)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(190, 10, "Informações do Cliente", ln=True, align='L', fill=True)

    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Nome: {cliente}", ln=True, align='L')
    pdf.cell(0, 8, f"E-mail: {cliente.email}", ln=True, align='L')
    pdf.cell(0, 8, f"Telefone: {cliente.telefone}", ln=True, align='L')
    pdf.cell(0, 8, f"Endereço: {cliente.logradouro}", ln=True, align='L')
    pdf.ln(5)

    # Dados de Equipamentos
    pdf.set_fill_color(44, 39, 98)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(190, 10, "Informações do(s) Equipamento(s)", ln=True, fill=True)
    pdf.ln(5)

    pdf.set_fill_color(169, 170, 172)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(80, 8, "Produto", border=1, fill=True)
    pdf.cell(30, 8, "Qtd", border=1, fill=True, align='C')
    pdf.cell(30, 8, "Estado", border=1, fill=True, align='C')
    pdf.cell(30, 8, "Custo (R$)", border=1, fill=True, align='C')
    pdf.ln(10)

    for item in itens:
        pdf.cell(80, 8, f"{item.item_locacao}", border=1)
        pdf.cell(30, 8, f"{item.quantidade}", border=1, align='C')
        pdf.cell(30, 8, f"{item.estado}", border=1, align='C')
        pdf.cell(30, 8, f"{item.custo_adicional}", border=1, align='C')
        pdf.ln(10)

    # Informações da Locação
    pdf.set_fill_color(44, 39, 98)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(190, 2, "", ln=True, fill=True)

    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"ATENÇÃO: No caso de falta de peças na devolução, será cobrada a re-locação da(s) mesma(s) até a devolução.", ln=True, align='L')
    pdf.ln(20)

    pdf.cell(0, 8, f"Manaus, _____\_____________\_____", ln=True, align='C')
    pdf.ln(20)

    pdf.cell(0, 8, "________________________", align='L')
    pdf.cell(0, 8, "________________________", ln=True, align='R')

    pdf.set_font("Arial", size=7)
    pdf.set_text_color(0, 0, 0)

    pdf_str_or_bytes = pdf.output(dest='S')
    pdf_bytes = pdf_str_or_bytes.encode('latin1') if isinstance(pdf_str_or_bytes, str) else pdf_str_or_bytes
    return pdf_bytes

@login_required(login_url='login')
def imprimir_contrato(request, locacao_id):
    locacao = Locacao.objects.get(pk=locacao_id)
    pdf_bytes = gerar_contrato(request, locacao)

    response = HttpResponse(bytes(pdf_bytes), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="contrato.pdf"'
    return response

@login_required(login_url='login')
def gerar_contrato(request, locacao):
    cliente     = locacao.cliente
    devolucao   = Devolucao.objects.filter(locacao=locacao)
    empresa     = CadEmpresa.objects.last()
    itens       = ItemDevolucao.objects.filter(devolucao=devolucao.first()) if devolucao.exists() else []

    endereco = empresa.logradouro + " " + empresa.numero + ", " + empresa.bairro + ", " + empresa.cidade + " - " + empresa.uf
    endereco_cliente = cliente.logradouro + " " + cliente.numero + ", " + cliente.bairro + ", " + cliente.cidade + " - " + cliente.uf

    # Criação do PDF
    class PDF(FPDF):
        def header(self):
            # Cabeçalho do documento
            self.set_fill_color(44, 39, 98)
            self.set_text_color(255, 255, 255)
            self.set_font("Arial", style='B', size=14)
            self.cell(190, 20, "CONTRATO DE LOCAÇÃO DE EQUIPAMENTOS ", align='C', ln=True, fill=True)
            self.ln(5)  # Espaçamento após o cabeçalho

        def footer(self):
            # Posição a 15 mm do rodapé
            self.set_y(-20)  # ou ajuste conforme preferir
            self.set_fill_color(44, 39, 98)
            self.set_text_color(255, 255, 255)
            self.set_draw_color(255, 255, 255)
            self.set_font("Arial", size=8)
            self.cell(190, 5, f"{empresa.razao}", ln=True, align='C', fill=True)
            self.cell(190, 5, f"{endereco}", ln=True, align='C', fill=True)

    # Usa a nova classe PDF
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", size=10)
    
    estilo_paragrafo = 'style="text-align: justify;"'
    estilo_aviso_negrito = 'style="font-weight: bold; text-align: justify;"'
    estilo_aviso_normal = 'style="text-align: justify;"'

    html_contrato = f"""
    <p {estilo_paragrafo}>
        <b>LOCADORA:</b> <b>{empresa.razao}</b>, CNPJ: <b>{empresa.cnpj}</b>, situada à <b>{endereco}</b>, 
        neste ato representada por seu representante legal, doravante denominada LOCADORA.
    </p>

    <p {estilo_paragrafo}>
        LOCATÁRIA: <b>{cliente.razao}</b>, CNPJ/CPF: <b>{cliente.cnpj_cpf}</b>, situada à <b>{endereco_cliente}</b>, 
        neste ato representada por seu representante legal, doravante denominada LOCATÁRIA.
    </p>

    <p {estilo_paragrafo}>
        Pelo presente instrumento particular de contrato de locação de bem móvel (equipamento para construção civil), 
        as partes contratantes têm entre si avençado o seguinte:
    </p>

    <p {estilo_paragrafo}>
        <b>1. DO OBJETO DO CONTRATO:</b> A locadora se compromete a atender a locatária com aluguel de andaimes e 
        equipamentos para a construção civil, <b>OS QUAIS SERÃO QUANTIFICADOS E ESPECIFICADOS NA COTAÇÃO E NO CONTRATO</b>, 
        que será devidamente assinado.
    </p>

    <p {estilo_paragrafo}>
        1.1. A JB ANDAIMES é apenas locadora de equipamentos, não sendo responsável por montagens ou projetos de montagens.
    </p>

    <p {estilo_paragrafo}>
        <b>2. DO INÍCIO E DO PRAZO DA LOCAÇÃO:</b> A locação terá início com a retirada e/ou reserva dos equipamentos no 
        depósito da LOCADORA e seu término com a entrega da última peça locada. A locação e devolução serão realizadas 
        no depósito da LOCADORA mediante agendamento e programação com o setor comercial desta.
    </p>

    <p {estilo_paragrafo}>
        2.1. O prazo da locação é de 30 (trinta) dias, com prorrogação automática e imediata pelo tempo que se fizer necessário, 
        caso haja interesse por parte dos contratantes.
    </p>

    <p {estilo_paragrafo}>
        2.2. A locação obedecerá ao período mínimo de 30 (trinta) dias, sem possibilidade de cobrança proporcional, 
        ainda que haja a devolução antecipada por parte do LOCATÁRIO.
    </p>

    <p {estilo_paragrafo}>
        2.3. Com o vencimento do prazo da locação sem que haja a devolução dos equipamentos locados em até 48 horas, o período 
        locatício será renovado automaticamente e pelo tempo que o LOCATÁRIO permanecer na posse dos bens, acumulando 
        locações mensais a serem cobradas mediante a emissão de <b>RENOVAÇÃO</b> e <b>EXTRATO DE LOCAÇÃO ATUALIZADA</b>.
    </p>

    <p {estilo_paragrafo}>
        <b>3. DA RESPONSABILIDADE DO LOCATÁRIO:</b> O LOCATÁRIO deverá devolver os equipamentos em perfeito estado de 
        conservação e nas mesmas condições de uso que os recebeu do LOCADOR.
    </p>

    <p {estilo_paragrafo}>
        3.1. É expressamente proibido ao LOCATÁRIO soldar, serrar, ou realizar qualquer outro tipo de alteração nos equipamentos, 
        bem como <b>JOGÁ-LOS DE QUALQUER ALTURA NO SOLO</b>, sendo este responsável pela operação, manutenção, montagem e 
        desmontagem de todos os equipamentos locados.
    </p>

    <p {estilo_paragrafo}>
        3.2. No caso de <b>EQUIPAMENTOS ELÉTRICOS</b>, estes deverão ser instalados por profissional habilitado, com a observação 
        de que tais equipamentos devem ser ligados em corrente trifásica, sob pena de danificá-los e pelos danos responder 
        o LOCATÁRIO perante a LOCADORA.
    </p>

    <p {estilo_paragrafo}>
        3.3. A responsabilidade pelas instalações dos equipamentos em desacordo com as especificações técnicas acima mencionadas e/ou 
        por quedas de fase e/ou oscilações de rede interna ou externa de energia, que ocasione queima do motor e/ou do equipamento, 
        é exclusiva do LOCATÁRIO.
    </p>

    <p {estilo_paragrafo}>
        3.4. Em casos de avarias, perdas ou extravio dos equipamentos locados, ainda que ocorra na sublocação, o LOCATÁRIO deverá 
        ressarcir tais peças, nos termos e valores discriminados no <b>REGULAMENTO PARA RESSARCIMENTO PRATICADO PELA LOCADORA</b>, 
        ficando esta autorizada a cobrar, de forma independente, por cada peça avariada, perdida ou extraviada, bem como a emitir 
        boleto para pagamento no valor de cada uma delas.
    </p>

    <p {estilo_paragrafo}>
        3.5. O LOCATÁRIO deve apresentar comprovante de endereço atualizado da empresa responsável pela locação.
    </p>

    <p {estilo_paragrafo}>
        <b>4. DO VALOR DO CONTRATO E DAS PENALIDADES:</b> O presente contrato tem o seu valor total fixado na cotação, 
        para pagamento a vista ou faturado.
    </p>

    <p {estilo_paragrafo}>
        4.1. Em casos de descontos <b>PROMOCIONAIS</b>, estes serão válidos somente até a data do vencimento especificado em boleto bancário.
    </p>

    <p {estilo_paragrafo}>
        4.2. O não pagamento na data acertada ensejará a cobrança de juros de 0,20% ao dia e multa de 2% sobre o valor do débito, 
        ficando a LOCADORA <b>AUTORIZADA a proceder com o registro da dívida nos órgãos de proteção ao crédito e no cartório de protesto</b>, 
        bem como <b>A RETIRAR OS EQUIPAMENTO LOCADOS DE QUALQUER OBRA OU LOCAL ONDE FOREM ENCONTRADOS</b>, 
        inclusive em posse de sublocatários, sem prejuízo do direito de realizar a cobrança por todos os meios legais, 
        inclusive execução imediata, sendo para tanto este instrumento considerado <b>TÍTULO EXECUTIVO EXTRAJUDICIAL</b>.
    </p>

    <p {estilo_paragrafo}>
        4.3. Os honorários advocatícios e as despesas judiciais e extrajudiciais que o locador for obrigado a arcar para a defesa 
        dos seus direitos correrão por conta do LOCATÁRIO, caso seja vencido.
    </p>

    <p {estilo_paragrafo}>
        <b>5. DO USO EXCLUSIVO DAS CERTIÇÕES:</b> As certidões do CREA, como o ART, e a capacidade técnica fornecido pela 
        LOCADORA no ato da contratação dos equipamentos, concede ao LOCATÁRIO a permissão de uso destes por tempo 
        <b>DETERMINADO E EXPRESSO</b> neste contrato, sendo autorizado o uso exclusivamente para validação dos equipamentos 
        pertencentes à LOCADORA, de acordo com o quantitativo exato na cotação vigente.
    </p>

    <p {estilo_paragrafo}>
        5.1. É <b>EXPRESSAMENTE PROIBIDA</b> a utilização das certificações mencionadas nesta cláusula para a contemplação 
        de outros equipamentos que não pertençam à LOCADORA, sob pena de ensejar a rescisão imediata deste contrato de locação 
        e autorizar a LOCADORA a retirar e/ou remover os equipamentos de onde estiverem, ou exigir a imediata devolução, 
        juntamente com efetivação da cobrança de multa ora estipulada no valor equivalente a 100% do valor integral do contrato, 
        sem desconto promocional.
    </p>

    <p {estilo_paragrafo}>
        <b>6. O responsável da obra</b> que assinar o pedido de locação responde <b>SOLIDARIAMENTE</b> com o locatário por 
        todas as infrações ao presente contrato, inclusive pelo pagamento dos aluguéis e danos ocasionados às peças locadas.
    </p>

    <p {estilo_paragrafo}>
        <b>6.</b> O presente <b>CONTRATO</b> poderá ser alterado no seu todo ou em parte, bastando para tanto que haja mútuo 
        entendimento entre as partes, celebrando- se um <b>TERMO ADITIVO</b> que passará a ter os mesmos efeitos do contrato.
    </p>

    <p {estilo_paragrafo}>
        <b>7.</b> Concordam as partes contratantes, que a LOCAODRA poderá usar, em material publicitário, de marketing e 
        divulgação, imagens das obras em que o material locado esteja sendo utilizado.
    </p>

    <p {estilo_paragrafo}>
        <b>8.</b> Obrigam - se as partes, por si e seus sucessores, ao fiel cumprimento de todas as cláusulas e condições 
        do presente <b>CONTRATO</b> e elegem para seu domicilio contratual o foro da cidade de Manaus/AM, com expressa 
        renúncia a qualquer outro, por mais privilegiado que seja.
    </p>

    <p {estilo_paragrafo}>
        E, por estarem justos e acordados, firmam o presente instrumento em 02 (duas) vias de igual teor, na presença das 
        testemunhas que abaixo assinam, para que possa surtir todos os efeitos legais.
    </p>

    <br><br>

    <p><b>ATENÇÃO:</b></p>

    <p {estilo_aviso_normal}>
        1. - Campos para assinatura são obrigatórios em formato legível conforme documento RG;
    </p>

    <p {estilo_aviso_normal}>
        2. - Campos como Locatária em casos de cliente PESSOA JURIDICA deverá ser assinado por representante legal, 
        conforme determinado em contrato social. E em casos de CLIENTES PESSOA FISICA, deverá ser assinado nome 
        completo e número de CPF.
    </p>

    <br><br>

    <p>Manaus, _____\_____________\_____</p>

    <br><br>

    <p>____________________________________________________</p>
    <p>{cliente} (Locatária)</p>

    <br><br>

    <p>____________________________________________________</p>
    <p>{empresa.razao} (Locadora)</p>
    """
    pdf.write_html(html_contrato)

    pdf.set_font("Arial", size=7)
    pdf.set_text_color(0, 0, 0)

    pdf_str_or_bytes = pdf.output(dest='S')
    pdf_bytes = pdf_str_or_bytes.encode('latin1') if isinstance(pdf_str_or_bytes, str) else pdf_str_or_bytes
    return pdf_bytes