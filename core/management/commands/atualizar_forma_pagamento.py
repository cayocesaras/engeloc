from django.core.management.base import BaseCommand
from core.models import ContasPagar


class Command(BaseCommand):
    help = 'Atualiza o campo forma_pagamento para "boleto" em todos os registros existentes de ContasPagar'

    def add_arguments(self, parser):
        parser.add_argument(
            '--forma',
            type=str,
            default='boleto',
            help='Forma de pagamento a ser definida (padrão: boleto)',
        )

    def handle(self, *args, **options):
        forma_pagamento = options['forma']
        
        # Valida se a forma de pagamento é válida
        formas_validas = ['boleto', 'nf', 'transferencia']
        if forma_pagamento not in formas_validas:
            self.stdout.write(
                self.style.ERROR(
                    f'Forma de pagamento inválida. Use uma das opções: {", ".join(formas_validas)}'
                )
            )
            return
        
        # Busca todos os registros que não têm forma_pagamento definido (None ou vazio)
        contas_sem_forma = ContasPagar.objects.filter(forma_pagamento__isnull=True)
        
        total_contas = contas_sem_forma.count()
        
        if total_contas == 0:
            self.stdout.write(
                self.style.SUCCESS('Todos os registros já possuem forma de pagamento definida.')
            )
            return
        
        # Atualiza os registros
        contas_atualizadas = contas_sem_forma.update(forma_pagamento=forma_pagamento)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ {contas_atualizadas} registro(s) atualizado(s) com forma de pagamento: {forma_pagamento}'
            )
        )

