from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from core.models import ContasPagar
import locale

# Configurar locale para português (se disponível)
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    pass


@login_required(login_url='login')
def dashboard_contas_pagar(request):
    """
    Dashboard de Contas a Pagar com filtros por dia, semana e mês.
    """
    # Obter parâmetro de filtro (dia, semana, mes)
    filtro = request.GET.get('filtro', 'dia')
    
    # Definir datas baseado no filtro
    hoje = timezone.now().date()
    
    if filtro == 'dia':
        data_inicio = hoje
        data_fim = hoje
        periodo_label = f"Hoje ({hoje.strftime('%d/%m/%Y')})"
    elif filtro == 'semana':
        # Semana atual (segunda a domingo)
        dias_semana = hoje.weekday()  # 0 = segunda, 6 = domingo
        data_inicio = hoje - timedelta(days=dias_semana)
        data_fim = data_inicio + timedelta(days=6)
        periodo_label = f"Semana ({data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')})"
    else:  # mes
        # Mês atual
        data_inicio = hoje.replace(day=1)
        # Último dia do mês
        if hoje.month == 12:
            data_fim = hoje.replace(day=31)
        else:
            data_fim = hoje.replace(month=hoje.month + 1, day=1) - timedelta(days=1)
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        periodo_label = f"Mês ({meses[hoje.month - 1]}/{hoje.year})"
    
    # Filtrar contas pelo período de vencimento
    contas = ContasPagar.objects.filter(
        data_vencimento__range=[data_inicio, data_fim]
    )
    
    # Estatísticas gerais
    total_contas = contas.count()
    total_valor = contas.aggregate(total=Sum('valor'))['total'] or 0
    
    # Estatísticas por status
    pendentes = contas.filter(status='pendente')
    em_aprovacao = contas.filter(status='em_aprovacao')
    pagas = contas.filter(status='pago')
    atrasadas = contas.filter(status='atrasado')
    canceladas = contas.filter(status='cancelado')
    
    stats_status = {
        'pendentes': {
            'quantidade': pendentes.count(),
            'valor': pendentes.aggregate(total=Sum('valor'))['total'] or 0
        },
        'em_aprovacao': {
            'quantidade': em_aprovacao.count(),
            'valor': em_aprovacao.aggregate(total=Sum('valor'))['total'] or 0
        },
        'pagas': {
            'quantidade': pagas.count(),
            'valor': pagas.aggregate(total=Sum('valor'))['total'] or 0
        },
        'atrasadas': {
            'quantidade': atrasadas.count(),
            'valor': atrasadas.aggregate(total=Sum('valor'))['total'] or 0
        },
        'canceladas': {
            'quantidade': canceladas.count(),
            'valor': canceladas.aggregate(total=Sum('valor'))['total'] or 0
        }
    }
    
    # Estatísticas por forma de pagamento
    formas_pagamento = {}
    for forma, label in ContasPagar.FORMA_PAGAMENTO_CHOICES:
        contas_forma = contas.filter(forma_pagamento=forma)
        formas_pagamento[label] = {
            'quantidade': contas_forma.count(),
            'valor': contas_forma.aggregate(total=Sum('valor'))['total'] or 0
        }
    
    # Top 5 fornecedores por valor
    top_fornecedores = contas.values('fornecedor__razao').annotate(
        total=Sum('valor'),
        quantidade=Count('id')
    ).order_by('-total')[:5]
    
    # Contas vencendo hoje
    contas_vencendo_hoje = contas.filter(data_vencimento=hoje).count()
    valor_vencendo_hoje = contas.filter(data_vencimento=hoje).aggregate(total=Sum('valor'))['total'] or 0
    
    # Contas vencidas (antes de hoje)
    contas_vencidas = contas.filter(data_vencimento__lt=hoje, status__in=['pendente', 'em_aprovacao']).count()
    valor_vencidas = contas.filter(data_vencimento__lt=hoje, status__in=['pendente', 'em_aprovacao']).aggregate(total=Sum('valor'))['total'] or 0
    
    # Distribuição por centro de custo
    centros_custo = contas.values('centro_custo__descricao').annotate(
        total=Sum('valor'),
        quantidade=Count('id')
    ).order_by('-total')[:10]
    
    context = {
        'filtro': filtro,
        'periodo_label': periodo_label,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'total_contas': total_contas,
        'total_valor': total_valor,
        'stats_status': stats_status,
        'formas_pagamento': formas_pagamento,
        'top_fornecedores': top_fornecedores,
        'contas_vencendo_hoje': contas_vencendo_hoje,
        'valor_vencendo_hoje': valor_vencendo_hoje,
        'contas_vencidas': contas_vencidas,
        'valor_vencidas': valor_vencidas,
        'centros_custo': centros_custo,
    }
    
    return render(request, 'financeiro/dashboard_contas_pagar.html', context)

