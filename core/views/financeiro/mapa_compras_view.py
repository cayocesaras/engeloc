from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Sum, Q
from calendar import monthrange

from core.models import ContasPagar
from core.forms import ContasPagarForm


def _get_fornecedor_nome(conta):
    """Retorna o nome do fornecedor ou 'Sem fornecedor' se não houver."""
    return conta.fornecedor.razao if conta.fornecedor else "Sem fornecedor"


@login_required(login_url='login')
def mapa_compras(request):
    """
    View para exibir o Mapa de Compras - apenas contas a pagar vinculadas a solicitações de compra.
    """
    # Filtra apenas contas que têm solicitação de compra vinculada (independente do status)
    # Usa select_related para otimizar a query e garantir que o relacionamento seja carregado
    contas = ContasPagar.objects.select_related('solicitacao', 'fornecedor', 'centro_custo').filter(solicitacao__isnull=False).order_by('data_vencimento')
    
    if request.method == 'POST':
        # Verifica se é uma requisição para autorizar pagamento
        if 'autorizar_pagamento_id' in request.POST:
            conta_id = request.POST.get('autorizar_pagamento_id')
            try:
                conta = get_object_or_404(ContasPagar, id=conta_id)
                
                # Validações de negócio
                if conta.status == 'pago':
                    messages.warning(request, 'Esta conta já está paga.')
                    return redirect('mapa_compras')
                
                if conta.status == 'cancelado':
                    messages.warning(request, 'Não é possível autorizar pagamento de uma conta cancelada.')
                    return redirect('mapa_compras')
                
                # Define a data de pagamento como hoje
                conta.data_pagamento = timezone.now().date()
                
                # Verifica se há mais de uma parcela
                if conta.quantidade_parcelas > 1:
                    parcela_paga = conta.parcela_atual  # Armazena qual parcela foi paga
                    
                    # Se não é a última parcela, incrementa a parcela atual e mantém pendente
                    if conta.parcela_atual < conta.quantidade_parcelas:
                        conta.parcela_atual += 1
                        conta.status = 'pendente'
                        conta.save()
                        messages.success(
                            request, 
                            f'Pagamento da parcela {parcela_paga}/{conta.quantidade_parcelas} '
                            f'da conta - {_get_fornecedor_nome(conta)} foi autorizado. '
                            f'Próxima parcela: {conta.parcela_atual}/{conta.quantidade_parcelas}'
                        )
                    else:
                        # É a última parcela, marca como pago
                        conta.status = 'pago'
                        conta.save()
                        messages.success(
                            request, 
                            f'Pagamento da última parcela {parcela_paga}/{conta.quantidade_parcelas} '
                            f'da conta - {_get_fornecedor_nome(conta)} foi autorizado. Conta totalmente quitada!'
                        )
                else:
                    # Apenas uma parcela, marca como pago diretamente
                    conta.status = 'pago'
                    conta.save()
                    messages.success(request, f'Pagamento da conta - {_get_fornecedor_nome(conta)} foi autorizado com sucesso!')
                
                return redirect('mapa_compras')
            except Exception as e:
                messages.error(request, f'Erro ao autorizar pagamento: {str(e)}')
                return redirect('mapa_compras')
        # Verifica se é uma requisição para reagendar uma conta
        elif 'reagendar_conta_id' in request.POST:
            conta_id = request.POST.get('reagendar_conta_id')
            try:
                conta = get_object_or_404(ContasPagar, id=conta_id)
                
                # Validações de negócio
                if conta.status == 'cancelado':
                    messages.warning(request, 'Não é possível reagendar uma conta cancelada.')
                    return redirect('mapa_compras')
                
                # Obtém a nova data de vencimento do POST
                nova_data_vencimento = request.POST.get('nova_data_vencimento')
                
                # Valida se a data de vencimento foi fornecida
                if not nova_data_vencimento:
                    messages.error(request, 'Data de vencimento é obrigatória.')
                    return redirect('mapa_compras')
                
                # Tenta fazer o parse da data
                try:
                    data_vencimento = parse_date(nova_data_vencimento)
                    if not data_vencimento:
                        raise ValueError('Formato de data inválido')
                    
                    # Atualiza apenas a data de vencimento
                    conta.data_vencimento = data_vencimento
                    conta.save()
                    
                    messages.success(request, f'Conta - {_get_fornecedor_nome(conta)} foi reagendada com sucesso!')
                    return redirect('mapa_compras')
                    
                except (ValueError, TypeError) as e:
                    messages.error(request, f'Formato de data inválido: {str(e)}')
                    return redirect('mapa_compras')
                    
            except Exception as e:
                messages.error(request, f'Erro ao reagendar conta: {str(e)}')
                return redirect('mapa_compras')
        # Verifica se é uma requisição para baixa do pagamento
        elif 'baixa_pagamento_id' in request.POST:
            conta_id = request.POST.get('baixa_pagamento_id')
            try:
                conta = get_object_or_404(ContasPagar, id=conta_id)
                
                # Validações de negócio
                if conta.status != 'pendente':
                    messages.warning(request, 'Apenas contas pendentes podem ter baixa de pagamento.')
                    return redirect('mapa_compras')
                
                # Verifica se o comprovante foi enviado
                if 'comprovante_baixa' not in request.FILES:
                    messages.error(request, 'É obrigatório enviar o comprovante de pagamento.')
                    return redirect('mapa_compras')
                
                comprovante = request.FILES['comprovante_baixa']
                
                # Salva o comprovante
                conta.comprovante = comprovante
                
                # Define a data de pagamento como hoje
                conta.data_pagamento = timezone.now().date()
                
                # Marca como pago
                conta.status = 'pago'
                conta.save()
                
                # Mensagem de sucesso
                if conta.quantidade_parcelas > 1:
                    messages.success(
                        request, 
                        f'Baixa da parcela {conta.parcela_atual}/{conta.quantidade_parcelas} '
                        f'da conta - {_get_fornecedor_nome(conta)} foi registrada com sucesso!'
                    )
                else:
                    messages.success(request, f'Baixa da conta - {_get_fornecedor_nome(conta)} foi registrada com sucesso!')
                
                return redirect('mapa_compras')
            except Exception as e:
                messages.error(request, f'Erro ao registrar baixa do pagamento: {str(e)}')
                return redirect('mapa_compras')
        # Verifica se é uma requisição para cancelar uma conta
        elif 'cancelar_conta_id' in request.POST:
            conta_id = request.POST.get('cancelar_conta_id')
            try:
                conta = get_object_or_404(ContasPagar, id=conta_id)
                
                # Validações de negócio
                if conta.status == 'cancelado':
                    messages.warning(request, 'Esta conta já está cancelada.')
                    return redirect('mapa_compras')
                
                if conta.status == 'pago':
                    messages.warning(request, 'Não é possível cancelar uma conta já paga.')
                    return redirect('mapa_compras')
                
                # Altera o status para cancelado
                conta.status = 'cancelado'
                conta.save()
                
                messages.success(request, f'Conta - {_get_fornecedor_nome(conta)} foi cancelada com sucesso!')
                return redirect('mapa_compras')
            except Exception as e:
                messages.error(request, f'Erro ao cancelar conta: {str(e)}')
                return redirect('mapa_compras')
        # Verifica se é uma requisição para editar uma conta
        elif 'editar_conta_id' in request.POST:
            conta_id = request.POST.get('editar_conta_id')
            try:
                conta = get_object_or_404(ContasPagar, id=conta_id)
                
                # Validações de negócio
                if conta.status == 'cancelado':
                    messages.warning(request, 'Não é possível editar uma conta cancelada.')
                    return redirect('mapa_compras')
                
                if conta.status == 'pago':
                    messages.warning(request, 'Não é possível editar uma conta já paga.')
                    return redirect('mapa_compras')
                
                # Cria o formulário com os dados da conta e os dados do POST
                form = ContasPagarForm(request.POST, request.FILES, instance=conta)
                
                if form.is_valid():
                    # Mantém a solicitação original (não pode ser alterada)
                    conta_editada = form.save(commit=False)
                    
                    # Garante que a solicitação seja sempre mantida (CRÍTICO - sem isso a conta sai do mapa)
                    if conta.solicitacao:
                        conta_editada.solicitacao = conta.solicitacao
                    else:
                        # Se por algum motivo a solicitação foi perdida, não permite salvar
                        messages.error(request, 'Erro: A solicitação de compra não pode ser removida.')
                        return redirect('mapa_compras')
                    
                    # Garante que o fornecedor seja sempre mantido (não pode ser alterado)
                    if conta.fornecedor:
                        conta_editada.fornecedor = conta.fornecedor
                    
                    # Garante que o valor seja sempre mantido (não pode ser alterado)
                    conta_editada.valor = conta.valor
                    
                    # Garante que o status seja válido - se não foi informado ou está vazio, mantém o original
                    status_informado = request.POST.get('status', '')
                    if not status_informado or status_informado == '':
                        conta_editada.status = conta.status
                    # Se foi informado, usa o informado (permite alterar o status)
                    
                    # Garante que parcela_atual seja mantida se não foi alterada
                    if not conta_editada.parcela_atual:
                        conta_editada.parcela_atual = conta.parcela_atual
                    
                    conta_editada.save()
                    
                    messages.success(request, f'Conta - {_get_fornecedor_nome(conta_editada)} foi editada com sucesso!')
                    return redirect('mapa_compras')
                else:
                    messages.error(request, 'Por favor, corrija os erros no formulário.')
                    # Recria a query para garantir que está atualizada
                    contas_para_template = ContasPagar.objects.select_related('solicitacao', 'fornecedor', 'centro_custo').filter(solicitacao__isnull=False).order_by('data_vencimento')
                    # Retorna para a página com o formulário preenchido
                    return render(request, 'financeiro/mapa_compras.html', {
                        'contas': contas_para_template,
                        'form': form,
                        'conta_editando_id': conta_id,
                        'total_pendentes': contas_para_template.filter(status='pendente').aggregate(total=Sum('valor'))['total'] or 0,
                        'qtd_pendentes': contas_para_template.filter(status='pendente').count(),
                        'total_atrasadas': contas_para_template.filter(status='atrasado').aggregate(total=Sum('valor'))['total'] or 0,
                        'qtd_atrasadas': contas_para_template.filter(status='atrasado').count(),
                        'total_em_aprovacao': contas_para_template.filter(status='em_aprovacao').aggregate(total=Sum('valor'))['total'] or 0,
                        'qtd_em_aprovacao': contas_para_template.filter(status='em_aprovacao').count(),
                    })
                    
            except Exception as e:
                messages.error(request, f'Erro ao editar conta: {str(e)}')
                return redirect('mapa_compras')
    
    # Calcula o somatório das contas pendentes
    contas_pendentes = contas.filter(status='pendente')
    total_pendentes = contas_pendentes.aggregate(total=Sum('valor'))['total'] or 0
    qtd_pendentes = contas_pendentes.count()
    
    # Calcula o somatório das contas atrasadas
    contas_atrasadas = contas.filter(status='atrasado')
    total_atrasadas = contas_atrasadas.aggregate(total=Sum('valor'))['total'] or 0
    qtd_atrasadas = contas_atrasadas.count()
    
    # Calcula o somatório das contas em aprovação
    contas_em_aprovacao = contas.filter(status='em_aprovacao')
    total_em_aprovacao = contas_em_aprovacao.aggregate(total=Sum('valor'))['total'] or 0
    qtd_em_aprovacao = contas_em_aprovacao.count()
    
    # Prepara o formulário para edição se necessário
    form = None
    conta_editando_id = request.GET.get('editar', None)
    if conta_editando_id:
        try:
            conta_editando = get_object_or_404(ContasPagar, id=conta_editando_id)
            form = ContasPagarForm(instance=conta_editando)
        except:
            pass
    
    if not form:
        form = ContasPagarForm()
    
    return render(request, 'financeiro/mapa_compras.html', {
        'contas': contas,
        'form': form,
        'conta_editando_id': conta_editando_id,
        'total_pendentes': total_pendentes,
        'qtd_pendentes': qtd_pendentes,
        'total_atrasadas': total_atrasadas,
        'qtd_atrasadas': qtd_atrasadas,
        'total_em_aprovacao': total_em_aprovacao,
        'qtd_em_aprovacao': qtd_em_aprovacao,
    })

