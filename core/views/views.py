from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.utils import timezone
from django.http import JsonResponse, Http404
from core.models import *
from core.forms import *

from django.contrib.auth import login
import json
from django.shortcuts import render, redirect
from uuid import uuid4
from datetime import timedelta
from django.shortcuts import get_object_or_404

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redireciona para a tela com o menu e DataTable
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    
    return render(request, 'login.html')

@login_required(login_url='login')
def aprovar_manutencoes(request):
    manutencoes  = Manutencao.objects.filter(status="pendente")
    return render(request, 'manutencao/aprovar_manutencoes.html', {'manutencoes': manutencoes})

@login_required(login_url='login')
def locacoes(request):
    return render(request, 'locacoes.html') 

@login_required(login_url='login')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('login')

def buscar_empresa(request):
    codigo = request.GET.get('codigo', None)
    if codigo:
        try:
            empresa = CadEmpresa.objects.get(codigo=codigo)
            data = {
                'codigo': empresa.codigo,
                'cnpj': empresa.cnpj,
                'razao': empresa.razao,
                'uf': empresa.uf,
                'cidade': empresa.cidade,
                'email': empresa.email,
                'fantasia': empresa.fantasia,
                'estadual': empresa.estadual,
                'municipal': empresa.municipal,
                'suframa': empresa.suframa,
                'cep': empresa.cep,
                'logradouro': empresa.logradouro,
                'numero': empresa.numero,
                'complemento': empresa.complemento,
                'bairro': empresa.bairro,
                'telefone': empresa.telefone,
            }
            return JsonResponse({'success': True, 'empresa': data})
        except CadEmpresa.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Empresa não encontrada.'})
    return JsonResponse({'success': False, 'message': 'Código não informado.'})

@login_required(login_url='login')
def list_empresas(request):
    empresas  = CadEmpresa.objects.all()
    return render(request, 'empresas.html', {'empresas': empresas})

@login_required(login_url='login')
def listagem_locacoes(request):
    locacoes  = Locacao.objects.filter(status = 'aprovada')
    return render(request, 'listagem_locacoes.html', {'locacoes': locacoes})

@login_required(login_url='login')
def listagem_clientes(request):
    clientes  = CadCliente.objects.all()
    return render(request, 'listagem_clientes.html', {'clientes': clientes})    

@login_required(login_url='login')
def cad_empresa(request):
    empresas            = CadEmpresa.objects.all()
    form                = CadEmpresaForm()
    muda_acao           = "incluir"
    codigo              = ""

    if request.method == 'POST':
        acao    = request.POST.get("Acao")
        codigo  = request.POST.get('id')

        if acao == "incluir":
            form = CadEmpresaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('empresas')

        elif acao == "visualizar":
                empresa         = CadEmpresa.objects.get(codigo=codigo)
                form            = CadEmpresaForm(instance=empresa)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "visualizar" # Indica para o template que a ação é alterar

        elif acao == "alterar_form":
            try:
                empresa         = CadEmpresa.objects.get(codigo=codigo)
                form            = CadEmpresaForm(instance=empresa)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "alterar" # Indica para o template que a ação é alterar
            except CadEmpresa.DoesNotExist:
                form.add_error(None, 'Empresa não encontrada para alteração.')

        elif acao == "alterar":
            try:
                empresa = CadEmpresa.objects.get(codigo=codigo)
                form = CadEmpresaForm(request.POST, instance=empresa)
                if form.is_valid():
                    form.save()
                    return redirect('empresas')
                else:
                    print("Formulário inválido:", form.errors)
            except CadEmpresa.DoesNotExist:
                form.add_error(None, 'Empresa não encontrada para alteração.')

        elif acao == "excluir":
            try:
                empresa = CadEmpresa.objects.get(codigo=codigo)
                empresa.delete()
                return redirect('empresas')
            except CadEmpresa.DoesNotExist:
                form.add_error(None, 'Empresa não encontrada para exclusão.')

    context = {
        'form': form,
        'empresas': empresas,
        'muda_acao': muda_acao,
        'codigo': codigo,
    }
    return render(request, 'empresas.html', context)

@login_required(login_url='login')
def cad_cliente(request):
    clientes            = CadCliente.objects.all()
    form                = CadClienteForm()
    muda_acao           = "incluir"
    codigo              = ""

    if request.method == 'POST':
        acao    = request.POST.get("Acao")
        codigo  = request.POST.get('id')

        if acao == "incluir":
            form = CadClienteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('clientes')

        elif acao == "visualizar":
                cliente         = CadCliente.objects.get(codigo=codigo)
                form            = CadClienteForm(instance=cliente)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "visualizar" # Indica para o template que a ação é alterar

        elif acao == "alterar_form":
            try:
                cliente         = CadCliente.objects.get(codigo=codigo)
                form            = CadClienteForm(instance=cliente)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "alterar" # Indica para o template que a ação é alterar
            except CadCliente.DoesNotExist:
                form.add_error(None, 'Cliente não encontrado para alteração.')

        elif acao == "alterar":
            try:
                cliente = CadCliente.objects.get(codigo=codigo)
                form = CadClienteForm(request.POST, instance=cliente)
                if form.is_valid():
                    form.save()
                    return redirect('clientes')
            except CadCliente.DoesNotExist:
                form.add_error(None, 'Cliente não encontrado para alteração.')

        elif acao == "excluir":
            try:
                cliente = CadCliente.objects.get(codigo=codigo)
                cliente.delete()
                return redirect('clientes')
            except CadCliente.DoesNotExist:
                form.add_error(None, 'Cliente não encontrado para exclusão.')

    context = {
        'form': form,
        'clientes': clientes,
        'muda_acao': muda_acao,
        'codigo': codigo,
    }
    return render(request, 'clientes.html', context)

@login_required(login_url='login')
def cad_fornecedor(request):
    fornecedores        = CadFornecedor.objects.all()
    form                = CadFornecedorForm()
    muda_acao           = "incluir"
    codigo              = ""

    if request.method == 'POST':
        acao    = request.POST.get("Acao")
        codigo  = request.POST.get('id')

        if acao == "incluir":
            form = CadFornecedorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('fornecedores')

        elif acao == "visualizar":
                cliente         = CadFornecedor.objects.get(codigo=codigo)
                form            = CadFornecedorForm(instance=cliente)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "visualizar" # Indica para o template que a ação é alterar

        elif acao == "alterar_form":
            try:
                cliente         = CadFornecedor.objects.get(codigo=codigo)
                form            = CadFornecedorForm(instance=cliente)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "alterar" # Indica para o template que a ação é alterar
            except CadFornecedor.DoesNotExist:
                form.add_error(None, 'Fornecedor não encontrado para alteração.')

        elif acao == "alterar":
            try:
                cliente = CadFornecedor.objects.get(codigo=codigo)
                form = CadFornecedorForm(request.POST, instance=cliente)
                if form.is_valid():
                    form.save()
                    return redirect('fornecedores')
            except CadFornecedor.DoesNotExist:
                form.add_error(None, 'Fornecedor não encontrado para alteração.')

        elif acao == "excluir":
            try:
                cliente = CadFornecedor.objects.get(codigo=codigo)
                cliente.delete()
                return redirect('fornecedores')
            except CadFornecedor.DoesNotExist:
                form.add_error(None, 'Fornecedor não encontrado para exclusão.')

    context = {
        'form': form,
        'fornecedores': fornecedores,
        'muda_acao': muda_acao,
        'codigo': codigo,
    }
    return render(request, 'fornecedores.html', context)

@login_required(login_url='login')
def cad_grupo_produto(request):
    grupo_produtos      = CadGrupoProduto.objects.all()
    form                = CadGrupoProdutoForm()
    muda_acao           = "incluir"
    codigo              = ""

    if request.method == 'POST':
        acao    = request.POST.get("Acao")
        codigo  = request.POST.get('id')

        if acao == "incluir":
            form = CadGrupoProdutoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('grupo_produtos')

        elif acao == "visualizar":
                cliente         = CadGrupoProduto.objects.get(codigo=codigo)
                form            = CadGrupoProdutoForm(instance=cliente)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "visualizar" # Indica para o template que a ação é alterar

        elif acao == "alterar_form":
            try:
                cliente         = CadGrupoProduto.objects.get(codigo=codigo)
                form            = CadGrupoProdutoForm(instance=cliente)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "alterar" # Indica para o template que a ação é alterar
            except CadGrupoProduto.DoesNotExist:
                form.add_error(None, 'Grupo não encontrado para alteração.')

        elif acao == "alterar":
            try:
                cliente = CadGrupoProduto.objects.get(codigo=codigo)
                form = CadGrupoProdutoForm(request.POST, instance=cliente)
                if form.is_valid():
                    form.save()
                    return redirect('grupo_produtos')
            except CadGrupoProduto.DoesNotExist:
                form.add_error(None, 'Grupo não encontrado para alteração.')

        elif acao == "excluir":
            try:
                grupo_produto = CadGrupoProduto.objects.get(codigo=codigo)
                grupo_produto.delete()
                return redirect('grupo_produtos')
            except CadGrupoProduto.DoesNotExist:
                form.add_error(None, 'Grupo não encontrado para exclusão.')

    context = {
        'form': form,
        'grupo_produtos': grupo_produtos,
        'muda_acao': muda_acao,
        'codigo': codigo,
    }
    return render(request, 'grupo_produtos.html', context)

@login_required(login_url='login')
def cad_item(request):
    itens               = CadItem.objects.all()
    form                = CadItemForm()
    muda_acao           = "incluir"
    codigo              = ""

    if request.method == 'POST':
        acao    = request.POST.get("Acao")
        codigo  = request.POST.get('id')

        if acao == "incluir":
            form = CadItemForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('itens_compra')

        elif acao == "visualizar":
                item            = CadItem.objects.get(codigo=codigo)
                form            = CadItemForm(instance=item)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "visualizar" # Indica para o template que a ação é alterar

        elif acao == "alterar_form":
            try:
                item            = CadItem.objects.get(codigo=codigo)
                form            = CadItemForm(instance=item)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "alterar" # Indica para o template que a ação é alterar
            except CadItem.DoesNotExist:
                form.add_error(None, 'Item não encontrado para alteração.')

        elif acao == "alterar":
            try:
                item = CadItem.objects.get(codigo=codigo)
                form = CadItemForm(request.POST, instance=item)
                if form.is_valid():
                    form.save()
                    return redirect('itens_compra')
            except CadItem.DoesNotExist:
                form.add_error(None, 'Item não encontrado para alteração.')

        elif acao == "excluir":
            try:
                item = CadItem.objects.get(codigo=codigo)
                item.delete()
                return redirect('itens_compra')
            except CadItem.DoesNotExist:
                form.add_error(None, 'Item não encontrado para exclusão.')

    context = {
        'form': form,
        'itens': itens,
        'muda_acao': muda_acao,
        'codigo': codigo,
    }
    return render(request, 'itens_compra.html', context)

@login_required(login_url='login')
def listagem_itens(request):
    itens               = CadItem.objects.all()

    context = {
        'itens': itens,
    }
    return render(request, 'listagem_itens.html', context)

@login_required(login_url='login')
def cad_unidade_medida(request):
    unidade_medida      = CadUnidadeMedida.objects.all()
    form                = CadUnidadeMedidaForm()
    muda_acao           = "incluir"
    codigo              = ""

    if request.method == 'POST':
        acao    = request.POST.get("Acao")
        codigo  = request.POST.get('id')

        if acao == "incluir":
            form = CadUnidadeMedidaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('unidade_medida')

        elif acao == "visualizar":
                unidade         = CadUnidadeMedida.objects.get(codigo=codigo)
                form            = CadUnidadeMedidaForm(instance=unidade)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "visualizar" # Indica para o template que a ação é alterar

        elif acao == "alterar_form":
            try:
                unidade         = CadUnidadeMedida.objects.get(codigo=codigo)
                form            = CadUnidadeMedidaForm(instance=unidade)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "alterar" # Indica para o template que a ação é alterar
            except CadUnidadeMedida.DoesNotExist:
                form.add_error(None, 'Unidade de Medida não encontrada para alteração.')

        elif acao == "alterar":
            try:
                unidade = CadUnidadeMedida.objects.get(codigo=codigo)
                form = CadUnidadeMedidaForm(request.POST, instance=unidade)
                if form.is_valid():
                    form.save()
                    return redirect('unidade_medida')
            except CadUnidadeMedida.DoesNotExist:
                form.add_error(None, 'Unidade de Medida não encontrada para alteração.')

        elif acao == "excluir":
            try:
                grupo_produto = CadUnidadeMedida.objects.get(codigo=codigo)
                grupo_produto.delete()
                return redirect('unidade_medida')
            except CadUnidadeMedida.DoesNotExist:
                form.add_error(None, 'Unidade de Medida não encontrada para exclusão.')

    context = {
        'form': form,
        'unidade_medida': unidade_medida,
        'muda_acao': muda_acao,
        'codigo': codigo,
    }
    return render(request, 'unidade_medida.html', context)

#import cloudinary.uploader

@login_required(login_url='login')
def cad_produto(request):
    produtos            = CadProduto.objects.all()
    form                = CadProdutoForm()
    muda_acao           = "incluir"
    codigo              = ""

    if request.method == 'POST':
        acao    = request.POST.get("Acao")
        codigo  = request.POST.get('id')

        if acao == "incluir":
            form = CadProdutoForm(request.POST, request.FILES)
            if form.is_valid():
                produto = form.save(commit=False)
                produto.save()
                return redirect('produtos')
            else:
                print(form.errors)

        elif acao == "visualizar":
                produto         = CadProduto.objects.get(codigo=codigo)
                form            = CadProdutoForm(instance=produto)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "visualizar" # Indica para o template que a ação é alterar

        elif acao == "alterar_form":
            try:
                produto         = CadProduto.objects.get(codigo=codigo)
                form            = CadProdutoForm(instance=produto)  # Pré-preenche o formulário com os dados do cliente
                muda_acao       = "alterar" # Indica para o template que a ação é alterar
            except CadProduto.DoesNotExist:
                form.add_error(None, 'Produto não encontrado para alteração.')

        elif acao == "alterar":
            try:
                produto = CadProduto.objects.get(codigo=codigo)
                form = CadProdutoForm(request.POST, request.FILES, instance=produto)
                if form.is_valid():
                    produto = form.save(commit=False)

                    #if request.FILES.get('foto'):
                    #    upload_result = cloudinary.uploader.upload(request.FILES['foto'])
                    #    produto.foto = upload_result.get('secure_url')

                    produto.save()
                    return redirect('produtos')
            except CadProduto.DoesNotExist:
                form.add_error(None, 'Produto não encontrado para alteração.')

        elif acao == "excluir":
            try:
                produtos = CadProduto.objects.get(codigo=codigo)
                produtos.delete()
                return redirect('produtos')
            except CadProduto.DoesNotExist:
                form.add_error(None, 'Produto não encontrado para exclusão.')

    context = {
        'form': form,
        'produtos': produtos,
        'muda_acao': muda_acao,
        'codigo': codigo,
    }
    return render(request, 'produtos.html', context)

@login_required(login_url='login')
def listagem_produtos(request):
    produtos            = CadProduto.objects.all()

    context = {
        'produtos': produtos,
    }
    return render(request, 'listagem_produtos.html', context)

from collections import defaultdict

@login_required(login_url='login')
def listagem_cautela_entregas(request):
    entregas = EntregaLocacao.objects.select_related('locacao', 'produto').order_by('-created_at')

    # Agrupar por código
    cautelas = defaultdict(list)
    for entrega in entregas:
        cautelas[entrega.codigo].append(entrega)

    # Transforma em lista de tuplas (codigo, entregas)
    context = {
        'cautelas': cautelas.items()
    }
    return render(request, 'listagem_cautela_entregas.html', context)

from django.contrib import messages

@login_required(login_url='login')
def excluir_cautela(request, codigo):
    if request.method == "POST":
        # Apaga todas as entregas da cautela
        EntregaLocacao.objects.filter(codigo=codigo).delete()
        messages.success(request, f"Cautela {codigo} excluída com sucesso.")
        return redirect('listagem_cautela_entregas')

    # Se vier por GET, pode exibir um confirm simples ou só redirecionar
    return redirect('listagem_cautela_entregas')


@login_required(login_url='login')
def list_clientes(request):
    clientes  = CadCliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})   

@login_required(login_url='login')
def cad_solicitacao(request):
    muda_acao = "incluir"
    codigo = ""

    # Configuração do formset (ligando os itens à solicitação)
    ItemFormSet = inlineformset_factory(
        SolicitacaoCompra,
        ItensSolicitacaoCompra,
        form=ItensSolicitacaoCompraForm,
        extra=1,
        can_delete=True
    )

    acao = request.POST.get('Acao') if request.method == 'POST' else None

    # --- Incluir ---
    if acao == 'incluir':
        form = SolicitacaoCompraForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.solicitante = request.user
            solicitacao.save()

            formset = ItemFormSet(request.POST, instance=solicitacao)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Solicitação incluída com sucesso.")
                return redirect('cad_solicitacao')
            else:
                solicitacao.delete()  # rollback se itens inválidos
                messages.error(request, "Erro ao salvar os itens da solicitação.")
        else:
            formset = ItemFormSet(request.POST)  # manter dados no erro

    # --- Alterar ---
    elif acao == 'alterar':
        solicitacao = get_object_or_404(SolicitacaoCompra, id=request.POST.get('id'))
        form = SolicitacaoCompraForm(request.POST, instance=solicitacao)
        formset = ItemFormSet(request.POST, instance=solicitacao)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Solicitação alterada com sucesso.")
            return redirect('cad_solicitacao')

    # --- Excluir ---
    elif acao == 'excluir':
        solicitacao = get_object_or_404(SolicitacaoCompra, id=request.POST.get('id'))
        solicitacao.delete()
        messages.success(request, "Solicitação excluída com sucesso.")
        return redirect('cad_solicitacao')

    # --- Visualizar / Edição ---
    elif acao in ['visualizar', 'editar']:
        muda_acao = "alterar" if acao == 'editar' else "visualizar"
        solicitacao = get_object_or_404(SolicitacaoCompra, id=request.POST.get('id'))
        form = SolicitacaoCompraForm(instance=solicitacao)
        formset = ItemFormSet(instance=solicitacao)
        codigo = solicitacao.id

    # --- Acesso inicial (GET) ---
    else:
        form = SolicitacaoCompraForm()
        formset = ItemFormSet()

    solicitacoes = SolicitacaoCompra.objects.all()

    return render(request, 'solicitacoes.html', {
        'form': form,
        'formset': formset,
        'solicitacoes': solicitacoes,
        'muda_acao': muda_acao,
        'codigo': codigo
    })

@login_required(login_url='login')
def aprovar_compra(request):
    solicitacoes    = SolicitacaoCompra.objects.filter(status='em_aberto')  # Filtra apenas as solicitações pendentes
    form            = SolicitacaoCompraForm()
    muda_acao       = "incluir"
    codigo          = ""
    
    if request.method == 'POST':
        acao = request.POST.get("Acao")
        codigo = request.POST.get('id')

        if acao == "incluir":
            form = SolicitacaoCompraForm(request.POST)
            if form.is_valid():
                form.instance.solicitante = request.user
                form.save()
                return redirect('aprovar_compra')  # Substitua 'solicitações' pela URL da sua lista de solicitações
            else:
                print(form.errors)

        elif acao == "visualizar":
            solicitacao     = SolicitacaoCompra.objects.get(codigo=codigo)
            form            = SolicitacaoCompraForm(instance=solicitacao)  # Pré-preenche o formulário com os dados da solicitação
            muda_acao       = "visualizar"  # Indica para o template que a ação é visualizar

        elif acao == "alterar_form":
            try:
                solicitacao     = SolicitacaoCompra.objects.get(codigo=codigo)
                form            = SolicitacaoCompraForm(instance=solicitacao)  # Pré-preenche o formulário com os dados da solicitação
                muda_acao       = "alterar"  # Indica para o template que a ação é alterar
            except solicitacao.DoesNotExist:
                form.add_error(None, 'Solicitação não encontrada para alteração.')

        elif acao == "alterar":
            try:
                solicitacao     = SolicitacaoCompra.objects.get(codigo=codigo)
                form            = SolicitacaoCompraForm(request.POST, instance=solicitacao)
                if form.is_valid():
                    form.save()
                    return redirect('aprovar_compra')  # Substitua 'solicitações' pela URL da sua lista de solicitações
            except solicitacao.DoesNotExist:
                form.add_error(None, 'Solicitação não encontrada para alteração.')

        elif acao == "excluir":
            try:
                solicitacao = SolicitacaoCompra.objects.get(codigo=codigo)
                solicitacao.delete()
                return redirect('aprovar_compra')  # Substitua 'solicitações' pela URL da sua lista de solicitações
            except solicitacao.DoesNotExist:
                form.add_error(None, 'Solicitação não encontrada para exclusão.')

    context = {
        'form': form,
        'solicitacoes': solicitacoes,
        'muda_acao': muda_acao,
        'codigo': codigo,
    }
    return render(request, 'aprovar_compra.html', context)

def aprovar_solicitacao(request, solicitacao_id):
    try:
        solicitacao = SolicitacaoCompra.objects.get(id=solicitacao_id)
        itens_processados = []
        itens_sem_relacao = []

        for item in solicitacao.itens.all():
            # verifica relação com produto de estoque
            relacao = RelacaoItemProduto.objects.filter(item=item.produto).first()

            if relacao:
                # cria os itens no estoque conforme quantidade
                criar_itens_estoque(relacao.produto, item.quantidade)
                itens_processados.append(item.produto.descricao)
            else:
                itens_sem_relacao.append(item.produto.descricao)

        # aprova a solicitação
        solicitacao.status = 'aprovada'
        solicitacao.save()

        gerar_contas_pagar(solicitacao)

        # feedback
        if itens_processados:
            messages.success(
                request,
                f"Solicitação aprovada. Itens adicionados ao estoque: {', '.join(itens_processados)}"
            )
        if itens_sem_relacao:
            messages.warning(
                request,
                f"Solicitação aprovada, mas estes itens não estão vinculados ao estoque: {', '.join(itens_sem_relacao)}"
            )

    except SolicitacaoCompra.DoesNotExist:
        messages.error(request, "Solicitação não encontrada.")

    return redirect('aprovar_compra')

def recusar_solicitacao(request, solicitacao_id):
    try:
        solicitacao = SolicitacaoCompra.objects.get(id=solicitacao_id)
        solicitacao.status = 'recusada'
        solicitacao.save()
        messages.success(request, 'Solicitação recusada com sucesso.')
    except SolicitacaoCompra.DoesNotExist:
        messages.error(request, 'Solicitação não encontrada.')

    return redirect('aprovar_compra')

def gerar_contas_pagar(solicitacao):
    # Garante que só vai gerar se ainda não houver uma conta existente (opcional)
    if hasattr(solicitacao, 'contapagar'):
        return  # Evita duplicidade
    
    ContasPagar.objects.create(
        solicitacao=solicitacao,
        fornecedor=solicitacao.fornecedor,
        descricao=f'Solicitação #{solicitacao.codigo} - {solicitacao.justificativa[:100]}',
        valor=solicitacao.valor_total,
        data_emissao=solicitacao.data_solicitacao,
        data_vencimento=solicitacao.data_solicitacao + timedelta(days=30),
        status='pendente'
    )

    return redirect('titulos_a_pagar')

@login_required(login_url='login')
def movimentacoes(request):
    movimentacoes   = Movimentacoes.objects.filter(tipo__in=['entrada', 'saida', 'devolucao'])
    form            = MovimentacoesForm()
    muda_acao       = "incluir"
    codigo          = ""

    if request.method == 'POST':
        acao = request.POST.get("Acao")
        codigo = request.POST.get('id')

        if acao == "incluir":
            produto_id = request.POST.get('produto')
            produto_obj = CadProduto.objects.get(pk=produto_id)
            quantidade = int(request.POST.get('quantidade', 0))
            form = MovimentacoesForm(request.POST)
            if form.is_valid():
                criar_itens_estoque(produto_obj, quantidade)
                form.save()
                return redirect('movimentacoes')  # Substitua 'solicitações' pela URL da sua lista de solicitações
            else:
                print(form.errors)

        elif acao == "visualizar":
            movimentacao    = Movimentacoes.objects.get(codigo=codigo)
            form            = MovimentacoesForm(instance=movimentacao)  # Pré-preenche o formulário com os dados da solicitação
            muda_acao       = "visualizar"  # Indica para o template que a ação é visualizar

        elif acao == "alterar_form":
            try:
                movimentacao    = Movimentacoes.objects.get(codigo=codigo)
                form            = MovimentacoesForm(instance=movimentacao)  # Pré-preenche o formulário com os dados da solicitação
                muda_acao       = "alterar"  # Indica para o template que a ação é alterar
            except movimentacao.DoesNotExist:
                form.add_error(None, 'Movimentação não encontrada para alteração.')

        elif acao == "alterar":
            try:
                movimentacao     = Movimentacoes.objects.get(codigo=codigo)
                form            = MovimentacoesForm(request.POST, instance=movimentacao)
                if form.is_valid():
                    form.save()
                    return redirect('movimentacoes')  # Substitua 'solicitações' pela URL da sua lista de solicitações
            except movimentacao.DoesNotExist:
                form.add_error(None, 'Movimentação não encontrada para alteração.')

        elif acao == "excluir":
            try:
                movimentacao = Movimentacoes.objects.get(codigo=codigo)
                movimentacao.delete()
                return redirect('movimentacoes')  # Substitua 'solicitações' pela URL da sua lista de solicitações
            except movimentacao.DoesNotExist:
                form.add_error(None, 'Movimentação não encontrada para exclusão.')

    context = {
        'form': form,
        'movimentacoes': movimentacoes,
        'muda_acao': muda_acao,
        'codigo': codigo,
    }
    return render(request, 'movimentacoes.html', context)

@login_required(login_url='login')
def mov_entrada(request):
    movimentacoes   = Movimentacoes.objects.filter(tipo__in=['entrada', 'saida', 'devolucao'])
    form            = MovEntradaForm()
    muda_acao       = "incluir"
    codigo          = ""

    if request.method == 'POST':
        acao = request.POST.get("Acao")
        codigo = request.POST.get('id')

        if acao == "incluir":
            produto_id = request.POST.get('produto')
            produto_obj = CadProduto.objects.get(pk=produto_id)
            quantidade = int(request.POST.get('quantidade', 0))
            form = MovEntradaForm(request.POST)
            if form.is_valid():
                criar_itens_estoque(produto_obj, quantidade)
                form.save()
                return redirect('entrada')  # Substitua 'solicitações' pela URL da sua lista de solicitações
            else:
                print(form.errors)

        elif acao == "visualizar":
            movimentacao    = Movimentacoes.objects.get(codigo=codigo)
            form            = MovEntradaForm(instance=movimentacao)  # Pré-preenche o formulário com os dados da solicitação
            muda_acao       = "visualizar"  # Indica para o template que a ação é visualizar

        elif acao == "alterar_form":
            try:
                movimentacao    = Movimentacoes.objects.get(codigo=codigo)
                form            = MovEntradaForm(instance=movimentacao)  # Pré-preenche o formulário com os dados da solicitação
                muda_acao       = "alterar"  # Indica para o template que a ação é alterar
            except movimentacao.DoesNotExist:
                form.add_error(None, 'Movimentação não encontrada para alteração.')

        elif acao == "alterar":
            try:
                movimentacao     = Movimentacoes.objects.get(codigo=codigo)
                form            = MovEntradaForm(request.POST, instance=movimentacao)
                if form.is_valid():
                    form.save()
                    return redirect('entrada')  # Substitua 'solicitações' pela URL da sua lista de solicitações
            except movimentacao.DoesNotExist:
                form.add_error(None, 'Movimentação não encontrada para alteração.')

        elif acao == "excluir":
            try:
                movimentacao = Movimentacoes.objects.get(codigo=codigo)
                movimentacao.delete()
                return redirect('entrada')  # Substitua 'solicitações' pela URL da sua lista de solicitações
            except movimentacao.DoesNotExist:
                form.add_error(None, 'Movimentação não encontrada para exclusão.')

    context = {
        'form': form,
        'movimentacoes': movimentacoes,
        'muda_acao': muda_acao,
        'codigo': codigo,
    }
    return render(request, 'entrada.html', context)

def criar_itens_estoque(produto, quantidade):
    """
    Cria registros individuais em ItensEstoque para o produto informado.
    """
    itens_criados = []
    for i in range(quantidade):
        codigo_unico = f"EST-{uuid4().hex[:8].upper()}"
        item = ItensEstoque.objects.create(
            produto=produto,
            codigo=codigo_unico,
            numero_serie=None,  # Se quiser gerar automático, faça aqui
            status='disponivel',
            data_ultimo_status=timezone.now(),
            observacoes=''
        )
        itens_criados.append(item)
    return itens_criados

@login_required(login_url='login')
def almoxarifado(request):

    itens               = CadItem.objects.all()

    context = {
        'itens': itens,
    }
    return render(request, 'almoxarifado.html', context)

from django.db import connection

@login_required(login_url='login')
def saldos(request):
    with connection.cursor() as cursor:
        cursor.execute("""
SELECT
    (p."CODIGO"  || ' - ' || p."DESCRICAO" ) AS produto,
    SUM(CASE WHEN i.status = 'disponivel' THEN 1 ELSE 0 END) AS disponivel,
    SUM(CASE WHEN i.status = 'manutencao' THEN 1 ELSE 0 END) AS manutencao,
    SUM(CASE WHEN i.status = 'locado' THEN 1 ELSE 0 END) AS locado
FROM
    itens_estoque i
JOIN
    cad_produto p ON i.produto_id = p."CODIGO" 
GROUP BY
    p."CODIGO" , p."DESCRICAO";
        """)
        rows = cursor.fetchall()

    # Formatar para o template
    produtos = []
    for row in rows:
        produtos.append({
            'produto': row[0],
            'disponivel': row[1],
            'manutencao': row[2],
            'locado': row[3],
            'total': row[1] + row[2] + row[3],
        })

    return render(request, 'saldos.html', {'produtos': produtos})

from django.forms import inlineformset_factory
from django.utils import timezone

@login_required(login_url='login')
def locacao(request):
    ItensLocacaoFormSet = inlineformset_factory(
            Locacao, ItensLocacao, form=ItensLocacaoForm, extra=1, can_delete=True
        )

    if request.method == 'POST':
        locacao_form = LocacaoForm(request.POST)
        formset = ItensLocacaoFormSet(request.POST)

        if locacao_form.is_valid() and formset.is_valid():
            locacao = locacao_form.save(commit=False)
            locacao.codigo = locacao.codigo or f"LOC-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            locacao.save()

            itens = formset.save(commit=False)
            for item in itens:
                item.locacao = locacao
                item.save()
                # Registra a movimentação do estoque
                Movimentacoes.objects.create(
                    produto=item.produto,
                    quantidade=item.quantidade,
                    tipo='locacao',
                    documento='Locação',
                    data_movimentacao=locacao.data
                )
            return redirect('locacao')
    else:
        locacao_form = LocacaoForm(initial={
            'codigo': f"LOC-{timezone.now().strftime('%Y%m%d%H%M%S')}",
        })
        formset = ItensLocacaoFormSet()

    locacoes = Locacao.objects.all().order_by('-data')[:20]

    return render(request, 'locacao.html', {
        'locacao_form': locacao_form,
        'formset': formset,
        'locacoes': locacoes,
    })

@login_required(login_url='login')
def cotacao(request):
    ItensLocacaoFormSet = inlineformset_factory(
        Locacao, ItensLocacao, form=ItensLocacaoForm, extra=1, can_delete=True
    )

    if request.method == 'POST':
        locacao_form = LocacaoForm(request.POST)
        formset = ItensLocacaoFormSet(request.POST)

        if locacao_form.is_valid() and formset.is_valid():
            locacao = locacao_form.save(commit=False)
            locacao.codigo = locacao.codigo or f"LOC-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            locacao.save()

            formset.instance = locacao  # <- ESSENCIAL
            formset.save()

            # Registra movimentações
            for item in locacao.itens.all():
                Movimentacoes.objects.create(
                    produto=item.produto,
                    quantidade=item.quantidade,
                    tipo='cotacao',
                    documento='cotacao',
                    data_movimentacao=locacao.data
                )

            return redirect('cotacao')
        else:
            print(locacao_form.errors)
            print(formset.errors)

    else:
        locacao_form = LocacaoForm(initial={
            'codigo': f"LOC-{timezone.now().strftime('%Y%m%d%H%M%S')}",
        })
        formset = ItensLocacaoFormSet()

    locacoes = Locacao.objects.filter(status='pendente').order_by('-data')[:20]

    return render(request, 'cotacao.html', {
        'locacao_form': locacao_form,
        'formset': formset,
        'locacoes': locacoes,
    })

@login_required(login_url='login')
def aprovar_cotacao(request):
    locacoes = Locacao.objects.filter(status='pendente').order_by('-data')[:20]

    return render(request, 'aprovar_cotacao.html', {
        'locacoes': locacoes,
    })

# utils.py ou no topo do views.py mesmo
from fpdf import FPDF
import requests
from django.http import HttpResponse, JsonResponse
from io import BytesIO

def formatar_moeda(valor):
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return "0,00"

    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@login_required(login_url='login')
def cotacao_locacao(request, locacao_id):
    locacao = Locacao.objects.get(pk=locacao_id)
    locacao.status = 'aprovada'
    locacao.save()

    # Percorre os Itens da Locação
    itens_locacao = ItensLocacao.objects.filter(locacao_id=locacao_id)

    for item_locacao in itens_locacao:
        quantidade_necessaria = int(item_locacao.quantidade)

        # Pega do estoque os itens disponíveis (status = 'disponivel')
        itens_estoque_disponiveis = ItensEstoque.objects.filter(
            produto=item_locacao.produto,
            status='disponivel'
        ).order_by('id')[:quantidade_necessaria]  # Pega só a quantidade necessária

        if itens_estoque_disponiveis.count() < quantidade_necessaria:
            messages.error(request, f"Estoque insuficiente para o produto {item_locacao.produto.descricao}")
            return redirect('cotacao')  # ou onde quiser direcionar em caso de erro

        # Atualiza os itens para 'locado'
        for item_estoque in itens_estoque_disponiveis:
            item_estoque.status = 'locado'
            item_estoque.data_ultimo_status = timezone.now()
            item_estoque.save()

    # Gera o título no contas a receber
    gerar_conta_a_receber(request, locacao_id)

    messages.success(request, "Locação concluída e estoque atualizado com sucesso.")
    return redirect('listagem_locacoes')

@login_required(login_url='login')
def entrega_locacao(request):
    if request.method == 'POST':
        locacao_id = request.POST.get('locacao_id')
        motorista = request.POST.get('motorista')

        # 'getlist' é a chave aqui! Ele retorna uma lista de todos os valores com o mesmo nome
        item_ids = request.POST.getlist('item_ids')
        produto_ids = request.POST.getlist('produto_ids')

        # Itera sobre os IDs dos itens e produtos para criar os registros
        for i in range(len(item_ids)):
            item_id = item_ids[i]
            produto_id = produto_ids[i]

            print(produto_id)
            
            # Pega o valor da quantidade para o item atual
            quantidade_key = f'quantidade_item_{item_id}'
            quantidade = request.POST.get(quantidade_key)
            
            # Se a quantidade for válida e maior que 0, cria o objeto
            if quantidade and int(quantidade) > 0:
                codigo = "ENT-" + timezone.now().strftime('%Y%m%d%H%M%S') # Cria um código único para cada entrega

                # Garanta que os objetos existam antes de criar o registro
                try:
                    EntregaLocacao.objects.create(
                        codigo=codigo,
                        locacao_id=locacao_id,
                        produto_id=produto_id,
                        quantidade=quantidade,
                        motorista=motorista
                    )
                except (Locacao.DoesNotExist, CadProduto.DoesNotExist) as e:
                    # Opcional: Lidar com erro se a locação ou produto não for encontrado
                    print(f"Erro: Objeto não encontrado. Detalhes: {e}")
                    # Você pode adicionar uma mensagem de erro para o usuário aqui
                    pass

        # Redireciona para a página de locações após o sucesso
        return redirect('listagem_locacoes') 
    
    # Se a requisição não for POST, exibe a página normalmente
    locacoes = Locacao.objects.all()
    context = {'locacoes': locacoes}
    return render(request, 'listagem_locacoes', context)

AUTENTIQUE_API_KEY = "c5ed5f6340142407b4723f3c6183533a736c9aa5dc0a84c967e484ec09a69782"

@login_required(login_url='login')
def enviar_contrato_para_assinatura(request, locacao_id):
    locacao = Locacao.objects.get(pk=locacao_id)

    ItensLocacaoFormSet = inlineformset_factory(
            Locacao, ItensLocacao, form=ItensLocacaoForm, extra=1, can_delete=True
        )
    
    locacoes = Locacao.objects.all().order_by('-data')[:20]
    
    locacao_form = LocacaoForm(initial={
        'codigo': f"LOC-{timezone.now().strftime('%Y%m%d%H%M%S')}",
    })
    formset = ItensLocacaoFormSet()

    # Gere o PDF como bytes
    pdf_bytes = gerar_contrato(locacao)

    graphql_query = """
    mutation CreateDocumentMutation($document: DocumentInput!, $signers: [SignerInput!]!, $file: Upload!) {
      createDocument(document: $document, signers: $signers, file: $file) {
        id
        name
        signatures {
          link { short_link }
        }
      }
    }
    """

    payload = {
        'operations': {
            "query": graphql_query,
            "variables": {
                "document": {
                    "name": f"Contrato Locação #{locacao.id}"
                },
                "signers": [
                    {
                        "email": locacao.cliente.email,
                        "action": "SIGN",
                        "name": locacao.cliente.razao
                    }
                ],
                "file": None  # Será mapeado
            }
        },
        'map': '{"file": ["variables.file"]}'
    }

    # As partes que precisam ser JSON devem ser strings!
    operations = json.dumps(payload['operations'])
    map_part = payload['map']

    files = [
        ('file', ('contrato.pdf', BytesIO(pdf_bytes), 'application/pdf'))
    ]

    headers = {
        'Authorization': f'Bearer {AUTENTIQUE_API_KEY}'
    }

    response = requests.post(
        'https://api.autentique.com.br/v2/graphql',
        data={'operations': operations, 'map': map_part},
        files=files,
        headers=headers
    )

    if response.status_code == 200:
        return render(request, 'locacao.html', {'mensagem': 'Contrato enviado para assinatura com sucesso!',
        'locacao_form': locacao_form,
        'formset': formset,
        'locacoes': locacoes,})    
    else:
        return render(request, 'locacao.html', {'mensagem': 'Erro ao enviar contrato para assinatura.',
        'locacao_form': locacao_form,
        'formset': formset,
        'locacoes': locacoes})

@login_required(login_url='login')
def listar_itens_estoque(request):
    itens = ItensEstoque.objects.select_related('produto').all()
    return render(request, 'itens_estoque.html', {'itens': itens})

@login_required(login_url='login')
def listar_itens_estoque_locacao(request):
    itens = ItensEstoque.objects.select_related('produto').filter(status='locado').order_by('produto__descricao')
    return render(request, 'itens_estoque_locacao.html', {'itens': itens})

@login_required(login_url='login')
def salvar_itens_estoque_em_massa(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist('item_ids')
        for item_id in item_ids:
            try:
                item                    = ItensEstoque.objects.get(pk=item_id)
                item.numero_serie       = request.POST.get(f'numero_serie_{item_id}')
                #item.status             = request.POST.get(f'status_{item_id}')
                item.data_ultimo_status = timezone.now()
                item.observacoes        = request.POST.get(f'observacoes_{item_id}')
                item.save()
            except ItensEstoque.DoesNotExist:
                continue
        # Redirecione para onde quiser:
        return redirect('listar_itens_estoque')

def saldo_estoque_produto_item(request):
    produto_id = request.GET.get('produto_id')

    if not produto_id:
        return JsonResponse({'error': 'ID do produto não enviado'}, status=400)

    try:
        produto = CadProduto.objects.get(pk=produto_id)
        saldo = ItensEstoque.objects.filter(produto=produto).filter(status='disponivel').count()
        preco = produto.preco if produto.preco else 0
        return JsonResponse({'saldo': saldo, 'preco': preco, 'produto': produto.descricao})
    except CadProduto.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)

############################# FINANCEIRO ################################
@login_required(login_url='login')
def cad_conta_cobranca(request):
    conta               = ContaCobranca.objects.all()
    form                = ContaCobrancaForm()

    if request.method == 'POST':
        form = ContaCobrancaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cad_conta_cobranca')

    context = {
        'form': form,
        'contas': conta,
    }
    return render(request, 'financeiro/conta_cobranca.html', context)

@login_required(login_url='login')
def alterar_conta_cobranca(request, conta_id):
    contas            = ContaCobranca.objects.all()
    try:
        conta         = ContaCobranca.objects.get(id=conta_id)
        form          = ContaCobrancaForm(instance=conta)
    except ContaCobranca.DoesNotExist:
        form.add_error(None, 'Conta não encontrada para alteração.')
    
    if request.method == 'POST':
            form = ContaCobrancaForm(request.POST, instance=conta)
            if form.is_valid():
                form.save()
                messages.success(request, 'Conta de cobrança alterada com sucesso!')
                return redirect('cad_conta_cobranca')
            else:
                messages.error(request, 'Erro ao alterar a conta. Verifique os campos.')
    else:
        form = ContaCobrancaForm(instance=conta)

    context = {
        'form': form,
        'contas': contas,
        'id': conta.id,
    }
    return render(request, 'financeiro/conta_cobranca.html', context)

def excluir_conta_cobranca(request, conta_id):
    try:
        conta = ContaCobranca.objects.get(id=conta_id)
        conta.delete()
        messages.success(request, 'Conta de cobrança excluída com sucesso.')
    except ContaCobranca.DoesNotExist:
        messages.error(request, 'Conta de cobrança não encontrada.')

    return redirect('cad_conta_cobranca')

@login_required(login_url='login')
def cad_condicao_cobranca(request):
    condicoes           = CondicaoCobranca.objects.all()
    form                = CondicaoCobrancaForm()

    if request.method == 'POST':
        form = CondicaoCobrancaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cad_condicao_cobranca')

    context = {
        'form': form,
        'condicoes': condicoes,
    }
    return render(request, 'financeiro/condicao_cobranca.html', context)

@login_required(login_url='login')
def alterar_condicao_cobranca(request, condicao_id):
    condicoes            = CondicaoCobranca.objects.all()
    try:
        condicao      = CondicaoCobranca.objects.get(id=condicao_id)
        form          = CondicaoCobrancaForm(instance=condicao)
    except CondicaoCobranca.DoesNotExist:
        form.add_error(None, 'Condição não encontrada para alteração.')
    
    if request.method == 'POST':
            form = CondicaoCobrancaForm(request.POST, instance=condicao)
            if form.is_valid():
                form.save()
                messages.success(request, 'Condição de cobrança alterada com sucesso!')
                return redirect('cad_condicao_cobranca')
            else:
                messages.error(request, 'Erro ao alterar a condição. Verifique os campos.')
    else:
        form = CondicaoCobrancaForm(instance=condicao)

    context = {
        'form': form,
        'condicoes': condicoes,
        'id': condicao.id,
    }
    return render(request, 'financeiro/condicao_cobranca.html', context)

def excluir_condicao_cobranca(request, condicao_id):
    try:
        condicao = CondicaoCobranca.objects.get(id=condicao_id)
        condicao.delete()
        messages.success(request, 'Condição de cobrança excluída com sucesso.')
    except CondicaoCobranca.DoesNotExist:
        messages.error(request, 'Condição de cobrança não encontrada.')

    return redirect('cad_condicao_cobranca')

@login_required(login_url='login')
def cad_instrucao_cobranca(request):
    instrucoes          = InstrucaoCobranca.objects.all()
    form                = InstrucaoCobrancaForm()

    if request.method == 'POST':
        form = InstrucaoCobrancaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cad_instrucao_cobranca')

    context = {
        'form': form,
        'instrucoes': instrucoes,
    }
    return render(request, 'financeiro/instrucao_cobranca.html', context)

@login_required(login_url='login')
def alterar_instrucao_cobranca(request, instrucao_id):
    instrucoes        = InstrucaoCobranca.objects.all()
    try:
        instrucao     = InstrucaoCobranca.objects.get(id=instrucao_id)
        form          = InstrucaoCobrancaForm(instance=instrucao)
    except InstrucaoCobranca.DoesNotExist:
        form.add_error(None, 'Instrução não encontrada para alteração.')
    
    if request.method == 'POST':
            form = InstrucaoCobrancaForm(request.POST, instance=instrucao)
            if form.is_valid():
                form.save()
                messages.success(request, 'Instrução de cobrança alterada com sucesso!')
                return redirect('cad_instrucao_cobranca')
            else:
                messages.error(request, 'Erro ao alterar a condição. Verifique os campos.')
    else:
        form = InstrucaoCobrancaForm(instance=instrucao)

    context = {
        'form': form,
        'instrucoes': instrucoes,
        'id': instrucao.id,
    }
    return render(request, 'financeiro/instrucao_cobranca.html', context)

def excluir_instrucao_cobranca(request, instrucao_id):
    try:
        condicao = InstrucaoCobranca.objects.get(id=instrucao_id)
        condicao.delete()
        messages.success(request, 'Instrução de cobrança excluída com sucesso.')
    except InstrucaoCobranca.DoesNotExist:
        messages.error(request, 'Instrução de cobrança não encontrada.')

    return redirect('cad_instrucao_cobranca')
@login_required(login_url='login')
def gerar_conta_a_receber(request, locacao_id):
    locacao = Locacao.objects.get(pk=locacao_id)

    ContasReceber.objects.create(
        cliente=locacao.cliente,
        locacao=locacao,
        descricao=f"Locação {locacao.codigo}",
        valor_desconto=locacao.desconto or 0,
        valor_total=locacao.total,
        data_emissao=timezone.now().date(),
        data_vencimento=locacao.fim + timedelta(days=7),  # ou outra lógica de vencimento
        forma_pagamento=locacao.pagamento,
        status='aberto'
    )
    return redirect('titulos_a_receber')


@login_required(login_url='login')
def gerar_conta_a_receber_devolucao(request, locacao_id, devolucao_id):
    locacao = Locacao.objects.get(pk=locacao_id)
    devolucao = Devolucao.objects.get(pk=devolucao_id, locacao=locacao)

    # Calcula o total do custo adicional de todos os produtos da devolução
    total_custo_adicional = devolucao.itens.aggregate(
        total=models.Sum('custo_adicional')
    )['total'] or 0

    # Cria o objeto ContasReceber
    conta_receber = ContasReceber.objects.create(
        cliente=locacao.cliente,
        locacao=locacao,
        descricao=f"Devolução referente à locação {locacao.codigo}",
        valor_total=total_custo_adicional,
        data_emissao=timezone.now().date(),
        data_vencimento=timezone.now().date() + timezone.timedelta(days=30),  # 30 dias para vencimento
        status='aberto',
        forma_pagamento='boleto'
    )

    messages.success(request, f"Conta a receber criada com sucesso! Valor: R$ {total_custo_adicional:.2f}")
    return redirect('titulos_a_receber')

@login_required(login_url='login')
def titulos_a_receber(request):
    titulos = ContasReceber.objects.select_related('cliente', 'locacao').order_by('-data_emissao')
    return render(request, 'financeiro/titulos_a_receber.html', {'titulos': titulos})

@login_required(login_url='login')
def titulos_a_pagar(request):
    contas = ContasPagar.objects.all().order_by('data_vencimento')
    return render(request, 'financeiro/titulos_a_pagar.html', {'contas': contas})

####################### DASHBOARD ########################
from django.db.models import Sum, Count
from plotly.offline import plot
import plotly.graph_objs as go
from datetime import timedelta

def home(request):
    hoje            = timezone.now().date()
    inicio_mes      = hoje.replace(day=1)

    locacoes_mes    = Locacao.objects.filter(data__gte=inicio_mes)
    total_locacoes  = locacoes_mes.count()
    total_clientes  = locacoes_mes.values('cliente').distinct().count()
    itens_locados   = ItensEstoque.objects.filter(status='locado').count()
    receita_mes     = ItensLocacao.objects.filter(locacao__data__gte=inicio_mes).aggregate(total=Sum('preco'))['total'] or 0

    # Gráfico: locações por dia
    locs_por_dia = (
        locacoes_mes
        .values('data')
        .annotate(qtd=Count('id'))
        .order_by('data')
    )
    data_x = [d['data'] for d in locs_por_dia]
    data_y = [d['qtd'] for d in locs_por_dia]

    fig_linhas = go.Figure()
    fig_linhas.add_trace(go.Line(x=data_x, y=data_y, name='Locações', marker=dict(color='#2c2762')))
    fig_linhas.update_layout(title='Locações por Dia', xaxis_title='Data', yaxis_title='Qtd', plot_bgcolor='white', font=dict(color='#333'), title_font=dict(color='#800AD0'), margin=dict(t=50, l=40, r=40, b=40))
    plot_linhas = plot(fig_linhas, output_type='div', include_plotlyjs=False)

    # Gráfico: status dos itens
    status_itens = (
        ItensEstoque.objects
        .values('status')
        .annotate(qtd=Count('id'))
    )
    labels = [s['status'].capitalize() for s in status_itens]
    values = [s['qtd'] for s in status_itens]

    cores_pizza = ['#6c757d', '#2c2762', '#47ea89', '#ffffff']  # primária, secundária, tons neutros

    fig_pizza = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=cores_pizza), textinfo='label+percent', insidetextorientation='radial')])
    fig_pizza.update_layout(title='Status dos Itens de Estoque', title_font=dict(color='#2c2762'), font=dict(color='#333'), margin=dict(t=50, l=40, r=40, b=40))
    plot_pizza = plot(fig_pizza, output_type='div', include_plotlyjs=False)

    # 📊 NOVO: Gráfico de faturamento por produto
    faturamento_produto = (
        ItensLocacao.objects
        .filter(locacao__data__gte=inicio_mes)
        .values('produto__descricao')  # Campo de descrição do produto
        .annotate(total_faturado=Sum('preco'))
        .order_by('-total_faturado')
    )

    produtos = [f['produto__descricao'] for f in faturamento_produto]
    valores = [float(f['total_faturado']) for f in faturamento_produto]

    fig_faturamento = go.Figure()
    fig_faturamento.add_trace(go.Bar(
        x=produtos,
        y=valores,
        name='Faturamento',
        marker=dict(color='#2c2762'),
        text=valores,
        textposition='auto'  # cor secundária
    ))
    fig_faturamento.update_layout(
        title='Faturamento por Produto Locado',
        xaxis_title='Produto',
        yaxis_title='R$',
        plot_bgcolor='white',
        font=dict(color='#333'),
        title_font=dict(color='#2c2762'),
        margin=dict(t=50, l=40, r=40, b=40)
    )
    plot_faturamento = plot(fig_faturamento, output_type='div', include_plotlyjs=False)

    return render(request, 'home.html', {
        'total_locacoes': total_locacoes,
        'total_clientes': total_clientes,
        'itens_locados': itens_locados,
        'receita_mes': receita_mes,
        'plot_linhas': plot_linhas,
        'plot_pizza': plot_pizza,
        'plot_faturamento': plot_faturamento
    })

######################################### MANUTENCOES #########################################
from django.utils import timezone
from datetime import date
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.db.models import Max

@login_required(login_url='login')
def manutencoes(request):
    manutencoes         = Manutencao.objects.all()
    form                = ManutencaoForm()
    muda_acao           = "incluir"
    codigo              = ""
    manutencao_etapas   = []

    # Pegar a próxima numeração de OS
    max_id = Manutencao.objects.all().aggregate(Max('id'))['id__max']
    proximo_id = (max_id or 0) + 1

    if request.method == 'POST':
        acao        = request.POST.get("Acao")
        codigo      = request.POST.get('id')
        produto_id  = request.POST.get('produto')
        status      = request.POST.get('status')

        if acao == "incluir":
            form = ManutencaoForm(request.POST)
            if form.is_valid():
                manutencao = form.save()

                # Atualiza status do produto
                produto_obj = ItensEstoque.objects.get(id=produto_id)
                produto_obj.status = 'manutencao'
                produto_obj.data_ultimo_status = timezone.now()
                produto_obj.save()

                # Gera as etapas com base nas EtapaManutencao
                gerar_etapas_para_manutencao(manutencao)

                Movimentacoes.objects.create(
                    produto=produto_obj.produto,
                    quantidade=1,
                    tipo='manutencao',
                    documento='Manutencao',
                    data_movimentacao=timezone.now()
                )
                return redirect('manutencoes')

        elif acao == "visualizar":
            cliente         = Manutencao.objects.get(codigo=codigo)
            form            = ManutencaoForm(instance=cliente)
            muda_acao       = "visualizar"
            manutencao_etapas = EtapaManutencao.objects.filter(manutencao=cliente).order_by('ordem')

        elif acao == "alterar_form":
            try:
                cliente         = Manutencao.objects.get(codigo=codigo)
                form            = ManutencaoForm(instance=cliente)
                muda_acao       = "alterar"
                manutencao_etapas = EtapaManutencao.objects.filter(manutencao=cliente).order_by('ordem')
            except Manutencao.DoesNotExist:
                form.add_error(None, 'Manutenção não encontrada para alteração.')

        elif acao == "alterar":
            try:
                cliente = Manutencao.objects.get(codigo=codigo)
                form = ManutencaoForm(request.POST, instance=cliente)
                if form.is_valid():
                    form.save()

                    produto_obj = ItensEstoque.objects.get(pk=codigo)
                    produto_obj.status = 'disponivel' if status == 'concluida' else 'manutencao'
                    produto_obj.data_ultimo_status = timezone.now()
                    produto_obj.save()

                    return redirect('manutencoes')
            except Manutencao.DoesNotExist:
                form.add_error(None, 'Manutenção não encontrada para alteração.')

        elif acao == "excluir":
            try:
                cliente = Manutencao.objects.get(id=codigo)
                produto_obj = cliente.produto
                cliente.delete()
                produto_obj.status = 'disponivel'
                produto_obj.data_ultimo_status = timezone.now()
                produto_obj.save()
                return redirect('manutencoes')
            except Manutencao.DoesNotExist:
                form.add_error(None, 'Manutenção não encontrada para exclusão.')

    else:
        form = ManutencaoForm(initial={
            'id': proximo_id,
        })

    context = {
        'form': form,
        'manutencoes': manutencoes,
        'muda_acao': muda_acao,
        'codigo': codigo,
        'manutencao_etapas': manutencao_etapas,
        'proximo_id_visual': proximo_id
    }
    return render(request, 'manutencao/manutencoes.html', context)

@login_required(login_url='login')
def fluxo_manutencao(request):
    fluxos = FluxoManutencao.objects.all()
    form = FluxoManutencaoForm()
    muda_acao = "incluir"
    codigo = ""

    if request.method == 'POST':
        acao = request.POST.get("Acao")
        codigo = request.POST.get('id')

        if acao == "incluir":
            form = FluxoManutencaoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('fluxo_manutencao')
            else:
                print(form.errors)

        elif acao == "alterar_form":
            fluxo = FluxoManutencao.objects.get(id=codigo)
            form = FluxoManutencaoForm(instance=fluxo)
            muda_acao = "alterar"

        elif acao == "alterar":
            fluxo = FluxoManutencao.objects.get(id=codigo)
            form = FluxoManutencaoForm(request.POST, instance=fluxo)
            if form.is_valid():
                form.save()
                return redirect('fluxo_manutencao')

        elif acao == "excluir":
            try:
                fluxo = FluxoManutencao.objects.get(id=codigo)
                fluxo.delete()
                return redirect('fluxo_manutencao')
            except FluxoManutencao.DoesNotExist:
                form.add_error(None, 'Fluxo não encontrada para exclusão.')

    context = {
        'form': form,
        'fluxos': fluxos,
        'muda_acao': muda_acao,
        'codigo': codigo,
    }
    return render(request, 'manutencao/fluxo_manutencao.html', context)

@login_required(login_url='login')
def etapas_manutencao(request):
    etapas = EtapaManutencao.objects.all()
    form = EtapaManutencaoForm()
    muda_acao = "incluir"
    codigo = ""

    if request.method == 'POST':
        acao = request.POST.get("Acao")
        codigo = request.POST.get('id')

        if acao == "incluir":
            form = EtapaManutencaoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('etapas_manutencao')
            else:
                print(form.errors)

        elif acao == "visualizar":
            etapa = EtapaManutencao.objects.get(id=codigo)
            form = EtapaManutencaoForm(instance=etapa)
            muda_acao = "visualizar"

        elif acao == "alterar_form":
            etapa = EtapaManutencao.objects.get(id=codigo)
            form = EtapaManutencaoForm(instance=etapa)
            muda_acao = "alterar"

        elif acao == "alterar":
            etapa = EtapaManutencao.objects.get(id=codigo)
            form = EtapaManutencaoForm(request.POST, instance=etapa)
            if form.is_valid():
                form.save()
                return redirect('etapas_manutencao')

        elif acao == "excluir":
            try:
                etapa = EtapaManutencao.objects.get(id=codigo)
                etapa.delete()
                return redirect('etapas_manutencao')
            except EtapaManutencao.DoesNotExist:
                form.add_error(None, 'Etapa não encontrada para exclusão.')

    context = {
        'form': form,
        'etapas': etapas,
        'muda_acao': muda_acao,
        'codigo': codigo,
    }
    return render(request, 'manutencao/etapas_manutencao.html', context)

def gerar_etapas_para_manutencao(manutencao):
    fluxo = manutencao.fluxo

    for etapa in fluxo.etapas.all():
        EtapaManutencaoExecutada.objects.create(
            manutencao=manutencao,
            etapa=etapa,
            data_prevista=manutencao.data_inicio + timedelta(days=etapa.prazo_dias)
        )

@login_required(login_url='login')
def visualizar_manutencao(request, manutencao_id):
    manutencao  = get_object_or_404(Manutencao, id=manutencao_id)
    etapas      = manutencao.etapas.select_related('etapa').all()

    # Calculos para barra de progresso
    total       = etapas.count()
    concluidas  = etapas.filter(status='concluida').count()
    progresso   = int((concluidas / total) * 100) if total > 0 else 0

    # Situacao da manutencao
    for etapa in etapas:
        if etapa.status == 'pendente':
            if etapa.data_prevista < date.today():
                etapa.situacao = 'atrasada'
            else:
                etapa.situacao = 'em_andamento'
        else:
            if etapa.data_conclusao > etapa.data_prevista:
                etapa.situacao = 'atrasada'
            else:
                etapa.situacao = 'no prazo'

    return render(request, 'manutencao/visualizar_manutencao.html', {
        'manutencao': manutencao,
        'etapas': etapas,
        'progresso': progresso
    })

@login_required(login_url='login')
def listagem_manutencao(request):
    manutencoes         = Manutencao.objects.all()
    
    context = {
        'manutencoes': manutencoes,
    }
    return render(request, 'manutencao/listagem_manutencao.html', context)

@login_required(login_url='login')
@require_POST
def concluir_etapa(request, etapa_id):
    etapa = get_object_or_404(EtapaManutencaoExecutada, id=etapa_id)
    etapa.status = 'concluida'
    etapa.data_conclusao = timezone.now()
    etapa.save()
    return redirect('visualizar_manutencao', manutencao_id=etapa.manutencao.id)

def aprova_manutencao(request, manutencao_id):
    try:
        manutencao = Manutencao.objects.get(id=manutencao_id)
        manutencao.status = 'aprovada'
        manutencao.save()
        messages.success(request, 'Manutenção aprovada!')
    except Manutencao.DoesNotExist:
        messages.error(request, 'Manutencação não encontrada.')

    return redirect('aprovar_manutencoes')

@login_required(login_url='login')
def grade_manutencoes(request):
    manutencoes         = Manutencao.objects.filter(status='aprovada')
    
    context = {
        'manutencoes': manutencoes,
    }
    return render(request, 'manutencao/grade_manutencoes.html', context)
############################################## SOLICITACAO DE COMPRA ################################

@login_required(login_url='login')
def solicitacaodecompra(request):
    if request.method == 'POST':
            form = SolicitacaoCompraForm(request.POST)
            if form.is_valid():
                solicitacao = form.save(commit=False)
                solicitacao.solicitante = request.user
                solicitacao.save()

                # Salvar os itens
                itens_json = request.POST.get('itens_json')
                if itens_json:
                    itens = json.loads(itens_json)
                    for i in itens:
                        ItensSolicitacaoCompra.objects.create(
                            solicitacao=solicitacao,
                            produto_id=i['id'],
                            quantidade=i['quantidade'],
                            valor_unitario=i['valor_unitario']
                        )

                messages.success(request, "Solicitação incluída com sucesso.")
                return redirect('solicitacaodecompra')
    else:
        form = SolicitacaoCompraForm()

    return render(request, 'solicitacaodecompra.html', {
        'form': form,
        'itens': CadItem.objects.all()  # para o select
    })

def relacao_item_produto(request):
    if request.method == 'POST':
        form = RelacaoItemProdutoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RelacaoItemProdutoForm()
    
    context = {
        'form': form,
        'itens': RelacaoItemProduto.objects.all()
    }
    return render(request, 'relacao_item_produto.html', context)

############################################## ADMINISTRADOR ##################################
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.mixins import PermissionRequiredMixin 
from django.views import View
from core.forms import GroupForm # Importe o formulário criado
from django.contrib.contenttypes.models import ContentType

class CriarGrupoEPermissoesView(PermissionRequiredMixin, View):
    # Garante que só Superusuários ou Administradores internos tenham acesso
    permission_required = 'auth.add_group' # Permissão padrão para criar grupos
    raise_exception = True
    template_name = 'admin.html'

    def get(self, request):
        # 1. Obtém o formulário de nome do grupo
        form = GroupForm()
        
        # 2. Lista TODAS as permissões disponíveis (incluindo as customizadas)
        # Filtre aqui se quiser remover permissões desnecessárias, como as do admin.
        available_permissions = Permission.objects.all().order_by('content_type__app_label', 'content_type__model', 'name')
        
        context = {
            'form': form,
            'available_permissions': available_permissions
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = GroupForm(request.POST)
        
        if form.is_valid():
            # Cria o novo Grupo
            new_group = form.save()
            
            # Obtém a lista de IDs de permissões selecionadas (do checkbox)
            selected_permission_ids = request.POST.getlist('permissions')
            
            # Obtém os objetos Permission com base nos IDs
            permissions = Permission.objects.filter(id__in=selected_permission_ids)
            
            # Atribui as permissões ao novo Grupo
            new_group.permissions.set(permissions)
            
            # Redireciona para onde você lista os grupos, por exemplo
            return redirect('lista_grupos') 
        
        # Se o formulário não for válido, retorna à tela com erro
        available_permissions = Permission.objects.all().order_by('content_type__app_label', 'content_type__model', 'name')
        context = {
            'form': form,
            'available_permissions': available_permissions
        }
        return render(request, self.template_name, context)