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
            self.cell(190, 5, f"Data: {locacao.data.strftime('%d/%m/%Y')}", ln=True, align='R', fill=True)

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
        "Estimativa aproximada, baseado em cima das informações que foram passadas para ----nome da empresa----, "
        "caso necessite de mais material, terá que ser solicitado novo orçamento para saber o novo valor. "
        "O material estará disponível para retirada em nosso depósito em 24HS mediante confirmação e fechamento da locação. "
        "A devolução também deverá ser realizada no nosso depósito. Prazo de locação de 30 dias. "
        "Material sujeito a disponibilidade em estoque. A ----nome da empresa---- é apenas locadora de equipamentos não responsável "
        "por montagem ou projetos de montagem.\n\n"
        "É PROIBIDA A TRANSFERÊNCIA P/ OUTRAS OBRAS E/OU A SUBLOCAÇÃO S/ AUTORIZAÇÃO DA ----nome da empresa----\n"
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
    response['Content-Disposition'] = 'inline; filename="cotacao.pdf"'
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
            self.cell(190, 5, f"Data: {locacao.data.strftime('%d/%m/%Y')}", ln=True, align='R', fill=True)

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
    response['Content-Disposition'] = 'inline; filename="cotacao.pdf"'
    return response

@login_required(login_url='login')
def gerar_cautela_entrega(request, locacao):
    cliente = locacao.cliente
    itens   = EntregaLocacao.objects.filter(locacao=locacao)
    empresa = CadEmpresa.objects.last()

    codigo = EntregaLocacao.objects.filter(locacao=locacao).first().codigo if EntregaLocacao.objects.filter(locacao=locacao).exists() else "N/A"

    endereco = empresa.logradouro + " " + empresa.numero + ", " + empresa.bairro + ", " + empresa.cidade + " - " + empresa.uf
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
            self.cell(190, 5, f"Data: {locacao.data.strftime('%d/%m/%Y')}", ln=True, align='R', fill=True)

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
    response['Content-Disposition'] = 'inline; filename="cotacao.pdf"'
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
            self.cell(190, 5, f"Data: {locacao.data.strftime('%d/%m/%Y')}", ln=True, align='R', fill=True)

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
    #pdf.cell(0, 8, f"{item.motorista} (Motorista)", align='L')
    #pdf.cell(0, 8, f"{locacao.solicitante} (Responsável)", align='R')
    

    pdf.set_font("Arial", size=7)
    pdf.set_text_color(0, 0, 0)

    pdf_str_or_bytes = pdf.output(dest='S')
    pdf_bytes = pdf_str_or_bytes.encode('latin1') if isinstance(pdf_str_or_bytes, str) else pdf_str_or_bytes
    return pdf_bytes