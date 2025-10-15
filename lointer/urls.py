"""
URL configuration for lointer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('acesso/criar-papel/', views.CriarGrupoEPermissoesView.as_view(), name='criar_grupo_e_permissoes'),
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('buscar-empresa/', views.buscar_empresa, name='buscar_empresa'),
    path('empresas/', views.cad_empresa, name='empresas'),
    path('clientes/', views.cad_cliente, name='clientes'),
    path("listagem_clientes/", views.listagem_clientes, name="listagem_clientes"),
    path('fornecedores/', views.cad_fornecedor, name='fornecedores'),
    path('grupo_produtos/', views.cad_grupo_produto, name='grupo_produtos'),
    path('unidade_medida/', views.cad_unidade_medida, name='unidade_medida'),
    path('almoxarifado/', views.almoxarifado, name='almoxarifados'),
    path('itens_compra/', views.cad_item, name='itens_compra'),
    path('aprovar_compra/', views.aprovar_compra, name='aprovar_compra'),
    path('listagem_itens/', views.listagem_itens, name='listagem_itens'),
    path('aprovar_solicitacao/<int:solicitacao_id>/', views.aprovar_solicitacao, name='aprovar_solicita_compra'),
    path('recusar_solicitacao/<int:solicitacao_id>/', views.recusar_solicitacao, name='recusar_solicita_compra'),
    path('produtos/', views.cad_produto, name='produtos'),
    path('listagem_produtos/', views.listagem_produtos, name='listagem_produtos'),
    path('solicitacoes/', views.cad_solicitacao, name='solicitacoes'),
    path('movimentacoes/', views.movimentacoes, name='movimentacoes'),
    path('entrada/', views.mov_entrada, name='mov_entrada'),
    path("manutencao/aprovar/", views.aprovar_manutencoes, name="aprovar_manutencoes"),
    path("aprova_manutencao/<int:manutencao_id>", views.aprova_manutencao, name="aprova_manutencao"),
    path("manutencao/manutencoes/", views.manutencoes, name="manutencoes"),
    path("manutencao/etapas_manutencao/", views.etapas_manutencao, name="etapas_manutencao"),
    path('manutencao/<int:manutencao_id>/visualizar/', views.visualizar_manutencao, name='visualizar_manutencao'),
    path('manutencao/fluxo', views.fluxo_manutencao, name='fluxo_manutencao'),
    path('manutencao/listagem', views.listagem_manutencao, name='listagem_manutencao'),
    path('manutencao/grade', views.grade_manutencoes, name='grade_manutencoes'),
    path('etapa/<int:etapa_id>/concluir/', views.concluir_etapa, name='concluir_etapa'),
    path("saldos/", views.saldos, name="saldos"),
    path("locacoes/", views.locacoes, name="locacoes"),
    path("locacao/", views.locacao, name="locacao"),
    path("listagem_locacoes/", views.listagem_locacoes, name="listagem_locacoes"),
    path("cotacao/", views.cotacao, name="cotacao"),
    path("aprovar_cotacao/", views.aprovar_cotacao, name="aprovar_cotacao"),
    path('cotacao/<int:locacao_id>',views.imprimir_cotacao, name='imprimir_cotacao'),
    path('locacao/<int:locacao_id>',views.imprimir_espelho, name='imprimir_espelho'),
    path('contrato/<int:locacao_id>',views.imprimir_contrato, name='imprimir_contrato'),
    path('cotacao_locacao/<int:locacao_id>',views.cotacao_locacao, name='cotacao_locacao'),
    path('locacao/<int:locacao_id>/enviar-assinatura/',views.enviar_contrato_para_assinatura,name='enviar_assinatura'),
    path('entrega_locacao', views.entrega_locacao, name="entrega_locacao"),
    path('listagem_cautela_entregas', views.listagem_cautela_entregas, name="listagem_cautela_entregas"),
    path('listagem_cautela_devolucoes', views.listagem_cautela_devolucoes, name="listagem_cautela_devolucoes"),
    path('cautela/excluir/<str:codigo>/', views.excluir_cautela, name='excluir_cautela'),
    path('imprimir_cautela_entrega/<int:locacao_id>',views.imprimir_cautela_entrega, name='imprimir_cautela_entrega'),
    path('imprimir_cautela_devolucao/<int:locacao_id>',views.imprimir_cautela_devolucao, name='imprimir_cautela_devolucao'),
    path('itens_estoque/', views.listar_itens_estoque, name='listar_itens_estoque'),
    path('itens_estoque_locacao/', views.listar_itens_estoque_locacao, name='listar_itens_estoque_locacao'),
    path('itens_estoque/salvar_em_massa/', views.salvar_itens_estoque_em_massa, name='salvar_itens_estoque_em_massa'),
    path('saldo_estoque_produto_item/', views.saldo_estoque_produto_item, name='saldo_estoque_produto_item'),
    path('financeiro/titulos_a_receber/', views.titulos_a_receber, name='titulos_a_receber'),
    path('financeiro/titulos_a_pagar/', views.titulos_a_pagar, name='titulos_a_pagar'),
    path('financeiro/conta_cobranca/', views.cad_conta_cobranca, name='cad_conta_cobranca'),
    path('financeiro/excluir_conta_cobranca/<int:conta_id>/', views.excluir_conta_cobranca, name='excluir_conta_cobranca'),
    path('financeiro/alterar_conta_cobranca/<int:conta_id>/', views.alterar_conta_cobranca, name='alterar_conta_cobranca'),
    path('financeiro/condicao_cobranca/', views.cad_condicao_cobranca, name='cad_condicao_cobranca'),
    path('financeiro/excluir_condicao_cobranca/<int:condicao_id>/', views.excluir_condicao_cobranca, name='excluir_condicao_cobranca'),
    path('financeiro/alterar_condicao_cobranca/<int:condicao_id>/', views.alterar_condicao_cobranca, name='alterar_condicao_cobranca'),
    path('financeiro/instrucao_cobranca/', views.cad_instrucao_cobranca, name='cad_instrucao_cobranca'),
    path('financeiro/excluir_instrucao_cobranca/<int:instrucao_id>/', views.excluir_instrucao_cobranca, name='excluir_instrucao_cobranca'),
    path('financeiro/alterar_instrucao_cobranca/<int:instrucao_id>/', views.alterar_instrucao_cobranca, name='alterar_instrucao_cobranca'),
    path('compras/solicitacaodecompra', views.solicitacaodecompra, name='solicitacaodecompra'),
    path('compras/relacao_item_produto', views.relacao_item_produto, name='relacao_item_produto'),
    path("devolucao/<int:locacao_id>/", views.cad_devolucao, name="cad_devolucao"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)