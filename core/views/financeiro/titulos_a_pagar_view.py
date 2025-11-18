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
def titulos_a_pagar(request):
    # Verifica se foi solicitado o filtro de mapa de compras
    if request.GET.get('mapa_compras') == '1':
        # Filtra por forma de pagamento NF e vencimento no mês atual
        hoje = timezone.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        
        # Calcula o último dia do mês usando calendar
        ultimo_dia = monthrange(hoje.year, hoje.month)[1]
        ultimo_dia_mes = hoje.replace(day=ultimo_dia)
        
        contas = ContasPagar.objects.filter(
            forma_pagamento='nf',
            data_vencimento__gte=primeiro_dia_mes,
            data_vencimento__lte=ultimo_dia_mes
        ).order_by('data_vencimento')
    else:
        contas = ContasPagar.objects.all().order_by('data_vencimento')
    
    if request.method == 'POST':
        # Verifica se é uma requisição para autorizar pagamento
        if 'autorizar_pagamento_id' in request.POST:
            conta_id = request.POST.get('autorizar_pagamento_id')
            try:
                conta = get_object_or_404(ContasPagar, id=conta_id)
                
                # Validações de negócio
                if conta.status == 'pago':
                    messages.warning(request, 'Esta conta já está paga.')
                    return redirect('titulos_a_pagar')
                
                if conta.status == 'cancelado':
                    messages.warning(request, 'Não é possível autorizar pagamento de uma conta cancelada.')
                    return redirect('titulos_a_pagar')
                
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
                
                return redirect('titulos_a_pagar')
            except Exception as e:
                messages.error(request, f'Erro ao autorizar pagamento: {str(e)}')
                return redirect('titulos_a_pagar')
        # Verifica se é uma requisição para reagendar uma conta
        elif 'reagendar_conta_id' in request.POST:
            conta_id = request.POST.get('reagendar_conta_id')
            try:
                conta = get_object_or_404(ContasPagar, id=conta_id)
                
                # Validações de negócio
                if conta.status == 'cancelado':
                    messages.warning(request, 'Não é possível reagendar uma conta cancelada.')
                    return redirect('titulos_a_pagar')
                
                # Obtém a nova data de vencimento do POST
                nova_data_vencimento = request.POST.get('nova_data_vencimento')
                
                # Valida se a data de vencimento foi fornecida
                if not nova_data_vencimento:
                    messages.error(request, 'Data de vencimento é obrigatória.')
                    return redirect('titulos_a_pagar')
                
                # Tenta fazer o parse da data
                try:
                    data_vencimento = parse_date(nova_data_vencimento)
                    if not data_vencimento:
                        raise ValueError('Formato de data inválido')
                    
                    # Atualiza apenas a data de vencimento
                    conta.data_vencimento = data_vencimento
                    conta.save()
                    
                    messages.success(request, f'Conta - {_get_fornecedor_nome(conta)} foi reagendada com sucesso!')
                    return redirect('titulos_a_pagar')
                    
                except (ValueError, TypeError) as e:
                    messages.error(request, f'Formato de data inválido: {str(e)}')
                    return redirect('titulos_a_pagar')
                    
            except Exception as e:
                messages.error(request, f'Erro ao reagendar conta: {str(e)}')
                return redirect('titulos_a_pagar')
        # Verifica se é uma requisição para baixa do pagamento
        elif 'baixa_pagamento_id' in request.POST:
            conta_id = request.POST.get('baixa_pagamento_id')
            try:
                conta = get_object_or_404(ContasPagar, id=conta_id)
                
                # Validações de negócio
                if conta.status != 'pendente':
                    messages.warning(request, 'Apenas contas pendentes podem ter baixa de pagamento.')
                    return redirect('titulos_a_pagar')
                
                # Verifica se o comprovante foi enviado
                if 'comprovante_baixa' not in request.FILES:
                    messages.error(request, 'É obrigatório enviar o comprovante de pagamento.')
                    return redirect('titulos_a_pagar')
                
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
                
                return redirect('titulos_a_pagar')
            except Exception as e:
                messages.error(request, f'Erro ao registrar baixa do pagamento: {str(e)}')
                return redirect('titulos_a_pagar')
        # Verifica se é uma requisição para cancelar uma conta
        elif 'cancelar_conta_id' in request.POST:
            conta_id = request.POST.get('cancelar_conta_id')
            try:
                conta = get_object_or_404(ContasPagar, id=conta_id)
                
                # Validações de negócio
                if conta.status == 'cancelado':
                    messages.warning(request, 'Esta conta já está cancelada.')
                    return redirect('titulos_a_pagar')
                
                if conta.status == 'pago':
                    messages.warning(request, 'Não é possível cancelar uma conta já paga.')
                    return redirect('titulos_a_pagar')
                
                # Altera o status para cancelado
                conta.status = 'cancelado'
                conta.save()
                
                messages.success(request, f'Conta - {_get_fornecedor_nome(conta)} foi cancelada com sucesso!')
                return redirect('titulos_a_pagar')
            except Exception as e:
                messages.error(request, f'Erro ao cancelar conta: {str(e)}')
                return redirect('titulos_a_pagar')
        else:
            # Formulário normal para criar uma nova conta
            form = ContasPagarForm(request.POST, request.FILES)
            if form.is_valid():
                conta = form.save()
                # Define o status como "em_aprovacao" ao criar uma nova conta
                conta.status = 'em_aprovacao'
                conta.save()
                messages.success(request, 'Conta a pagar criada com sucesso!')
                return redirect('titulos_a_pagar')
            else:
                messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = ContasPagarForm()
    
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
    
    return render(request, 'financeiro/titulos_a_pagar.html', {
        'contas': contas,
        'form': form,
        'total_pendentes': total_pendentes,
        'qtd_pendentes': qtd_pendentes,
        'total_atrasadas': total_atrasadas,
        'qtd_atrasadas': qtd_atrasadas,
        'total_em_aprovacao': total_em_aprovacao,
        'qtd_em_aprovacao': qtd_em_aprovacao,
    })