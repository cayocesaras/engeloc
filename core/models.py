
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .domain.financeiro.CentroCusto import CentroCusto

### Tabelas de Cadastro ###

class CadEmpresa(models.Model):
    codigo          = models.CharField(db_column='CODIGO', primary_key=True, max_length=10)
    cnpj            = models.CharField(db_column='CNPJ', max_length=18)
    razao           = models.CharField(db_column='RAZAO', max_length=100)
    fantasia        = models.CharField(db_column='FANTASIA', max_length=100)
    estadual        = models.CharField(db_column='ESTADUAL', max_length=14)
    municipal       = models.CharField(db_column='MUNICIPAL', max_length=14)
    suframa         = models.CharField(db_column='SUFRAMA', max_length=14)
    cep             = models.CharField(db_column='CEP', max_length=9)
    logradouro      = models.CharField(db_column='LOGRADOURO', max_length=100)
    numero          = models.CharField(db_column='NUMERO', max_length=6)
    complemento     = models.CharField(db_column='COMPLEMENTO', max_length=200)
    bairro          = models.CharField(db_column='BAIRRO', max_length=100)
    uf              = models.CharField(db_column='UF', max_length=2)
    cidade          = models.CharField(db_column='CIDADE', max_length=50)
    telefone        = models.CharField(db_column='TELEFONE', max_length=15)
    email           = models.CharField(db_column='EMAIL', max_length=100)

    class Meta:
        db_table            = 'cad_empresa'
        verbose_name        = 'Cadastro de Empresa'
        verbose_name_plural = 'Cadastro de Empresas'

class CadCliente(models.Model):
    codigo          = models.CharField(db_column='CODIGO', primary_key=True, max_length=10)
    tipo            = models.CharField(db_column='TIPO', max_length=8)
    cnpj_cpf        = models.CharField(db_column='CNPJ_CPF', max_length=18)
    razao           = models.CharField(db_column='RAZAO', max_length=100)
    fantasia        = models.CharField(db_column='FANTASIA', max_length=100)
    estadual        = models.CharField(db_column='ESTADUAL', max_length=14)
    municipal       = models.CharField(db_column='MUNICIPAL', max_length=14)
    suframa         = models.CharField(db_column='SUFRAMA', max_length=14)
    cep             = models.CharField(db_column='CEP', max_length=9)
    logradouro      = models.CharField(db_column='LOGRADOURO', max_length=100)
    numero          = models.CharField(db_column='NUMERO', max_length=6)
    complemento     = models.CharField(db_column='COMPLEMENTO', max_length=200)
    bairro          = models.CharField(db_column='BAIRRO', max_length=100)
    uf              = models.CharField(db_column='UF', max_length=2)
    cidade          = models.CharField(db_column='CIDADE', max_length=50)
    telefone        = models.CharField(db_column='TELEFONE', max_length=15)
    email           = models.CharField(db_column='EMAIL', max_length=100)

    class Meta:
        db_table            = 'cad_cliente'
        verbose_name        = 'Cadastro de Cliente'
        verbose_name_plural = 'Cadastro de Clientes'
    
    def __str__(self):
        return self.razao

class CadFornecedor(models.Model):
    codigo          = models.CharField(db_column='CODIGO', primary_key=True, max_length=10)
    tipo            = models.CharField(db_column='TIPO', max_length=8)
    cnpj_cpf        = models.CharField(db_column='CNPJ_CPF', max_length=18)
    razao           = models.CharField(db_column='RAZAO', max_length=100)
    fantasia        = models.CharField(db_column='FANTASIA', max_length=100)
    estadual        = models.CharField(db_column='ESTADUAL', max_length=14)
    municipal       = models.CharField(db_column='MUNICIPAL', max_length=14)
    suframa         = models.CharField(db_column='SUFRAMA', max_length=14)
    cep             = models.CharField(db_column='CEP', max_length=9)
    logradouro      = models.CharField(db_column='LOGRADOURO', max_length=100)
    numero          = models.CharField(db_column='NUMERO', max_length=6)
    complemento     = models.CharField(db_column='COMPLEMENTO', max_length=200)
    bairro          = models.CharField(db_column='BAIRRO', max_length=100)
    uf              = models.CharField(db_column='UF', max_length=2)
    cidade          = models.CharField(db_column='CIDADE', max_length=50)
    telefone        = models.CharField(db_column='TELEFONE', max_length=15)
    email           = models.CharField(db_column='EMAIL', max_length=100)

    class Meta:
        db_table            = 'cad_fornecedor'
        verbose_name        = 'Cadastro de Fornecedor'
        verbose_name_plural = 'Cadastro de Fornecedores'
    
    def __str__(self):
        return self.razao

class CadGrupoProduto(models.Model):
    codigo          = models.CharField(db_column='CODIGO', primary_key=True, max_length=10)
    descricao       = models.CharField(db_column='DESCRICAO', max_length=100)

    class Meta:
        db_table            = 'cad_grupo_produto'
        verbose_name        = 'Cadastro de Grupo de Produto'
        verbose_name_plural = 'Cadastro de Grupos de Produto'

    def __str__(self):
            return self.descricao

class CadUnidadeMedida(models.Model):
    codigo          = models.CharField(db_column='CODIGO', primary_key=True, max_length=10)
    descricao       = models.CharField(db_column='DESCRICAO', max_length=100)

    class Meta:
        db_table            = 'cad_unidade_medida'
        verbose_name        = 'Cadastro de Unidade de Medida'
        verbose_name_plural = 'Cadastro de Unidades de Medida'
    
    def __str__(self):
            return self.descricao

class CadProduto(models.Model):
    codigo          = models.CharField(db_column='CODIGO', primary_key=True, max_length=10)
    descricao       = models.CharField(db_column='DESCRICAO', max_length=100)
    grupo           = models.ForeignKey(CadGrupoProduto, db_column='GRUPO', on_delete=models.CASCADE)  # Alterado para ForeignKey
    unidade         = models.ForeignKey(CadUnidadeMedida, db_column='UNIDADE', on_delete=models.CASCADE)  # Alterado para ForeignKey
    preco           = models.DecimalField(db_column='PRECO', max_digits=10, decimal_places=2)
    altura          = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Altura (cm)")
    largura         = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Largura (cm)")
    profundidade    = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Profundidade (cm)")
    peso            = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    tipo            = models.CharField(db_column='TIPO', max_length=10)
    ressarcimento   = models.DecimalField(db_column='RESSARCIMENTO', max_digits=10, decimal_places=2)
    is_ativo        = models.IntegerField(db_column='IS_ATIVO')
    foto            = models.ImageField(upload_to='produtos/', blank=True, null=True)  # 👈 Alterado

    class Meta:
        db_table            = 'cad_produto'
        verbose_name        = 'Cadastro de Produto'
        verbose_name_plural = 'Cadastro de Produtos'
    
    def __str__(self):
            return self.descricao
    
############################################ COMPRAS ####################################################


class CadItem(models.Model):
    codigo      = models.CharField(max_length=20, default=1, unique=True)
    descricao   = models.CharField(max_length=200)
    unidade     = models.ForeignKey(CadUnidadeMedida, on_delete=models.CASCADE)
    ativo       = models.BooleanField(default=True)  # Para controle de catálogo ativo/inativo

    class Meta:
        db_table            = 'cad_item'
        ordering            = ['descricao']
        verbose_name        = 'Cadastro de Item'
        verbose_name_plural = 'Cadastro de Itens'

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"
    
class RelacaoItemProduto(models.Model):
    item        = models.ForeignKey(CadItem, on_delete=models.CASCADE, related_name='relacoes')
    produto     = models.ForeignKey(CadProduto, on_delete=models.CASCADE, related_name='relacoes')

    class Meta:
        db_table            = 'relacao_item_produto'
        verbose_name        = 'Relação Item-Produto'
        verbose_name_plural = 'Relações Item-Produto'

    def __str__(self):
        return f"{self.item.descricao} - {self.produto.descricao}"

class SolicitacaoCompra(models.Model):
    STATUS_CHOICES = [
        ('em_aberto', 'Em Aberto'),
        ('aprovada', 'Aprovada'),
        ('reprovada', 'Reprovada'),
    ]

    codigo              = models.CharField(max_length=20, unique=True)
    solicitante         = models.ForeignKey(User, on_delete=models.CASCADE)
    fornecedor          = models.ForeignKey(CadFornecedor, db_column='FORNECEDOR', on_delete=models.CASCADE)
    valor_total         = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_solicitacao    = models.DateField(default=timezone.now)
    justificativa       = models.TextField(blank=True)
    status              = models.CharField(max_length=15, choices=STATUS_CHOICES, default='em_aberto')
    data_hora_criacao   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = 'solicitacao_compra'
        ordering            = ['-data_solicitacao']
        verbose_name        = 'Solicitação de Compra'
        verbose_name_plural = 'Solicitações de Compra'

    def __str__(self):
        return f"{self.codigo} - {self.fornecedor.razao}"

class ItensSolicitacaoCompra(models.Model):
    solicitacao     = models.ForeignKey(SolicitacaoCompra, on_delete=models.CASCADE, related_name='itens')
    produto         = models.ForeignKey(CadItem, on_delete=models.CASCADE)
    quantidade      = models.PositiveIntegerField()
    valor_unitario  = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table            = 'itens_solicitacao_compra'
        verbose_name        = 'Item de Solicitação de Compra'
        verbose_name_plural = 'Itens de Solicitação de Compra'

    def __str__(self):
        return f"{self.produto} ({self.quantidade})"


class Movimentacoes(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('emprestimo', 'Empréstimo'),
        ('devolucao', 'Devolução'),
        ('avaria', 'Avaria'),
    ]

    codigo              = models.AutoField(primary_key=True)
    documento           = models.CharField(db_column='DOCUMENTO', max_length=20, default='')
    data_hora           = models.DateTimeField(db_column='DATA_HORA', default=timezone.now)
    data_movimentacao   = models.DateField(db_column='DATA_MOVIMENTACAO')
    produto             = models.ForeignKey(CadProduto, db_column='PRODUTO', default='', on_delete=models.CASCADE)
    quantidade          = models.DecimalField(db_column='QUANTIDADE', max_digits=10, decimal_places=2)
    tipo                = models.CharField(
        db_column='TIPO',
        max_length=10,
        choices=TIPO_CHOICES,
        default='entrada'
    )

    class Meta:
        db_table = 'movimentacoes'

    def __str__(self):
        return f"Movimentação {self.codigo}"

############################################ LOCACAO ####################################################

class Locacao(models.Model):
    codigo          = models.CharField(max_length=50, unique=True)
    cliente         = models.ForeignKey('CadCliente', default='', on_delete=models.CASCADE)
    data            = models.DateField(auto_now_add=True)
    solicitante     = models.CharField(max_length=100, default='', verbose_name='Solicitante')
    inicio          = models.DateField(db_column='DATA_INICIO', default=timezone.now)
    fim             = models.DateField(db_column='DATA_FIM', default=timezone.now)
    dias            = models.DecimalField(max_digits=10, decimal_places=0, editable=False)  # 👈 evita edição manual
    desconto        = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observacoes     = models.TextField(blank=True, null=True)
    pagamento       = models.CharField(max_length=20, choices=[('dinheiro', 'Dinheiro'), ('cartao', 'Cartão'), ('transferencia', 'Transferência')], default='dinheiro')
    status          = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('reprovada', 'Reprovada'), ('aprovada', 'Aprovada'), ('concluida', 'Concluída')], default='pendente')
    total           = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if self.inicio and self.fim:
            delta = (self.fim - self.inicio).days
            # garante que nunca fique negativo
            self.dias = max(delta, 0)
        super().save(*args, **kwargs)

    def possui_itens_com_saldo(self):
        # Itera sobre todos os itens relacionados a esta locação
        for item in self.itens.all():
            # Se encontrar um item com saldo positivo, retorna True e para a busca
            if item.saldo() > 0:
                return True
        # Se o loop terminar e nenhum item com saldo for encontrado, retorna False
        return False

    def __str__(self):
        return f"{self.cliente.razao} - {self.codigo} - {self.data}"

    class Meta:
        db_table            = 'cad_locacao'
        verbose_name        = 'Cadastro de Locação'
        verbose_name_plural = 'Cadastro de Locações'

class ItensLocacao(models.Model):
    locacao         = models.ForeignKey(Locacao, related_name='itens', on_delete=models.CASCADE)
    produto         = models.ForeignKey('CadProduto', on_delete=models.CASCADE)
    item_estoque    = models.ForeignKey('ItensEstoque', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Item de Estoque")
    quantidade      = models.PositiveIntegerField()
    preco           = models.DecimalField(max_digits=10, decimal_places=2)
    combo           = models.ForeignKey('Combo', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Combo de Equipamentos")
    combo_preco     = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço do Combo")

    def __str__(self):
        return f"{self.produto.descricao} x {self.quantidade}"
    
    def saldo(self):
        entregues = EntregaLocacao.objects.filter(
            locacao=self.locacao, produto=self.produto
        ).aggregate(total=models.Sum('quantidade'))['total'] or 0
        return self.quantidade - entregues
    
    def saldo_disponivel_devolucao(self):
        """
        Calcula o saldo disponível para devolução:
        Quantidade Entregue - Quantidade Já Devolvida
        """
        # Quantidade entregue
        entregues = EntregaLocacao.objects.filter(
            locacao=self.locacao, produto=self.produto
        ).aggregate(total=models.Sum('quantidade'))['total'] or 0
        
        # Quantidade já devolvida
        devolvidas = ItemDevolucao.objects.filter(
            item_locacao=self
        ).aggregate(total=models.Sum('quantidade'))['total'] or 0
        
        return entregues - devolvidas

    class Meta:
        db_table            = 'itens_locacao'
        verbose_name        = 'Cadastro de Item de Locação'
        verbose_name_plural = 'Cadastro de Itens de Locação'

class EntregaLocacao(models.Model):
    codigo          = models.CharField(max_length=20)
    locacao         = models.ForeignKey(Locacao, on_delete=models.CASCADE)
    produto         = models.ForeignKey('CadProduto', on_delete=models.CASCADE)
    quantidade      = models.PositiveIntegerField()
    motorista       = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = 'entrega_locacao'
        verbose_name        = 'Entrega Locação'

class ItensEstoque(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('locado', 'Locado'),
        ('manutencao', 'Em Manutenção'),
        ('danificado', 'Danificado'),
    ]
    produto             = models.ForeignKey(CadProduto, on_delete=models.CASCADE)
    codigo              = models.CharField(max_length=20, unique=True, verbose_name="Código do Item")
    numero_serie        = models.CharField(max_length=100, blank=True, null=True, default='')
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    data_ultimo_status  = models.DateTimeField(auto_now=True)
    observacoes         = models.TextField(blank=True, null=True)

    class Meta:
        db_table            = 'itens_estoque'
        verbose_name        = 'Cadastro de Item de Estoque'
        verbose_name_plural = 'Cadastro de Itens de Estoque'
        default_permissions = ()

    def __str__(self):
        return f"{self.codigo} - {self.produto.descricao}"
    
############################################ FINANCEIRO ####################################################
from django.db import models
from django.utils import timezone

class ContaCobranca(models.Model):
    banco           = models.CharField(max_length=20, choices=[
        ('237', '237 - Bradesco'),
        ('033', '033 - Santander'),
        ('341', '341 - Banco Itaú'),
        ('001', '001 - Banco do Brasil'),
        ('756', '756 - Sicoob'),
        ('748', '748 - Sicredi'),
        ('104', '104 - Caixa Econômica'),
        ('077', '077 - Banco Inter'),
        ('364', '364 - EFÍ'),
        ('085', '085 - Alios'),
        ('136', '136 - UNICRED'),
        ('070', '070 - Banco Brasilia (BSB)'),
        ('041', '041 - Banco Barisul'),
        ('208', '208 - BTG'),
        ('336', '336 - C6')
    ])
    numero          = models.CharField(max_length=20, unique=True)
    digito          = models.CharField(max_length=1)
    convenio        = models.CharField(max_length=20)
    carteira        = models.CharField(max_length=2)

    class Meta:
        db_table            = 'conta_cobranca'
        verbose_name        = 'Conta de Cobrança'
    
    def __str__(self):
        return f"{self.banco}"

class CondicaoCobranca(models.Model):
    codigo          = models.CharField(max_length=20, unique=True)
    vencimento_dias = models.IntegerField()
    juros           = models.DecimalField(max_digits=10, decimal_places=2)
    multa           = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table            = 'condicao_cobraca'
        verbose_name        = 'Condição de Cobrança'
    
    def __str__(self):
        return f"{self.vencimento_dias} dias"

class InstrucaoCobranca(models.Model):
    codigo          = models.CharField(max_length=20, unique=True)
    mensagem1       = models.CharField(max_length=200)
    mensagem2       = models.CharField(max_length=200)
    mensagem3       = models.CharField(max_length=200)
    local_pagamento = models.CharField(max_length=200, default = '')

    class Meta:
        db_table            = 'instrucao_cobranca'
        verbose_name        = 'Instrução de Cobrança'
    
    def __str__(self):
        return f"{self.codigo}"

class ClienteCobranca(models.Model):
    cliente         = models.ForeignKey('CadCliente', on_delete=models.CASCADE)
    conta           = models.ForeignKey('ContaCobranca', on_delete=models.CASCADE)
    condicao        = models.ForeignKey('CondicaoCobranca', on_delete=models.CASCADE)
    instrucao       = models.ForeignKey('InstrucaoCobranca', on_delete=models.CASCADE)

    class Meta:
        db_table            = 'cliente_cobranca'
        verbose_name        = 'Relacionamento do Cliente com a Cobrança'


class ContasReceber(models.Model):
    cliente         = models.ForeignKey('CadCliente', on_delete=models.CASCADE)
    locacao         = models.ForeignKey('Locacao', on_delete=models.CASCADE, related_name='titulos')
    descricao       = models.CharField(max_length=255, default='', blank=True)
    valor_desconto  = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_total     = models.DecimalField(max_digits=10, decimal_places=2)
    data_emissao    = models.DateField(default=timezone.now)
    data_vencimento = models.DateField()
    data_pagamento  = models.DateField(null=True, blank=True)
    status          = models.CharField(max_length=20, choices=[
        ('aberto', 'Em Aberto'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado')
    ], default='aberto')
    forma_pagamento = models.CharField(max_length=20, choices=[
        ('dinheiro', 'Dinheiro'),
        ('cartao', 'Cartão'),
        ('pix', 'Pix'),
        ('boleto', 'Boleto')
    ], default='boleto')
    link_boleto     = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Título {self.pk} - {self.cliente.razao} - R$ {self.valor_total}"
    
    class Meta:
        db_table            = 'contas_receber'
        verbose_name        = 'Conta a Receber'
        verbose_name_plural = 'Contas a Receber'
        default_permissions = ()

class ContasPagar(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_aprovacao', 'Em aprovação'),
        ('pago', 'Pago'),
        ('atrasado', 'Atrasado'),
        ('cancelado', 'Cancelado'),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('pix', 'PIX'),
        ('transferencia', 'Transferência'),
        ('especie', 'Espécie'),
        ('boleto', 'Boleto'),
        ('debito_em_conta', 'Débito em Conta'),
    ]
    
    CLASSIFICACAO_DESPESA_CHOICES = [
        ('compra', 'Compra'),
        ('cartao_credito', 'Cartão de crédito'),
        ('emprestimo_encargos', 'Empréstimo encargos'),
        ('contrato_servicos', 'Contrato de serviços'),
        ('emprestimos_bancarios', 'Empréstimos bancários'),
        ('despesas_administrativas', 'Despesas administrativas'),
    ]

    solicitacao     = models.ForeignKey('SolicitacaoCompra', on_delete=models.CASCADE, related_name='contas_pagar', null=True, blank=True)
    fornecedor      = models.ForeignKey('CadFornecedor', on_delete=models.CASCADE, null=True, blank=True)
    centro_custo    = models.ForeignKey(CentroCusto, on_delete=models.CASCADE, verbose_name="Centro de Custo", null=True, blank=True)
    descricao       = models.CharField(max_length=200, help_text="Descrição do pagamento ou serviço")
    valor           = models.DecimalField(max_digits=12, decimal_places=2)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES, verbose_name="Forma de Pagamento", blank=True, null=True)
    quantidade_parcelas = models.IntegerField(verbose_name="Quantidade de Parcelas", default=1, help_text="Total de parcelas")
    parcela_atual   = models.IntegerField(verbose_name="Parcela Atual", default=1, help_text="Número da parcela atual")
    data_emissao    = models.DateField(default=timezone.now)
    data_vencimento = models.DateField()
    data_pagamento  = models.DateField(blank=True, null=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes     = models.TextField(blank=True, null=True)
    anexo           = models.FileField(upload_to='contas_pagar/anexos/', blank=True, null=True, verbose_name="Anexo")
    aprovado        = models.BooleanField(default=False, verbose_name="Aprovado")
    comprovante     = models.FileField(upload_to='contas_pagar/comprovantes/', blank=True, null=True, verbose_name="Comprovante de Pagamento")
    classificacao_despesa = models.CharField(max_length=30, choices=CLASSIFICACAO_DESPESA_CHOICES, verbose_name="Classificação de Despesa", blank=True, null=True)
    recorrente      = models.BooleanField(default=False, verbose_name="Recorrente")

    class Meta:
        db_table            = 'contas_pagar'
        verbose_name        = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        default_permissions = ()

    def __str__(self):
        fornecedor_str = self.fornecedor.razao if self.fornecedor else "Sem fornecedor"
        return f"{fornecedor_str} - R${self.valor} - {self.get_status_display()}"

    class Meta:
        ordering = ['data_vencimento']

############################################ MANUTENCACAO ####################################################

# Etapas que podem ser configuradas (ex: Cadastro: revisão, teste, limpeza, etc.)
from django.db import models
from django.utils import timezone

# Fluxo de manutenção (ex: "Pintura", "Lubrificação", etc.)
class FluxoManutencao(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        db_table        = 'fluxos_manutencao'
        verbose_name    = 'Cadastro de Fluxo de Manutenção'
        verbose_name    = 'Cadastro de Fluxos de Manutenção'

    def __str__(self):
        return self.nome


# Etapas associadas a cada fluxo
class EtapaManutencao(models.Model):
    fluxo       = models.ForeignKey(FluxoManutencao, on_delete=models.CASCADE, related_name='etapas')
    nome        = models.CharField(max_length=100)
    descricao   = models.TextField(blank=True, null=True)
    ordem       = models.PositiveIntegerField()
    prazo_dias  = models.PositiveIntegerField(help_text="Prazo para concluir a etapa em dias")

    class Meta:
        db_table            = 'etapas_manutencao'
        ordering            = ['ordem']
        verbose_name        = 'Cadastro de Etapa de Manutenção'
        verbose_name_plural = 'Cadastro de Etapas de Manutenção'

    def __str__(self):
        return f"{self.ordem} - {self.nome}"


# Produto em manutenção (utilizando modelo ItensEstoque como exemplo)
class Manutencao(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
    ]
    produto     = models.ForeignKey('ItensEstoque', on_delete=models.CASCADE)
    fluxo       = models.ForeignKey(FluxoManutencao, on_delete=models.CASCADE)
    data_inicio = models.DateField(default=timezone.now)
    observacoes = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    class Meta:
        db_table            = 'manutencoes'
        verbose_name        = 'Cadastro de Manutenção'
        verbose_name_plural = 'Cadastro de Manutenções'

    def __str__(self):
        return f"Manutenção {self.id} - {self.produto}"


# Execução de cada etapa para uma manutenção
class EtapaManutencaoExecutada(models.Model):
    manutencao      = models.ForeignKey(Manutencao, on_delete=models.CASCADE, related_name='etapas')
    etapa           = models.ForeignKey(EtapaManutencao, on_delete=models.CASCADE)
    data_prevista   = models.DateField()
    data_conclusao  = models.DateField(null=True, blank=True)
    status          = models.CharField(
        max_length=20,
        choices=[('pendente', 'Pendente'), ('concluida', 'Concluída')],
        default='pendente'
    )

    class Meta:
        default_permissions = ()
        db_table            = 'etapa_manutencao_executada'
        ordering            = ['etapa__ordem']
        verbose_name        = 'Etapa de Manutenção Executada'
        verbose_name_plural = 'Etapas de Manutenção Executada'

    def __str__(self):
        return f"{self.etapa.nome} ({self.status})"

##################################### DEVOLUCAO #######################################

from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone


ESTADO_CHOICES = (
    ("bom", "Bom"),
    ("danificado", "Danificado"),
    ("perdido", "Perdido"),
)


class Devolucao(models.Model):
    """
    Representa a devolução de uma locação.
    """

    locacao = models.ForeignKey(
        'Locacao',
        on_delete=models.CASCADE,
        related_name='devolucoes',
        verbose_name="Locação",
        null=True,
        blank=True
    )
    data_devolucao = models.DateField(default=timezone.now, verbose_name="Data de devolução")
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Responsável pela devolução",
    )
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    multa_por_atraso = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    custo_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    finalizada = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Devolução"
        verbose_name_plural = "Devoluções"
        ordering = ["-data_devolucao", "-created_at"]

    def __str__(self):
        return f"Devolução #{self.pk} - Locação {self.locacao.codigo}"

    def calcular_multa_por_atraso(self, valor_por_dia=None):
        """
        Calcula multa por atraso simples: valor fixo por dia de atraso.
        """
        data_prevista = self.locacao.fim
        dias_atraso = (self.data_devolucao - data_prevista).days
        if dias_atraso <= 0:
            return Decimal("0.00")

        if valor_por_dia:
            return (Decimal(dias_atraso) * Decimal(valor_por_dia)).quantize(Decimal("0.01"))

        return Decimal("0.00")

    def finalizar(self, *, multa_valor_por_dia=None, commit=True):
        """
        Finaliza a devolução, calcula custos e marca como finalizada.
        """
        multa = self.calcular_multa_por_atraso(valor_por_dia=multa_valor_por_dia)
        self.multa_por_atraso = multa

        total = multa
        for item in self.itens.select_related("item_locacao").all():
            item.processar_item()
            total += item.custo_adicional

        self.custo_total = total.quantize(Decimal("0.01"))
        self.finalizada = True
        if commit:
            self.save()

        return self.custo_total


class ItemDevolucao(models.Model):
    """
    Cada linha de item devolvido.
    """

    devolucao = models.ForeignKey(Devolucao, on_delete=models.CASCADE, related_name="itens")
    item_locacao = models.ForeignKey(
        "ItensLocacao",
        on_delete=models.PROTECT,
        related_name="devolucoes_item",
        verbose_name="Item da locação",
    )
    # Item de estoque específico devolvido (quando estado não é "bom")
    item_estoque = models.ForeignKey(
        "ItensEstoque",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="devolucoes_item_estoque",
        verbose_name="Item de Estoque Específico"
    )
    quantidade = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default="bom")

    custo_adicional = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    encaminhado_manutencao = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True)
    
    # Campo para foto do item
    foto_item = models.ImageField(upload_to='devolucoes/fotos/', blank=True, null=True, verbose_name="Foto do Item")
    
    # Data específica de devolução deste item
    data_devolucao = models.DateField(default=timezone.now, verbose_name="Data de Devolução")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item de Devolução"
        verbose_name_plural = "Itens de Devolução"

    def __str__(self):
        return f"ItemDevolucao #{self.pk} - {self.item_locacao.produto.descricao} ({self.estado})"

############################ COMBO DE EQUIPAMENTOS ############################
class Combo(models.Model):
    nome        = models.CharField(max_length=200)
    descricao   = models.TextField(blank=True, null=True)
    preco       = models.DecimalField(db_column='PRECO', max_digits=10, decimal_places=2)
    custo       = models.BooleanField(default=False)

    class Meta:
        db_table            = 'combo'
        verbose_name        = 'Combo de Equipamentos'
        verbose_name_plural = 'Combos de Equipamentos'

    def __str__(self):
        return self.nome

class ComboItem(models.Model):
    combo       = models.ForeignKey(Combo, on_delete=models.CASCADE, related_name="itens")
    produto     = models.ForeignKey(CadProduto, on_delete=models.PROTECT)
    quantidade  = models.PositiveIntegerField()

    class Meta:
        db_table            = 'combo_item'
        verbose_name        = 'Item do Combo'
        verbose_name_plural = 'Itens do Combo'

    def __str__(self):
        return f"{self.quantidade}x {self.produto.descricao}"

############################ TROCA DE EQUIPAMENTOS ############################
class TrocaEquipamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
        ('concluida', 'Concluída'),
    ]
    
    locacao             = models.ForeignKey(Locacao, on_delete=models.CASCADE, related_name='trocas_equipamentos')
    data_solicitacao    = models.DateTimeField(auto_now_add=True)
    data_aprovacao      = models.DateTimeField(null=True, blank=True)
    usuario_solicitante = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='trocas_solicitadas')
    usuario_aprovador   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='trocas_aprovadas')
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes         = models.TextField(blank=True, null=True)
    valor_original      = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor total da locação original")
    valor_novo          = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor total após a troca")
    diferenca_valor     = models.DecimalField(max_digits=10, decimal_places=2, editable=False, help_text="Diferença entre novo e original")
    titulo_gerado       = models.ForeignKey(ContasReceber, on_delete=models.SET_NULL, null=True, blank=True, related_name='troca_equipamento')
    
    def save(self, *args, **kwargs):
        # Calcula automaticamente a diferença
        self.diferenca_valor = self.valor_novo - self.valor_original
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Troca #{self.pk} - Locação {self.locacao.codigo} - {self.status}"
    
    class Meta:
        db_table            = 'troca_equipamento'
        verbose_name        = 'Troca de Equipamento'
        verbose_name_plural = 'Trocas de Equipamentos'
        ordering            = ['-data_solicitacao']

class ItemTrocaEquipamento(models.Model):
    """
    Registra os itens que foram removidos e adicionados em uma troca
    """
    troca               = models.ForeignKey(TrocaEquipamento, on_delete=models.CASCADE, related_name='itens')
    item_locacao_original = models.ForeignKey(ItensLocacao, on_delete=models.SET_NULL, null=True, blank=True, related_name='trocas_saidas')
    
    # Equipamento removido
    produto_removido    = models.ForeignKey(CadProduto, on_delete=models.SET_NULL, null=True, blank=True, related_name='trocas_saidas', verbose_name="Produto Removido")
    quantidade_removida = models.PositiveIntegerField()
    preco_removido      = models.DecimalField(max_digits=10, decimal_places=2)
    item_estoque_removido = models.ForeignKey(ItensEstoque, on_delete=models.SET_NULL, null=True, blank=True, related_name='trocas_saidas')
    
    # Equipamento adicionado
    produto_adicionado  = models.ForeignKey(CadProduto, on_delete=models.SET_NULL, null=True, blank=True, related_name='trocas_entradas', verbose_name="Produto Adicionado")
    quantidade_adicionada = models.PositiveIntegerField()
    preco_adicionado    = models.DecimalField(max_digits=10, decimal_places=2)
    item_estoque_adicionado = models.ForeignKey(ItensEstoque, on_delete=models.SET_NULL, null=True, blank=True, related_name='trocas_entradas')
    
    def diferenca_unitaria(self):
        """Calcula a diferença unitária entre produto removido e adicionado"""
        return self.preco_adicionado - self.preco_removido
    
    def diferenca_total(self):
        """Calcula a diferença total para este item"""
        return (self.preco_adicionado * self.quantidade_adicionada) - (self.preco_removido * self.quantidade_removida)
    
    def __str__(self):
        return f"Troca #{self.troca.pk} - {self.produto_removido.descricao if self.produto_removido else 'N/A'} → {self.produto_adicionado.descricao if self.produto_adicionado else 'N/A'}"
    
    class Meta:
        db_table            = 'item_troca_equipamento'
        verbose_name        = 'Item de Troca de Equipamento'
        verbose_name_plural = 'Itens de Troca de Equipamento'
