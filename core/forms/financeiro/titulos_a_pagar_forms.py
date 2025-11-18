from django import forms
from django.core.exceptions import ValidationError
from core.models import ContasPagar


class CancelarContaPagarForm(forms.Form):
    """
    Formulário para cancelar e excluir uma conta a pagar.
    Segue as melhores práticas do Django:
    - Validação no método clean()
    - Campos apropriados
    - Mensagens de erro personalizadas
    """
    conta_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True,
        label='ID da Conta'
    )
    confirmacao = forms.BooleanField(
        required=True,
        label='Confirmar cancelamento',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        """
        Inicializa o formulário, permitindo passar a instância da conta
        para validação adicional se necessário.
        """
        self.conta = kwargs.pop('conta', None)
        super().__init__(*args, **kwargs)
        
        # Se a conta foi passada, define o valor padrão do campo conta_id
        if self.conta and not self.data:
            self.fields['conta_id'].initial = self.conta.id
    
    def clean_conta_id(self):
        """
        Valida se a conta existe e se pode ser cancelada.
        """
        conta_id = self.cleaned_data.get('conta_id')
        
        if not conta_id:
            raise ValidationError('ID da conta é obrigatório.')
        
        try:
            conta = ContasPagar.objects.get(pk=conta_id)
        except ContasPagar.DoesNotExist:
            raise ValidationError('Conta a pagar não encontrada.')
        
        # Validações de negócio
        if conta.status == 'cancelado':
            raise ValidationError('Esta conta já foi cancelada.')
        
        if conta.status == 'pago':
            raise ValidationError('Não é possível cancelar uma conta já paga.')
        
        # Armazena a conta para uso posterior
        self.conta = conta
        
        return conta_id
    
    def clean_confirmacao(self):
        """
        Valida se o usuário confirmou o cancelamento.
        """
        confirmacao = self.cleaned_data.get('confirmacao')
        
        if not confirmacao:
            raise ValidationError('Você deve confirmar o cancelamento para prosseguir.')
        
        return confirmacao
    
    def save(self):
        """
        Exclui a conta do banco de dados.
        Retorna um dicionário com informações da conta excluída.
        
        Nota: Este método deve ser chamado apenas após a validação do formulário.
        """
        if not hasattr(self, 'cleaned_data') or not self.cleaned_data:
            raise ValueError('O formulário deve ser válido antes de chamar save()')
        
        # Se a conta não foi armazenada durante a validação, busca novamente
        if not hasattr(self, 'conta') or not self.conta:
            conta_id = self.cleaned_data.get('conta_id')
            try:
                self.conta = ContasPagar.objects.get(pk=conta_id)
            except ContasPagar.DoesNotExist:
                raise ValidationError('Conta a pagar não encontrada.')
        
        # Armazena informações antes de excluir para possíveis logs
        conta_info = {
            'id': self.conta.id,
            'fornecedor': str(self.conta.fornecedor) if self.conta.fornecedor else "Sem fornecedor",
            'valor': str(self.conta.valor),
            'descricao': self.conta.descricao
        }
        
        # Exclui a conta
        self.conta.delete()
        
        return conta_info

