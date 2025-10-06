# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required


from core.models import Devolucao, ItemDevolucao, ItensLocacao
import json
from core.forms import DevolucaoForm, ItemDevolucaoFormSet
from core.models import Locacao
from collections import defaultdict

@login_required(login_url='login')
def cad_devolucao(request, locacao_id):
    locacao = get_object_or_404(Locacao, id=locacao_id)

    if request.method == 'POST':
        form = DevolucaoForm(request.POST)
        if form.is_valid():
            devolucao = form.save(commit=False)
            devolucao.locacao = locacao
            devolucao.save()

            # Salvar itens vindos do JSON
            itens_json = request.POST.get('itens_json')
            if itens_json:
                itens = json.loads(itens_json)
                for i in itens:
                    item_locacao = ItensLocacao.objects.get(id=i['item_locacao_id'])
                    quantidade = int(i['quantidade'])
                    custo = float(i.get('custo_adicional', 0))

                    # garante que não devolve mais do que o saldo
                    if quantidade > item_locacao.saldo():
                        quantidade = item_locacao.saldo()

                    ItemDevolucao.objects.create(
                        devolucao=devolucao,
                        item_locacao=item_locacao,
                        quantidade=quantidade,
                        estado=i['estado'],
                        custo_adicional=custo,
                        observacoes=i.get('observacoes', '')
                    )

            #devolucao.atualizar_custos()  # calcula multas / manutenção etc.
            messages.success(request, "Devolução registrada com sucesso.")
            return redirect("listagem_locacoes")  # ou onde preferir
    else:
        form = DevolucaoForm(initial={'responsavel': request.user, 'locacao': locacao})

    return render(request, "devolucoes.html", {
        "form": form,
        "locacao": locacao,
        "itens_locacao": locacao.itens.all(),  # para listar no modal
    })

@login_required(login_url='login')
def listagem_cautela_devolucoes(request):
    cautelas = Devolucao.objects.all()

    return render(request, 'listagem_cautela_devolucoes.html', {
        'cautelas': cautelas
    })