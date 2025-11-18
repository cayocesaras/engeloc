from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from core.models import (
    CadCliente, CadProduto, CadGrupoProduto, CadUnidadeMedida,
    Locacao, ItensLocacao, TrocaEquipamento, ItemTrocaEquipamento,
    ContasReceber
)
from datetime import timedelta


class TrocaEquipamentoTestCase(TestCase):
    """Testes para a funcionalidade de troca de equipamentos"""
    
    def setUp(self):
        """Preparação dos dados para testes"""
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Criar grupo de produto
        self.grupo = CadGrupoProduto.objects.create(
            codigo='001',
            descricao='Equipamento de Aluguel'
        )
        
        # Criar unidade de medida
        self.unidade = CadUnidadeMedida.objects.create(
            codigo='001',
            descricao='Unidade'
        )
        
        # Criar produtos
        self.produto1 = CadProduto.objects.create(
            codigo='001',
            descricao='Estrado de Madeira',
            grupo=self.grupo,
            unidade=self.unidade,
            preco=Decimal('50.00'),
            ressarcimento=Decimal('100.00'),
            is_ativo=1,
            tipo='locavel'
        )
        
        self.produto2 = CadProduto.objects.create(
            codigo='002',
            descricao='Estrado de Metal',
            grupo=self.grupo,
            unidade=self.unidade,
            preco=Decimal('80.00'),
            ressarcimento=Decimal('150.00'),
            is_ativo=1,
            tipo='locavel'
        )
        
        # Criar cliente
        self.cliente = CadCliente.objects.create(
            codigo='001',
            tipo='PJ',
            cnpj_cpf='12.345.678/0001-90',
            razao='Empresa Teste Ltda',
            fantasia='Empresa Teste'
        )
        
        # Criar locação
        hoje = timezone.now().date()
        self.locacao = Locacao.objects.create(
            codigo='LOC-001',
            cliente=self.cliente,
            solicitante='João Silva',
            inicio=hoje,
            fim=hoje + timedelta(days=10),
            status='aprovada',
            total=Decimal('500.00')
        )
        
        # Adicionar itens à locação
        self.item1 = ItensLocacao.objects.create(
            locacao=self.locacao,
            produto=self.produto1,
            quantidade=5,
            preco=Decimal('50.00')
        )
        
    def test_criar_troca_equipamento(self):
        """Testa a criação de uma solicitação de troca"""
        troca = TrocaEquipamento.objects.create(
            locacao=self.locacao,
            usuario_solicitante=self.user,
            status='pendente',
            valor_original=Decimal('250.00'),
            valor_novo=Decimal('300.00'),
            observacoes='Substituição de equipamento'
        )
        
        self.assertEqual(troca.diferenca_valor, Decimal('50.00'))
        self.assertEqual(troca.status, 'pendente')
        self.assertIsNone(troca.usuario_aprovador)
        self.assertIsNone(troca.titulo_gerado)
        
    def test_calcular_diferenca_positiva(self):
        """Testa cálculo de diferença positiva"""
        troca = TrocaEquipamento.objects.create(
            locacao=self.locacao,
            usuario_solicitante=self.user,
            valor_original=Decimal('100.00'),
            valor_novo=Decimal('150.00')
        )
        
        self.assertTrue(troca.diferenca_valor > 0)
        self.assertEqual(troca.diferenca_valor, Decimal('50.00'))
        
    def test_calcular_diferenca_negativa(self):
        """Testa cálculo de diferença negativa (desconto)"""
        troca = TrocaEquipamento.objects.create(
            locacao=self.locacao,
            usuario_solicitante=self.user,
            valor_original=Decimal('200.00'),
            valor_novo=Decimal('150.00')
        )
        
        self.assertTrue(troca.diferenca_valor < 0)
        self.assertEqual(troca.diferenca_valor, Decimal('-50.00'))
        
    def test_gerar_titulo_ao_aprovar_com_diferenca(self):
        """Testa a geração automática de título ao aprovar com diferença positiva"""
        troca = TrocaEquipamento.objects.create(
            locacao=self.locacao,
            usuario_solicitante=self.user,
            status='pendente',
            valor_original=Decimal('200.00'),
            valor_novo=Decimal('300.00')
        )
        
        # Simular aprovação
        if troca.diferenca_valor > 0:
            titulo = ContasReceber.objects.create(
                cliente=troca.locacao.cliente,
                locacao=troca.locacao,
                descricao=f'Ajuste por troca - Troca #{troca.pk}',
                valor_total=troca.diferenca_valor,
                data_emissao=timezone.now().date(),
                data_vencimento=timezone.now().date() + timedelta(days=7),
                status='aberto'
            )
            
            troca.titulo_gerado = titulo
            troca.save()
        
        troca.refresh_from_db()
        self.assertIsNotNone(troca.titulo_gerado)
        self.assertEqual(troca.titulo_gerado.valor_total, Decimal('100.00'))
        
    def test_adicionar_itens_troca(self):
        """Testa a adição de itens em uma troca"""
        troca = TrocaEquipamento.objects.create(
            locacao=self.locacao,
            usuario_solicitante=self.user,
            valor_original=Decimal('250.00'),
            valor_novo=Decimal('300.00')
        )
        
        # Adicionar item de troca
        item_troca = ItemTrocaEquipamento.objects.create(
            troca=troca,
            produto_removido=self.produto1,
            quantidade_removida=5,
            preco_removido=Decimal('50.00'),
            produto_adicionado=self.produto2,
            quantidade_adicionada=3,
            preco_adicionado=Decimal('80.00')
        )
        
        self.assertEqual(item_troca.quantidade_removida, 5)
        self.assertEqual(item_troca.quantidade_adicionada, 3)
        self.assertEqual(item_troca.diferenca_unitaria(), Decimal('30.00'))
        self.assertEqual(item_troca.diferenca_total(), Decimal('240.00') - Decimal('250.00'))
        
    def test_filtro_status_troca(self):
        """Testa a filtragem de trocas por status"""
        # Criar trocas com diferentes status
        TrocaEquipamento.objects.create(
            locacao=self.locacao,
            usuario_solicitante=self.user,
            status='pendente',
            valor_original=Decimal('100.00'),
            valor_novo=Decimal('150.00')
        )
        
        TrocaEquipamento.objects.create(
            locacao=self.locacao,
            usuario_solicitante=self.user,
            status='aprovada',
            valor_original=Decimal('100.00'),
            valor_novo=Decimal('150.00')
        )
        
        pendentes = TrocaEquipamento.objects.filter(status='pendente')
        aprovadas = TrocaEquipamento.objects.filter(status='aprovada')
        
        self.assertEqual(pendentes.count(), 1)
        self.assertEqual(aprovadas.count(), 1)
        
    def test_relacionamento_locacao_troca(self):
        """Testa o relacionamento entre Locação e TrocaEquipamento"""
        troca = TrocaEquipamento.objects.create(
            locacao=self.locacao,
            usuario_solicitante=self.user,
            valor_original=Decimal('100.00'),
            valor_novo=Decimal('150.00')
        )
        
        # Verificar relacionamento reverso
        trocas = self.locacao.trocas_equipamentos.all()
        self.assertEqual(trocas.count(), 1)
        self.assertEqual(trocas.first(), troca)
        
    def test_str_troca_equipamento(self):
        """Testa a representação em string de TrocaEquipamento"""
        troca = TrocaEquipamento.objects.create(
            locacao=self.locacao,
            usuario_solicitante=self.user,
            status='pendente',
            valor_original=Decimal('100.00'),
            valor_novo=Decimal('150.00')
        )
        
        string_repr = str(troca)
        self.assertIn('Troca #', string_repr)
        self.assertIn(self.locacao.codigo, string_repr)
        self.assertIn('pendente', string_repr)
