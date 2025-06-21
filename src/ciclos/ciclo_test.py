import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from usuarios.models import Profile
from ciclos.models import Ciclo
from datetime import date, timedelta

@pytest.mark.django_db
def test_ciclo_str():
    user = User.objects.create_user(username="teste", email="teste@ex.com", password="senha123")
    Profile.objects.create(user=user, nome="Teste", data_nascimento=date(2000,1,1), peso=60)
    ciclo = Ciclo(usuario=user, data=date(2024, 6, 1), dia_menstruada=True, duracao_ciclo=28, duracao_menstruacao=5, fluxo_menstrual='MODERADO')
    assert str(ciclo) == f"Ciclo do usuário {user.username} em {ciclo.data}"

@pytest.mark.parametrize("duracao,menstruacao,fluxo", [
    (28, 5, 'MODERADO'),
    (30, 6, 'LEVE'),
    (27, 4, 'INTENSO'),
])
@pytest.mark.django_db
def test_criar_ciclo_parametrizado(duracao, menstruacao, fluxo):
    user = User.objects.create_user(username=f"ana{duracao}", email=f"ana{duracao}@example.com", password="senha123")
    Profile.objects.create(user=user, nome="Ana Paula", data_nascimento=date(1995, 4, 10), peso=60.0)
    client = APIClient()
    client.force_authenticate(user=user)
    data = {
        "data": "2025-06-01",
        "dia_menstruada": True,
        "duracao_ciclo": duracao,
        "duracao_menstruacao": menstruacao,
        "fluxo_menstrual": fluxo
    }
    response = client.post("/api/ciclos/", data, format='json')
    assert response.status_code == 201
    assert response.data["duracao_ciclo"] == duracao
    assert response.data["fluxo_menstrual"] == fluxo

@pytest.mark.django_db
def test_criar_ciclo_api():
    user = User.objects.create_user(username="ana", email="ana@example.com", password="senha123")
    Profile.objects.create(user=user, nome="Ana Paula", data_nascimento=date(1995, 4, 10), peso=60.0)
    client = APIClient()
    client.force_authenticate(user=user)
    data = {
        "data": "2025-06-01",
        "dia_menstruada": True,
        "duracao_ciclo": 28,
        "duracao_menstruacao": 5,
        "fluxo_menstrual": "MODERADO"
    }
    response = client.post("/api/ciclos/", data, format='json')
    assert response.status_code == 201
    assert response.data["duracao_ciclo"] == 28
    assert response.data["fluxo_menstrual"] == "MODERADO"
    assert response.data["dia_menstruada"] is True

@pytest.mark.django_db
def test_listar_ciclos_api():
    user = User.objects.create_user(username="ana", email="ana@example.com", password="senha123")
    Profile.objects.create(user=user, nome="Ana Paula", data_nascimento=date(1995, 4, 10), peso=60.0)
    ciclo = Ciclo.objects.create(
        usuario=user,
        data=date(2025, 6, 1),
        dia_menstruada=True,
        duracao_ciclo=28,
        duracao_menstruacao=5,
        fluxo_menstrual="MODERADO"
    )
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/ciclos/")
    assert response.status_code == 200
    assert len(response.data) > 0
    ciclo_id = ciclo.id
    assert any(c["id"] == ciclo_id for c in response.data)

@pytest.mark.django_db
def test_atualizar_ciclo_api():
    user = User.objects.create_user(username="ana", email="ana@example.com", password="senha123")
    Profile.objects.create(user=user, nome="Ana Paula", data_nascimento=date(1995, 4, 10), peso=60.0)
    ciclo = Ciclo.objects.create(
        usuario=user,
        data=date(2025, 6, 1),
        dia_menstruada=True,
        duracao_ciclo=28,
        duracao_menstruacao=5,
        fluxo_menstrual="MODERADO"
    )
    client = APIClient()
    client.force_authenticate(user=user)
    data = {
        "data": "2025-06-01",
        "dia_menstruada": False,
        "duracao_ciclo": 30,
        "duracao_menstruacao": 6,
        "fluxo_menstrual": "INTENSO"
    }
    response = client.put(f"/api/ciclos/{ciclo.id}/", data, format='json')
    assert response.status_code == 200
    assert response.data["duracao_ciclo"] == 30
    assert response.data["fluxo_menstrual"] == "INTENSO"
    assert response.data["dia_menstruada"] is False

@pytest.mark.django_db
def test_deletar_ciclo_api():
    user = User.objects.create_user(username="ana", email="ana@example.com", password="senha123")
    Profile.objects.create(user=user, nome="Ana Paula", data_nascimento=date(1995, 4, 10), peso=60.0)
    ciclo = Ciclo.objects.create(
        usuario=user,
        data=date(2025, 6, 1),
        dia_menstruada=True,
        duracao_ciclo=28,
        duracao_menstruacao=5,
        fluxo_menstrual="MODERADO"
    )
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.delete(f"/api/ciclos/{ciclo.id}/")
    assert response.status_code == 204
    assert Ciclo.objects.count() == 0

# --- Testes de integração dos endpoints customizados ---
@pytest.mark.django_db
def test_ciclo_ultimo_endpoint():
    user = User.objects.create_user(username="ultimo", email="ultimo@example.com", password="senha123")
    Profile.objects.create(user=user, nome="Ultimo Teste", data_nascimento=date(1990, 1, 1), peso=60.0)
    Ciclo.objects.create(usuario=user, data=date(2024, 5, 1), dia_menstruada=True, duracao_ciclo=28, duracao_menstruacao=5, fluxo_menstrual='MODERADO')
    Ciclo.objects.create(usuario=user, data=date(2024, 6, 1), dia_menstruada=True, duracao_ciclo=30, duracao_menstruacao=6, fluxo_menstrual='LEVE')
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/ciclos/ultimo/")
    assert response.status_code == 200
    assert response.data["data"] == "2024-06-01"

@pytest.mark.django_db
def test_ciclo_previsao_endpoint():
    user = User.objects.create_user(username="previsao", email="previsao@example.com", password="senha123")
    Profile.objects.create(user=user, nome="Previsao Teste", data_nascimento=date(1990, 1, 1), peso=60.0)
    Ciclo.objects.create(usuario=user, data=date(2024, 5, 1), dia_menstruada=True, duracao_ciclo=28, duracao_menstruacao=5, fluxo_menstrual='MODERADO')
    Ciclo.objects.create(usuario=user, data=date(2024, 6, 1), dia_menstruada=True, duracao_ciclo=30, duracao_menstruacao=6, fluxo_menstrual='LEVE')
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/ciclos/previsao/")
    assert response.status_code == 200
    assert "data_previsao" in response.data
    assert "duracao_media" in response.data

@pytest.mark.django_db
def test_ciclo_duracao_media_endpoint():
    user = User.objects.create_user(username="media", email="media@example.com", password="senha123")
    Profile.objects.create(user=user, nome="Media Teste", data_nascimento=date(1990, 1, 1), peso=60.0)
    Ciclo.objects.create(usuario=user, data=date(2024, 5, 1), dia_menstruada=True, duracao_ciclo=28, duracao_menstruacao=5, fluxo_menstrual='MODERADO')
    Ciclo.objects.create(usuario=user, data=date(2024, 6, 1), dia_menstruada=True, duracao_ciclo=30, duracao_menstruacao=6, fluxo_menstrual='LEVE')
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/ciclos/duracao_media/")
    assert response.status_code == 200
    assert "duracao_media" in response.data
    assert "total_ciclos" in response.data
