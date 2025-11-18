from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Sum

from core.models import ContasPagar


def _get_fornecedor_nome(conta):
    """Retorna o nome do fornecedor ou 'Sem fornecedor' se não houver."""
    return conta.fornecedor.razao if conta.fornecedor else "Sem fornecedor"


@login_required(login_url='login')
def aprovacao_titulos_a_pagar(request):
    """
    View para aprovação de contas a pagar.
    Exibe apenas contas com status 'em_aprovacao'.
    """
    # Filtra apenas contas em aprovação
    contas = ContasPagar.objects.filter(status='em_aprovacao').order_by('data_vencimento')
    
    if request.method == 'POST':
        # Verifica se é uma requisição para autorizar pagamento em lote
        if 'autorizar_pagamento_ids' in request.POST:
            conta_ids = request.POST.getlist('autorizar_pagamento_ids')
            contas_autorizadas = []
            contas_erro = []
            
            for conta_id in conta_ids:
                try:
                    conta = get_object_or_404(ContasPagar, id=conta_id)
                    
                    # Validações de negócio
                    if conta.status != 'em_aprovacao':
                        contas_erro.append(f'Conta ID {conta_id} não está em aprovação')
                        continue
                    
                    # Marca como aprovado e muda status para pendente
                    conta.aprovado = True
                    conta.status = 'pendente'
                    conta.save()
                    
                    contas_autorizadas.append(_get_fornecedor_nome(conta))
                except Exception as e:
                    contas_erro.append(f'Erro ao autorizar conta ID {conta_id}: {str(e)}')
            
            # Mensagens de feedback
            if contas_autorizadas:
                if len(contas_autorizadas) == 1:
                    messages.success(request, f'Pagamento da conta - {contas_autorizadas[0]} foi autorizado com sucesso!')
                else:
                    messages.success(request, f'{len(contas_autorizadas)} pagamentos foram autorizados com sucesso!')
            
            if contas_erro:
                for erro in contas_erro:
                    messages.warning(request, erro)
            
            return redirect('aprovacao_titulos_a_pagar')
        # Verifica se é uma requisição para autorizar pagamento individual
        elif 'autorizar_pagamento_id' in request.POST:
            conta_id = request.POST.get('autorizar_pagamento_id')
            try:
                conta = get_object_or_404(ContasPagar, id=conta_id)
                
                # Validações de negócio
                if conta.status != 'em_aprovacao':
                    messages.warning(request, 'Esta conta não está em aprovação.')
                    return redirect('aprovacao_titulos_a_pagar')
                
                # Marca como aprovado e muda status para pendente
                conta.aprovado = True
                conta.status = 'pendente'
                conta.save()
                
                messages.success(request, f'Pagamento da conta - {_get_fornecedor_nome(conta)} foi autorizado com sucesso!')
                return redirect('aprovacao_titulos_a_pagar')
            except Exception as e:
                messages.error(request, f'Erro ao autorizar pagamento: {str(e)}')
                return redirect('aprovacao_titulos_a_pagar')
        # Verifica se é uma requisição para reagendar uma conta
        elif 'reagendar_conta_id' in request.POST:
            conta_id = request.POST.get('reagendar_conta_id')
            try:
                conta = get_object_or_404(ContasPagar, id=conta_id)
                
                # Validações de negócio
                if conta.status == 'cancelado':
                    messages.warning(request, 'Não é possível reagendar uma conta cancelada.')
                    return redirect('aprovacao_titulos_a_pagar')
                
                # Obtém a nova data de vencimento do POST
                nova_data_vencimento = request.POST.get('nova_data_vencimento')
                
                # Valida se a data de vencimento foi fornecida
                if not nova_data_vencimento:
                    messages.error(request, 'Data de vencimento é obrigatória.')
                    return redirect('aprovacao_titulos_a_pagar')
                
                # Tenta fazer o parse da data
                try:
                    data_vencimento = parse_date(nova_data_vencimento)
                    if not data_vencimento:
                        raise ValueError('Formato de data inválido')
                    
                    # Atualiza apenas a data de vencimento
                    conta.data_vencimento = data_vencimento
                    conta.save()
                    
                    messages.success(request, f'Conta - {_get_fornecedor_nome(conta)} foi reagendada com sucesso!')
                    return redirect('aprovacao_titulos_a_pagar')
                    
                except (ValueError, TypeError) as e:
                    messages.error(request, f'Formato de data inválido: {str(e)}')
                    return redirect('aprovacao_titulos_a_pagar')
                    
            except Exception as e:
                messages.error(request, f'Erro ao reagendar conta: {str(e)}')
                return redirect('aprovacao_titulos_a_pagar')
        # Verifica se é uma requisição para cancelar uma conta
        elif 'cancelar_conta_id' in request.POST:
            conta_id = request.POST.get('cancelar_conta_id')
            try:
                conta = get_object_or_404(ContasPagar, id=conta_id)
                
                # Validações de negócio
                if conta.status == 'cancelado':
                    messages.warning(request, 'Esta conta já está cancelada.')
                    return redirect('aprovacao_titulos_a_pagar')
                
                if conta.status == 'pago':
                    messages.warning(request, 'Não é possível cancelar uma conta já paga.')
                    return redirect('aprovacao_titulos_a_pagar')
                
                # Altera o status para cancelado
                conta.status = 'cancelado'
                conta.save()
                
                messages.success(request, f'Conta - {_get_fornecedor_nome(conta)} foi cancelada com sucesso!')
                return redirect('aprovacao_titulos_a_pagar')
            except Exception as e:
                messages.error(request, f'Erro ao cancelar conta: {str(e)}')
                return redirect('aprovacao_titulos_a_pagar')
    
    # Calcula o somatório das contas em aprovação
    total_em_aprovacao = contas.aggregate(total=Sum('valor'))['total'] or 0
    qtd_em_aprovacao = contas.count()
    
    return render(request, 'financeiro/aprovacao_titulos_a_pagar.html', {
        'contas': contas,
        'total_em_aprovacao': total_em_aprovacao,
        'qtd_em_aprovacao': qtd_em_aprovacao,
    })

