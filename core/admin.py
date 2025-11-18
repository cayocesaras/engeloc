from django.contrib import admin
from .models import TrocaEquipamento, ItemTrocaEquipamento

# Register your models here.

class ItemTrocaEquipamentoInline(admin.TabularInline):
    model = ItemTrocaEquipamento
    extra = 1

@admin.register(TrocaEquipamento)
class TrocaEquipamentoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'locacao', 'status', 'valor_original', 'valor_novo', 'diferenca_valor', 'data_solicitacao')
    list_filter = ('status', 'data_solicitacao')
    search_fields = ('locacao__codigo', 'locacao__cliente__razao')
    readonly_fields = ('data_solicitacao', 'data_aprovacao', 'diferenca_valor')
    inlines = [ItemTrocaEquipamentoInline]
    fieldsets = (
        ('Informações Gerais', {
            'fields': ('locacao', 'status', 'data_solicitacao', 'data_aprovacao')
        }),
        ('Usuários', {
            'fields': ('usuario_solicitante', 'usuario_aprovador')
        }),
        ('Valores', {
            'fields': ('valor_original', 'valor_novo', 'diferenca_valor')
        }),
        ('Título Gerado', {
            'fields': ('titulo_gerado',)
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
    )
