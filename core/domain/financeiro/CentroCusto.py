from django.db import models

class CentroCusto(models.Model):
    codigo = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=20, default='')
    
    def __str__(self):
        return self.descricao
    
    class Meta:
        verbose_name = 'Centro de Custo'
        verbose_name_plural = 'Centros de Custo'