# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required


from core.models import Devolucao, ItemDevolucao, ItensLocacao, ItensEstoque
import json
from core.forms import DevolucaoForm, ItemDevolucaoFormSet
from core.models import Locacao
from collections import defaultdict
from datetime import datetime
from django.utils import timezone

def atualizar_status_item_estoque(item_estoque, estado_devolucao):
    """
    Atualiza o status do item de estoque baseado no estado da devolução.
    
    Args:
        item_estoque: Objeto ItensEstoque
        estado_devolucao: Estado da devolução ('bom', 'danificado', 'inutilizado')
    """
    if not item_estoque:
        return False
        
    if estado_devolucao != 'bom':
        novo_status = 'danificado'
    else:
        novo_status = 'disponivel'

    if item_estoque.status != novo_status:
        item_estoque.status = novo_status
        item_estoque.save()
        print(f"Status do item de estoque {item_estoque.codigo} atualizado de '{item_estoque.status}' para '{novo_status}'")
        return True
    
    return False

@login_required(login_url='login')
def cad_devolucao(request, locacao_id):
    locacao = get_object_or_404(Locacao, id=locacao_id)

    if request.method == 'POST':
        form = DevolucaoForm(request.POST)
        if form.is_valid():
            # Sempre cria uma nova devolução
            devolucao = form.save(commit=False)
            devolucao.locacao = locacao  # Associa a locação
            devolucao.save()

            # Salvar itens vindos do JSON (tanto para devolução nova quanto existente)
            itens_json = request.POST.get('itens_json')
            if itens_json:
                itens = json.loads(itens_json)
                for i in itens:
                    # Verifica se o item já está salvo (tem item_id)
                    if i.get('item_id'):
                        # Item já está salvo, pula para o próximo
                        continue
                        
                    # Item novo, precisa ser salvo
                    item_locacao = ItensLocacao.objects.get(id=i['item_locacao_id'])
                    quantidade = int(i['quantidade'])
                    custo = float(i.get('custo_adicional', 0))

                    # garante que não devolve mais do que o saldo disponível para devolução
                    if quantidade > item_locacao.saldo_disponivel_devolucao():
                        quantidade = item_locacao.saldo_disponivel_devolucao()

                    # Cria o ItemDevolucao
                    # Converte a data do formato JavaScript (pode vir em DD/MM/YYYY ou YYYY-MM-DD)
                    data_devolucao_str = i.get('data_devolucao', timezone.now().date().strftime('%Y-%m-%d'))
                    try:
                        # Tenta primeiro o formato ISO (YYYY-MM-DD)
                        data_devolucao = datetime.strptime(data_devolucao_str, '%Y-%m-%d').date()
                    except ValueError:
                        try:
                            # Se falhar, tenta o formato brasileiro (DD/MM/YYYY)
                            data_devolucao = datetime.strptime(data_devolucao_str, '%d/%m/%Y').date()
                        except ValueError:
                            # Se ambos falharem, usa a data atual
                            data_devolucao = timezone.now().date()
                    
                    # Se há códigos de estoque específicos selecionados e o estado não é "bom", pega o primeiro
                    item_estoque_especifico = None
                    if i.get('codigos_estoque') and i['estado'] != 'bom':
                        try:
                            item_estoque_especifico = ItensEstoque.objects.get(id=i['codigos_estoque'][0])
                        except ItensEstoque.DoesNotExist:
                            pass  # Ignora códigos inválidos
                    
                    item_devolucao = ItemDevolucao.objects.create(
                        devolucao=devolucao,
                        item_locacao=item_locacao,
                        item_estoque=item_estoque_especifico,  # Associa o item de estoque específico
                        quantidade=quantidade,
                        estado=i['estado'],
                        custo_adicional=custo,
                        observacoes=i.get('observacoes', ''),
                        data_devolucao=data_devolucao
                    )
                    
                    # Atualiza o status do item de estoque baseado no estado da devolução
                    if item_estoque_especifico:
                        atualizar_status_item_estoque(item_estoque_especifico, i['estado'])
                    
                    # Processa a foto se foi enviada
                    if i.get('foto_item') and i['estado'] != 'bom':
                        # Busca a foto nos arquivos enviados usando o ID do item de locação
                        foto_key = f'foto_item_{i["item_locacao_id"]}'
                        if foto_key in request.FILES:
                            foto_arquivo = request.FILES[foto_key]
                            item_devolucao.foto_item = foto_arquivo
                            item_devolucao.save()

            #devolucao.atualizar_custos()  # calcula multas / manutenção etc.
            
            # Gera conta a receber para a devolução se houver custos adicionais
            from core.views.views import gerar_conta_a_receber_devolucao
            try:
                gerar_conta_a_receber_devolucao(request, locacao_id, devolucao.id)
            except Exception as e:
                # Se houver erro na geração da conta, não impede o salvamento da devolução
                messages.warning(request, f"Devolução salva, mas houve erro ao gerar conta a receber: {str(e)}")
            
            messages.success(request, "Devolução registrada com sucesso.")
            return redirect("listagem_locacoes")  # ou onde preferir
    else:
        # Pré-preenche o formulário com dados da devolução existente, se houver
        initial_data = {'responsavel': request.user}
        # Busca a última devolução para pré-preencher observações
        ultima_devolucao = locacao.devolucoes.order_by('-created_at').first()
        if ultima_devolucao:
            initial_data.update({
                'observacoes': ultima_devolucao.observacoes
            })
        form = DevolucaoForm(initial=initial_data)

    # Busca todos os itens de estoque que estão locados para esta locação
    itens_estoque_locados = ItensEstoque.objects.filter(
        status='locado'
    ).select_related('produto').order_by('produto__descricao', 'codigo')

    # Prepara os dados dos itens de estoque para JavaScript
    itens_estoque_json = []
    for item in itens_estoque_locados:
        itens_estoque_json.append({
            'id': str(item.id),
            'codigo': item.codigo,
            'numero_serie': item.numero_serie or '',
            'produto_id': str(item.produto.codigo),  # Usa codigo em vez de id
            'produto_descricao': item.produto.descricao
        })

    # Prepara dados dos itens de devolução existentes
    itens_devolucao_json = []
    # Busca itens das devoluções existentes para esta locação
    devolucoes_existentes = locacao.devolucoes.all()
    for devolucao in devolucoes_existentes:
        for item in devolucao.itens.all():
            itens_devolucao_json.append({
                'item_id': str(item.id),  # ID do item confirmado no banco
                'item_locacao_id': str(item.item_locacao.id),
                'produto': item.item_locacao.produto.descricao,
                'quantidade': item.quantidade,
                'estado': item.estado,
                'observacoes': item.observacoes or '',
                'custo_adicional': float(item.custo_adicional),
                'qtd_locada': item.item_locacao.quantidade,
                'saldo': item.item_locacao.saldo_disponivel_devolucao(),
                'codigos_estoque': [str(item.item_estoque.id)] if item.item_estoque else [],
                'foto_item': item.foto_item.name if item.foto_item else None,
                'data_devolucao': item.data_devolucao.strftime('%d/%m/%Y') if item.data_devolucao else None
            })

    # Determina se está editando devolução existente ou criando nova
    editando_devolucao = devolucoes_existentes.exists()
    
    return render(request, "devolucoes.html", {
        "form": form,
        "locacao": locacao,
        "itens_locacao": locacao.itens.all(),  # para listar no modal 
        "itens_estoque_locados": json.dumps(itens_estoque_json),  # para seleção de códigos
        "itens_devolucao_existentes": json.dumps(itens_devolucao_json),  # itens já cadastrados
        "editando_devolucao": editando_devolucao,  # indica se está editando
    })

@login_required(login_url='login')
def listagem_cautela_devolucoes(request):
    cautelas = Devolucao.objects.prefetch_related('itens').all()

    # Verificar se a quantidade de itens devolvidos é igual à quantidade locada
    # Se for menor retorna o status Pendente se não retorna Completa
    for cautela in cautelas:
        for item in cautela.itens.all():
            item.completo = item.quantidade == item.item_locacao.quantidade
            item.status = 'Completa' if item.completo else 'Pendente'

    return render(request, 'listagem_cautela_devolucoes.html', {
        'cautelas': cautelas,
    })