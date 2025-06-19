from django.db import models
from usuarios.models import Usuario  

class Ciclo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ciclos')
    data = models.DateField() 
    dia_menstruada = models.BooleanField()
    duracao_ciclo = models.PositiveIntegerField()  
    duracao_menstruacao = models.PositiveIntegerField() 
    fluxo_menstrual = models.CharField(max_length=20, choices=[
        ('LEVE', 'Leve'),
        ('MODERADO', 'Moderado'),
        ('INTENSO', 'Intenso'),
        ('MUITO_INTENSO', 'Muito Intenso'),
    ])

    def __str__(self):
        return f"Ciclo do usuário {self.usuario.nome} em {self.data}"

    class Meta:
        db_table = 'ciclo'
