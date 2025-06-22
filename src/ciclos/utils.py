from .models import Ciclo
from datetime import timedelta


def calcular_duracao_media_ciclos(user):
    ciclos = Ciclo.objects.filter(usuario=user)
    if not ciclos.exists():
        return None
    return sum(c.duracao_ciclo for c in ciclos) / ciclos.count()


def prever_proximo_ciclo(user):
    ciclos = Ciclo.objects.filter(usuario=user).order_by('-data')
    if not ciclos.exists():
        return None
    media = calcular_duracao_media_ciclos(user)
    if media is None:
        return None
    ultimo = ciclos.first()
    return ultimo.data + timedelta(days=int(media))
