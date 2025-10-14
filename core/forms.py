from django import forms
from django.forms import inlineformset_factory
from .models import CadEmpresa, CadCliente, CadFornecedor, CadGrupoProduto, CadUnidadeMedida, CadItem, CadProduto, SolicitacaoCompra
from .models import Movimentacoes, ItensEstoque, ItensLocacao, Locacao, ItensSolicitacaoCompra
from .models import Manutencao
from .models import RelacaoItemProduto

ESTADOS_BRASIL = [
    ('', 'Escolha um Estado'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
    ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
    ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
]

class CadEmpresaForm(forms.ModelForm):

    # Campos obrigatórios
    codigo          = forms.CharField(required=True, label='Código', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codigo', 'id': 'id_codigo', 'maxlength': 10}))
    cnpj            = forms.CharField(required=True, label='CNPJ', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ', 'data-mask': '00.000.000/0000-00', 'id': 'id_cnpj'}))
    razao           = forms.CharField(required=True, label='Razão Social', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razão Social', 'id': 'id_razao'}))
    uf              = forms.ChoiceField(required=True, label='UF', choices=ESTADOS_BRASIL, widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_uf'}))
    cidade          = forms.CharField(required=True, label='Cidade', widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_cidade'}))
    email           = forms.EmailField(required=True, label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))

    # Campos opcionais
    fantasia        = forms.CharField(required=False, label='Fantasía', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fantasia', 'id': 'id_fantasia'}))
    estadual        = forms.CharField(required=False, label='Inscrição Estadual', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estadual', 'id': 'id_estadual'}))
    municipal       = forms.CharField(required=False, label='Inscrição Municipal', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Municipal', 'id': 'id_municipal'}))
    suframa         = forms.CharField(required=False, label='Suframa', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Suframa', 'id': 'id_suframa'}))
    cep             = forms.CharField(required=False, label='CEP', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP', 'id': 'id_cep', 'data-mask': '00000-000'}))
    logradouro      = forms.CharField(required=False, label='Logradouro', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Logradouro', 'id': 'id_logradouro'}))
    numero          = forms.CharField(required=False, label='Número', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numero', 'id': 'id_numero'}))
    complemento     = forms.CharField(required=False, label='Complemento', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Complemento'}))
    bairro          = forms.CharField(required=False, label='Bairro', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro', 'id': 'id_bairro'}))
    telefone        = forms.CharField(required=False, label='Telefone', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'data-mask': '(00) 00000-0000'}))

    class Meta:
        model = CadEmpresa
        fields = '__all__'

class CadClienteForm(forms.ModelForm):
    ESTADOS_BRASIL = [
        ('', 'Escolha um Estado'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]

    # Campos obrigatórios
    codigo          = forms.CharField(required=True, label='Código', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Código', 'id': 'id_codigo', 'maxlength': 10}))
    tipo            = forms.ChoiceField(required=True, label='Tipo', choices=[('','Escolha o Tipo'),('Jurídica','Jurídica'),('Física','Física')], widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo'}))
    cnpj_cpf        = forms.CharField(required=True, label='CNPJ/CPF', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'CNPJ/CPF', 'id': 'id_cnpj_cpf'}))
    razao           = forms.CharField(required=True, label='Razão Social', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Razão Social', 'id': 'id_razao'}))
    uf              = forms.ChoiceField(required=True, label='UF', choices=ESTADOS_BRASIL, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'UF', 'id': 'id_uf'}))
    cidade          = forms.CharField(required=True, label='Cidade', widget=forms.Select(attrs={'class': 'form-control', 'placeholder':'Cidade', 'id': 'id_cidade'}))
    email           = forms.EmailField(required=True, label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'E-mail',}))

    # Campos opcionais
    fantasia        = forms.CharField(required=False, label='Fantasía', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Fantasia', 'id': 'id_fantasia'}))
    estadual        = forms.CharField(required=False, label='Inscrição Estadual', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Estadual', 'id': 'id_estadual'}))
    municipal       = forms.CharField(required=False, label='Inscrição Municipal', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Municipal', 'id': 'id_municipal'}))
    suframa         = forms.CharField(required=False, label='Suframa', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Suframa', 'id': 'id_suframa'}))
    cep             = forms.CharField(required=False, label='CEP', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'CEP', 'id': 'id_cep', 'data-mask': '00000-000'}))
    logradouro      = forms.CharField(required=False, label='Logradouro', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Logradouro', 'id': 'id_logradouro'}))
    numero          = forms.CharField(required=False, label='Número', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Número', 'id': 'id_numero'}))
    complemento     = forms.CharField(required=False, label='Complemento', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Complemento'}))
    bairro          = forms.CharField(required=False, label='Bairro', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Bairro', 'id': 'id_bairro'}))
    telefone        = forms.CharField(required=False, label='Telefone', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'data-mask': '(00) 00000-0000'}))

    class Meta:
        model = CadCliente
        fields = '__all__'

class CadFornecedorForm(forms.ModelForm):
    ESTADOS_BRASIL = [
        ('', 'Escolha um Estado'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]

    # Campos obrigatórios
    codigo          = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Código', 'id': 'id_codigo', 'maxlength': 10}))
    tipo            = forms.ChoiceField(required=True, choices=[('','Tipo'),('Jurídica','Jurídica'),('Física','Física')], widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo'}))
    cnpj_cpf        = forms.CharField(required=True, label='CNPJ/CPF', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'CNPJ/CPF', 'id': 'id_cnpj_cpf'}))
    razao           = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Razão Social', 'id': 'id_razao'}))
    uf              = forms.ChoiceField(required=True, choices=ESTADOS_BRASIL, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'UF', 'id': 'id_uf'}))
    cidade          = forms.CharField(required=True, widget=forms.Select(attrs={'class': 'form-control', 'placeholder':'Cidade', 'id': 'id_cidade'}))
    email           = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'E-mail',}))

    # Campos opcionais
    fantasia        = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Fantasia', 'id': 'id_fantasia'}))
    estadual        = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Estadual', 'id': 'id_estadual'}))
    municipal       = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Municipal', 'id': 'id_municipal'}))
    suframa         = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Suframa', 'id': 'id_suframa'}))
    cep             = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'CEP', 'id': 'id_cep', 'data-mask': '00000-000'}))
    logradouro      = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Logradouro', 'id': 'id_logradouro'}))
    numero          = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Número', 'id': 'id_numero'}))
    complemento     = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Complemento'}))
    bairro          = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Bairro', 'id': 'id_bairro'}))
    telefone        = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'data-mask': '(00) 00000-0000'}))

    class Meta:
        model = CadFornecedor
        fields = '__all__'
    
class CadGrupoProdutoForm(forms.ModelForm):
    codigo          = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Código', 'id': 'id_codigo', 'maxlength': 10}))
    descricao       = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Descrição', 'id': 'id_descricao'}))

    class Meta:
        model = CadGrupoProduto
        fields = '__all__'

class CadUnidadeMedidaForm(forms.ModelForm):
    codigo          = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Código', 'id': 'id_codigo', 'maxlength': 10}))
    descricao       = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Descrição', 'id': 'id_descricao'}))

    class Meta:
        model = CadUnidadeMedida
        fields = '__all__'

class CadItemForm(forms.ModelForm):
    class Meta:
        model = CadItem
        fields = ['codigo', 'descricao', 'unidade']  # Removido 'quantidade'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'unidade': forms.Select(attrs={'class': 'form-control'}),
        }

from django import forms
from django.contrib.auth.models import User
from .models import SolicitacaoCompra, CadFornecedor

class SolicitacaoCompraForm(forms.ModelForm):
    fornecedor = forms.ModelChoiceField(
        queryset=CadFornecedor.objects.all(),
        empty_label="Selecione um fornecedor",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_fornecedor'})
    )

    valor_total = forms.CharField(
        required=True,
        label='Valor Total (R$)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Valor Total (R$)',
            'id': 'id_valor_total',
            'data-mask': 'money',
            'readonly': 'readonly'
        })
    )

    def clean_valor_unitario(self):
        valor_unitario = self.cleaned_data.get('valor_unitario')
        if valor_unitario:
            valor_unitario = valor_unitario.replace('.', '').replace(',', '.')
        else:
            valor_unitario = 0
        return float(valor_unitario)
    
    def clean_valor_total(self):
        valor_total = self.cleaned_data.get('valor_total')
        if valor_total:
            valor_total = valor_total.replace('.', '').replace(',', '.')
        else:
            valor_total = 0
        return float(valor_total)

    class Meta:
        model = SolicitacaoCompra
        fields = ['codigo', 'fornecedor', 'data_solicitacao', 'justificativa', 'valor_total']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código da solicitação', 'id': 'id_codigo'}),
            'data_solicitacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data'}),
            'justificativa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Justifique a solicitação', 'id': 'id_justificativa'}),
        }

class ItensSolicitacaoCompraForm(forms.ModelForm):
    class Meta:
        model = ItensSolicitacaoCompra
        fields = ['produto', 'quantidade', 'valor_unitario']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CadProdutoForm(forms.ModelForm):
    ATIVO_CHOICES = [
        ('', 'Escolha o Status'), ('1', 'Ativo'), ('0', 'Inativo')
    ]

    TIPO_CHOICES = [
        ('', 'Escolha o Tipo'), ('1', 'Ativo'), ('2', 'Uso e consumo'), ('3', 'Mercadoria'), ('4', 'Outros')
    ]

    is_ativo    = forms.ChoiceField(required=True, label='Status', choices=ATIVO_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_is_ativo'}))
    codigo      = forms.CharField(required=True, label='Código', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código', 'id': 'id_codigo', 'maxlength': 10}))
    descricao   = forms.CharField(required=True, label='Descrição', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'id': 'id_descricao'}))
    grupo       = forms.ModelChoiceField(queryset=CadGrupoProduto.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_grupo'}), empty_label="Selecione um Grupo de Produto")
    unidade     = forms.ModelChoiceField(queryset=CadUnidadeMedida.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_unidade'}), empty_label="Selecione a Unidade de Medida")
    tipo        = forms.ChoiceField(required=True, label='Tipo', choices=TIPO_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo'}))
    preco       = forms.CharField(required=True, label='Preço (R$)', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preço (R$)', 'id': 'id_preco', 'data-mask': 'money'}))
    ressarcimento = forms.CharField(
        required=True,
        label='Ressarcimento (R$)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ressarcimento (R$)',
            'id': 'id_ressarcimento',
            'data-mask': 'money'
        })
    )

    # Campos para dimensões e peso
    altura = forms.CharField(
        required=False,
        label='Altura (cm)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Altura (cm)',
            'id': 'id_altura',
            'data-mask': 'money'
        })
    )
    largura = forms.CharField(
        required=False,
        label='Largura (cm)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Largura (cm)',
            'id': 'id_largura',
            'data-mask': 'money'
        })
    )
    profundidade = forms.CharField(
        required=False,
        label='Profundidade (cm)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Profundidade (cm)',
            'id': 'id_profundidade',
            'data-mask': 'money'
        })
    )
    peso = forms.CharField(
        required=False,
        label='Peso (kg)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Peso (kg)',
            'id': 'id_peso',
            'data-mask': 'money'
        })
    )
    foto = forms.ImageField(
        required=False,
        label='Foto do Produto',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'id': 'id_foto'
        })
    )

    # Métodos para limpar os campos de dimensões e peso
    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco:
            preco = preco.replace('.', '').replace(',', '.')
        else:
            preco = 0
        return float(preco)

    def clean_ressarcimento(self):
        ressarcimento = self.cleaned_data.get('ressarcimento')
        if ressarcimento:
            ressarcimento = ressarcimento.replace('.', '').replace(',', '.')
        else:
            ressarcimento = 0
        return float(ressarcimento)

    def clean_altura(self):
        altura = self.cleaned_data.get('altura')
        if altura:
            altura = altura.replace(',', '.')
        else:
            altura = 0
        return float(altura)

    def clean_largura(self):
        largura = self.cleaned_data.get('largura')
        if largura:
            largura = largura.replace(',', '.')
        else:
            largura = 0
        return float(largura)

    def clean_profundidade(self):
        profundidade = self.cleaned_data.get('profundidade')
        if profundidade:
            profundidade = profundidade.replace(',', '.')
        else:
            profundidade = 0
        return float(profundidade)

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if peso:
            peso = peso.replace(',', '.')
        else:
            peso = 0
        return float(peso)

    class Meta:
        model = CadProduto
        fields = '__all__'

class MovimentacoesForm(forms.ModelForm):
    documento = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento', 'id': 'id_documento'})
    )
    data_movimentacao = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_movimentacao'})
    )
    produto = forms.ModelChoiceField(
        queryset=CadProduto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_produto'}),
        empty_label="Selecione o item"
    )
    quantidade = forms.DecimalField(
        required=True,
        max_digits=10,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade', 'id': 'id_quantidade'})
    )
    tipo = forms.ChoiceField(
        required=True,
        choices=[('entrada', 'Entrada'),('saida', 'Saída'),('emprestimo', 'Empréstimo'),('devolucao', 'Devolução'),('avaria', 'Avaria')],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo'})
    )

    class Meta:
        model = Movimentacoes
        fields = ['documento','data_movimentacao', 'produto', 'quantidade', 'tipo']

class MovEntradaForm(forms.ModelForm):
    documento = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento', 'id': 'id_documento'})
    )
    data_movimentacao = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_movimentacao'})
    )
    produto = forms.ModelChoiceField(
        queryset=CadProduto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_produto'}),
        empty_label="Selecione o item"
    )
    quantidade = forms.DecimalField(
        required=True,
        min_value=0,
        max_digits=10,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade', 'id': 'id_quantidade'})
    )
    tipo = forms.ChoiceField(
        required=True,
        choices=[('entrada', 'Entrada')],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo'})
    )

    class Meta:
        model = Movimentacoes
        fields = ['documento','data_movimentacao', 'produto', 'quantidade', 'tipo']

class LocacaoForm(forms.ModelForm):
    codigo = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código', 'readonly': 'readonly', 'id': 'id_codigo'})
    )
    solicitante = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solicitante'})
    )
    cliente = forms.ModelChoiceField(
        queryset=CadCliente.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Selecione um Cliente"
    )
    inicio = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_movimentacao'})
    )
    fim = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_movimentacao'})
    )
    desconto = forms.CharField(
        required=True,
        label='Desconto',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Desconto',
            'value': '0,00',
            'id': 'id_desconto',
            'data-mask': 'money'
        })
    )
    observacoes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações', 'rows': 3, 'id': 'id_observacoes'})
    )
    pagamento       = forms.ChoiceField(
        required=True,
        choices=[('dinheiro', 'Dinheiro'), ('cartao', 'Cartão'), ('pix', 'Pix')],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_pagamento'})
    )
    total = forms.CharField(
        required=True,
        label='Total',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'value': '0,00',
            'placeholder': 'Total',
            'id': 'id_total',
            'data-mask': 'money'
        })
    )

    # Método para limpar o campo de desconto
    def clean_desconto(self):
        desconto = self.cleaned_data.get('desconto')
        if desconto:
            desconto = desconto.replace('.', '').replace(',', '.')
        else:
            desconto = 0
        return float(desconto)
    
    # Método para limpar o campo de total
    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total:
            total = total.replace('.', '').replace(',', '.')
        else:
            total = 0
        return float(total)

    class Meta:
        model = Locacao
        fields = ['codigo', 'solicitante', 'cliente', 'inicio', 'fim', 'desconto', 'observacoes', 'pagamento', 'total']

class ItensLocacaoForm(forms.ModelForm):
    produto = forms.ModelChoiceField(
        queryset=CadProduto.objects.filter(is_ativo=1),
        widget=forms.Select(attrs={'class': 'form-control produto-select', 'id': 'id_produto'}),
        empty_label="Selecione o produto"
    )
    quantidade = forms.DecimalField(
        required=True,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control quantidade-input', 'placeholder': 'Quantidade', 'id': 'id_quantidade'})
    )
    saldo = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control saldo-input', 'placeholder': 'Quantidade', 'readonly': 'readonly', 'id': 'id_saldo'})
    )
    preco = forms.CharField(
        required=True,
        label='Preço',
        widget=forms.TextInput(attrs={
            'class': 'form-control preco-input',
            'readonly': 'readonly',
            'value': '0,00',
            'placeholder': 'Preço',
            'id': 'id_preco',
            'data-mask': 'money'
        })
    )

    # Métodos para limpar os campos de dimensões e peso
    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco:
            preco = preco.replace('.', '').replace(',', '.')
        else:
            preco = 0
        return float(preco)
    
    class Meta:
        model = ItensLocacao
        fields = ['produto', 'quantidade','preco']

class ItensEstoqueForm(forms.ModelForm):
    class Meta:
        model = ItensEstoque
        fields = ['numero_serie', 'status', 'observacoes']
        widgets = {
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class RelacaoItemProdutoForm(forms.ModelForm):
    class Meta:
        model = RelacaoItemProduto
        fields = ['item','produto']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'produto': forms.Select(attrs={'class': 'form-control'}),
        }

######################################### MANUTENCOES #########################################
from .models import EtapaManutencao
from .models import FluxoManutencao

class FluxoManutencaoForm(forms.ModelForm):
    class Meta:
        model = FluxoManutencao
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ManutencaoForm(forms.ModelForm):
    id  = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'O.S.', 'readonly': 'readonly', 'id': 'id_id'}),
        label='O.S.'
    )
    fluxo = forms.ModelChoiceField(
        queryset=FluxoManutencao.objects.filter(),
        widget=forms.Select(attrs={'class': 'form-control produto-select', 'id': 'id_fluxo'}),
        empty_label="Selecione o fluxo"
    )
    data_inicio = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_inicio'})
    )
    produto = forms.ModelChoiceField(
        queryset=ItensEstoque.objects.filter(status='disponivel'),
        widget=forms.Select(attrs={'class': 'form-control produto-select', 'id': 'id_fluxo'}),
        empty_label="Selecione o produto"
    )
    tipo = forms.ChoiceField(
        required=True,
        choices=[('preventiva', 'Preventiva'),('corretiva', 'Corretiva'),('outros', 'Outros')],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo'})
    )
    class Meta:
        model = Manutencao
        fields = ['id','fluxo', 'produto', 'data_inicio', 'observacoes','tipo']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_id(self):
        return None 

class EtapaManutencaoForm(forms.ModelForm):
    fluxo = forms.ModelChoiceField(
        queryset=FluxoManutencao.objects.filter(),
        widget=forms.Select(attrs={'class': 'form-control produto-select', 'id': 'id_fluxo'}),
        empty_label="Selecione o fluxo"
    )
    class Meta:
        model = EtapaManutencao
        fields = ['fluxo', 'nome', 'descricao', 'ordem', 'prazo_dias']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
            'prazo_dias': forms.NumberInput(attrs={'class': 'form-control'}),
        }

############################## FINANCERO #####################################
from .models import ContaCobranca
from .models import CondicaoCobranca
from .models import InstrucaoCobranca

class ContaCobrancaForm(forms.ModelForm):
    class Meta:
        model = ContaCobranca
        fields = ['banco', 'numero', 'digito', 'convenio', 'carteira']
        labels = {
            'numero':   'Número da Conta',
            'digito':   'Dígito',
            'convenio': 'Convênio',
        }
        widgets = {
            'banco':    forms.Select(attrs={'class': 'form-control'}),
            'numero':   forms.TextInput(attrs={'class': 'form-control'}),
            'digito':   forms.TextInput(attrs={'class': 'form-control'}),
            'convenio': forms.TextInput(attrs={'class': 'form-control'}),
            'carteira': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CondicaoCobrancaForm(forms.ModelForm):
    class Meta:
        model = CondicaoCobranca
        fields = ['codigo', 'vencimento_dias','juros','multa']
        labels = {
            'codigo':           'Código',
            'vencimento_dias':  'Dias para Vencimento',
            'juros':            '% Juros',
            'multa':            '% Multa'
        }
        widgets = {
            'codigo':           forms.TextInput(attrs={'class': 'form-control'}),
            'vencimento_dias':  forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'juros':            forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'multa':            forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
        }

class InstrucaoCobrancaForm(forms.ModelForm):
    class Meta:
        model = InstrucaoCobranca
        fields = ['codigo','mensagem1','mensagem2','mensagem3','local_pagamento']
        labels = {
            'codigo':           'Código',
            'mensagem1':        'Mensagem Cobrança 1',
            'mensagem2':        'Mensagem Cobrança 2',
            'mensagem3':        'Mensagem Cobrança 3',
            'local_pagamento':  'Local de Pagamento'
        }
        widgets = {
            'codigo':           forms.TextInput(attrs={'class': 'form-control'}),
            'mensagem1':        forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200}),
            'mensagem2':        forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200}),
            'mensagem3':        forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200}),
            'local_pagamento':  forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200}),
        }

############################# DEVOLUCAO #####################################
from .models import Devolucao, ItemDevolucao
from django.forms import inlineformset_factory, BaseInlineFormSet

class DevolucaoForm(forms.ModelForm):
    class Meta:
        model = Devolucao
        fields = ['locacao', 'data_devolucao', 'observacoes']
        widgets = {
            'data_devolucao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'locacao': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

class ItemDevolucaoForm(forms.ModelForm):
    class Meta:
        model = ItemDevolucao
        fields = ['item_locacao', 'quantidade', 'estado', 'observacoes']

    def __init__(self, *args, locacao=None, **kwargs):
        super().__init__(*args, **kwargs)
        if locacao:
            self.fields['item_locacao'].queryset = ItensLocacao.objects.filter(locacao=locacao)
        else:
            self.fields['item_locacao'].queryset = ItensLocacao.objects.none()


class BaseItemDevolucaoFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.locacao = kwargs.pop('locacao', None)
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['locacao'] = self.locacao
        return super()._construct_form(i, **kwargs)


ItemDevolucaoFormSet = inlineformset_factory(
    Devolucao,
    ItemDevolucao,
    form=ItemDevolucaoForm,
    formset=BaseItemDevolucaoFormSet,
    extra=1,
    can_delete=True
)

############################# ADMINISTRADOR #####################################
from django.contrib.auth.models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
        widgets = {
            # Você pode estilizar o campo de nome
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }