from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from core.domain.financeiro.CentroCusto import CentroCusto
from core.forms import CentroCustoForm


@login_required(login_url='login')
def centro_custo(request):
    centros_custo = CentroCusto.objects.all().order_by('descricao')
    
    if request.method == 'POST':
        # Verifica se é uma requisição para editar
        if 'editar_centro_custo_id' in request.POST:
            centro_custo_id = request.POST.get('editar_centro_custo_id')
            try:
                centro_custo = get_object_or_404(CentroCusto, codigo=centro_custo_id)
                form = CentroCustoForm(request.POST, instance=centro_custo)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Centro de custo atualizado com sucesso!')
                    return redirect('centro_custo')
                else:
                    messages.error(request, 'Por favor, corrija os erros no formulário.')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar centro de custo: {str(e)}')
                return redirect('centro_custo')
        else:
            # Formulário normal para criar um novo centro de custo
            form = CentroCustoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Centro de custo criado com sucesso!')
                return redirect('centro_custo')
            else:
                messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = CentroCustoForm()
    
    return render(request, 'financeiro/centro_custo.html', {
        'centros_custo': centros_custo,
        'form': form,
    })

