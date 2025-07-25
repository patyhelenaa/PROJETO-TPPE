import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from usuarios.models import Profile
from ciclos.models import Ciclo
from sintomas.models import (
    Fisico, Humor, Libido, Secrecao, Intensidade, HumorEnum, TexturaSecrecao
)
from datetime import date


@pytest.fixture
def usuario_e_ciclo():
    user = User.objects.create_user(
        username="teste",
        email="teste@exemplo.com",
        password="senha123"
    )
    Profile.objects.create(
        user=user,
        nome="Teste",
        data_nascimento=date(2000, 1, 1),
        peso=60.0
    )
    ciclo = Ciclo.objects.create(
        usuario=user,
        data=date(2025, 6, 24),
        dia_menstruada=True,
        duracao_ciclo=28,
        duracao_menstruacao=5,
        fluxo_menstrual="MODERADO"
    )
    return user, ciclo


@pytest.mark.django_db
def test_criar_fisico(usuario_e_ciclo):
    user, ciclo = usuario_e_ciclo
    client = APIClient()
    client.force_authenticate(user=user)
    data = {
        "intensidade": Intensidade.LEVE,
        "descricao": "Dor leve",
        "nome_sintoma": "Dor muscular",
        "data": "2025-06-24",
        "pratica": True,
        "remedio_tomado": "Nenhum"
    }
    response = client.post("/api/fisico/", data, format="json")
    assert response.status_code == 201
    assert response.data["nome_sintoma"] == "Dor muscular"
    assert response.data["pratica"] is True
    assert response.data["ciclo"] == ciclo.id


@pytest.mark.django_db
def test_listar_fisico(usuario_e_ciclo):
    user, ciclo = usuario_e_ciclo
    Fisico.objects.create(
        intensidade=Intensidade.MODERADO,
        descricao="Dor moderada",
        nome_sintoma="Dor nas costas",
        data=date.today(),
        pratica=False,
        remedio_tomado="Paracetamol",
        ciclo=ciclo
    )
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/fisico/")
    assert response.status_code == 200
    assert len(response.data) > 0
    assert any(f["nome_sintoma"] == "Dor nas costas" for f in response.data)


@pytest.mark.django_db
def test_criar_humor(usuario_e_ciclo):
    user, ciclo = usuario_e_ciclo
    client = APIClient()
    client.force_authenticate(user=user)
    data = {
        "intensidade": Intensidade.INTENSO,
        "descricao": "Senti tristeza profunda",
        "nome_sintoma": "Tristeza",
        "data": "2025-06-24",
        "gatilho": "Discussão",
        "humor": HumorEnum.TRISTEZA
    }
    response = client.post("/api/humor/", data, format="json")
    assert response.status_code == 201
    assert response.data["humor"] == HumorEnum.TRISTEZA
    assert response.data["ciclo"] == ciclo.id


@pytest.mark.django_db
def test_listar_humor(usuario_e_ciclo):
    user, ciclo = usuario_e_ciclo
    Humor.objects.create(
        intensidade=Intensidade.LEVE,
        descricao="Alegria leve",
        nome_sintoma="Felicidade",
        data=date.today(),
        gatilho="Boa notícia",
        humor=HumorEnum.FELICIDADE,
        ciclo=ciclo
    )
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/humor/")
    assert response.status_code == 200
    assert len(response.data) > 0
    assert any(h["nome_sintoma"] == "Felicidade" for h in response.data)


@pytest.mark.django_db
def test_criar_libido(usuario_e_ciclo):
    user, ciclo = usuario_e_ciclo
    client = APIClient()
    client.force_authenticate(user=user)
    data = {
        "intensidade": Intensidade.MODERADO,
        "descricao": "Teve relações com parceiro",
        "nome_sintoma": "Libido",
        "data": "2025-06-24",
        "relacoes_com_parceiro": True,
        "relacoes_sem_parceiro": False
    }
    response = client.post("/api/libido/", data, format="json")
    assert response.status_code == 201
    assert response.data["relacoes_com_parceiro"] is True
    assert response.data["ciclo"] == ciclo.id


@pytest.mark.django_db
def test_listar_libido(usuario_e_ciclo):
    user, ciclo = usuario_e_ciclo
    Libido.objects.create(
        intensidade=Intensidade.LEVE,
        descricao="Sem relações",
        nome_sintoma="Libido baixa",
        data=date.today(),
        relacoes_com_parceiro=False,
        relacoes_sem_parceiro=False,
        ciclo=ciclo
    )
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/libido/")
    assert response.status_code == 200
    assert len(response.data) > 0
    assert any(lbd["nome_sintoma"] == "Libido baixa" for lbd in response.data)


@pytest.mark.django_db
def test_criar_secrecao(usuario_e_ciclo):
    user, ciclo = usuario_e_ciclo
    client = APIClient()
    client.force_authenticate(user=user)
    data = {
        "intensidade": Intensidade.MUITO_INTENSO,
        "descricao": "Secreção pegajosa",
        "nome_sintoma": "Secreção vaginal",
        "data": "2025-06-24",
        "textura": TexturaSecrecao.PEGAJOSA,
        "remedio_tomado": "Nenhum"
    }
    response = client.post("/api/secrecao/", data, format="json")
    assert response.status_code == 201
    assert response.data["textura"] == TexturaSecrecao.PEGAJOSA
    assert response.data["ciclo"] == ciclo.id


@pytest.mark.django_db
def test_listar_secrecao(usuario_e_ciclo):
    user, ciclo = usuario_e_ciclo
    Secrecao.objects.create(
        intensidade=Intensidade.MODERADO,
        descricao="Secreção cremosa",
        nome_sintoma="Secreção vaginal",
        data=date.today(),
        textura=TexturaSecrecao.CREMOSA,
        remedio_tomado="Pomada",
        ciclo=ciclo
    )
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/secrecao/")
    assert response.status_code == 200
    assert len(response.data) > 0
    assert any(sec["descricao"] == "Secreção cremosa" for sec in response.data)
