from django.db import models
from ciclos.models import Ciclo

class Intensidade(models.TextChoices):
    LEVE = 'LEVE', 'Leve'
    MODERADO = 'MODERADO', 'Moderado'
    INTENSO = 'INTENSO', 'Intenso'
    MUITO_INTENSO = 'MUITO_INTENSO', 'Muito Intenso'

class HumorEnum(models.TextChoices):
    FELICIDADE = 'FELICIDADE', 'Felicidade'
    TRISTEZA = 'TRISTEZA', 'Tristeza'
    IRRITACAO = 'IRRITACAO', 'Irritação'
    ANSIEDADE = 'ANSIEDADE', 'Ansiedade'

class TexturaSecrecao(models.TextChoices):
    AQUOSA = 'AQUOSA', 'Aquosa'
    CREMOSA = 'CREMOSA', 'Cremosa'
    ELASTICA = 'ELASTICA', 'Elástica'
    PEGAJOSA = 'PEGAJOSA', 'Pegajosa'


class Sintoma(models.Model):
    intensidade = models.CharField(max_length=15, choices=Intensidade.choices)
    descricao = models.TextField(blank=True, null=True)
    nome_sintoma = models.CharField(max_length=100)
    data = models.DateField()

    class Meta:
        abstract = True


class Fisico(Sintoma):
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, related_name='fisicos')
    pratica = models.BooleanField(default=False)  # type: ignore
    remedio_tomado = models.CharField(max_length=255, blank=True, null=True)


class Humor(Sintoma):
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, related_name='humores')
    gatilho = models.CharField(max_length=255, blank=True, null=True)
    humor = models.CharField(max_length=15, choices=HumorEnum.choices)


class Libido(Sintoma):
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, related_name='libidos')
    relacoes_com_parceiro = models.BooleanField(default=False)  # type: ignore
    relacoes_sem_parceiro = models.BooleanField(default=False)  # type: ignore


class Secrecao(Sintoma):
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, related_name='secrecoes')
    textura = models.CharField(max_length=15, choices=TexturaSecrecao.choices)
    remedio_tomado = models.CharField(max_length=255, blank=True, null=True)
