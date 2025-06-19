import pytest
from rest_framework.test import APIClient
from usuarios.models import Usuario
from ciclos.models import Ciclo
from datetime import date, timedelta

@pytest.mark.django_db
def test_ciclo_str():
    usuario = Usuario(nome="Teste", email="teste@ex.com", data_nascimento=date(2000,1,1), gravidez=False, peso=60)
    usuario.set_password("senha123")
    usuario.save()
    ciclo = Ciclo(usuario=usuario, data=date(2024, 6, 1), dia_menstruada=True, duracao_ciclo=28, duracao_menstruacao=5, fluxo_menstrual='MODERADO')
    assert str(ciclo) == f"Ciclo do usuário {usuario.nome} em {ciclo.data}"

@pytest.mark.parametrize("duracao,menstruacao,fluxo", [
    (28, 5, 'MODERADO'),
    (30, 6, 'LEVE'),
    (27, 4, 'INTENSO'),
])
@pytest.mark.django_db
def test_criar_ciclo_parametrizado(duracao, menstruacao, fluxo):
    usuario = Usuario.objects.create(
        nome="Ana Paula",
        email=f"ana{duracao}@example.com",
        data_nascimento=date(1995, 4, 10),
        gravidez=False,
        peso=60.0,
    )
    usuario.set_password("senha123")
    usuario.save()
    client = APIClient()
    client.force_authenticate(user=usuario)
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
    usuario = Usuario.objects.create(
        nome="Ana Paula",
        email="ana@example.com",
        data_nascimento=date(1995, 4, 10),
        gravidez=False,
        peso=60.0,
    )
    usuario.set_password("senha123")
    usuario.save()
    client = APIClient()
    client.force_authenticate(user=usuario)
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
    usuario = Usuario.objects.create(
        nome="Ana Paula",
        email="ana@example.com",
        data_nascimento=date(1995, 4, 10),
        gravidez=False,
        peso=60.0,
    )
    usuario.set_password("senha123")
    usuario.save()
    ciclo = Ciclo.objects.create(
        usuario=usuario,
        data=date(2025, 6, 1),
        dia_menstruada=True,
        duracao_ciclo=28,
        duracao_menstruacao=5,
        fluxo_menstrual="MODERADO"
    )
    client = APIClient()
    client.force_authenticate(user=usuario)
    response = client.get("/api/ciclos/")
    assert response.status_code == 200
    ciclo_id = ciclo.id
    assert any(c["id"] == ciclo_id for c in response.data)

@pytest.mark.django_db
def test_atualizar_ciclo_api():
    usuario = Usuario.objects.create(
        nome="Ana Paula",
        email="ana@example.com",
        data_nascimento=date(1995, 4, 10),
        gravidez=False,
        peso=60.0,
    )
    usuario.set_password("senha123")
    usuario.save()
    ciclo = Ciclo.objects.create(
        usuario=usuario,
        data=date(2025, 6, 1),
        dia_menstruada=True,
        duracao_ciclo=28,
        duracao_menstruacao=5,
        fluxo_menstrual="MODERADO"
    )
    client = APIClient()
    client.force_authenticate(user=usuario)
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
    usuario = Usuario.objects.create(
        nome="Ana Paula",
        email="ana@example.com",
        data_nascimento=date(1995, 4, 10),
        gravidez=False,
        peso=60.0,
    )
    usuario.set_password("senha123")
    usuario.save()
    ciclo = Ciclo.objects.create(
        usuario=usuario,
        data=date(2025, 6, 1),
        dia_menstruada=True,
        duracao_ciclo=28,
        duracao_menstruacao=5,
        fluxo_menstrual="MODERADO"
    )
    client = APIClient()
    client.force_authenticate(user=usuario)
    response = client.delete(f"/api/ciclos/{ciclo.id}/")
    assert response.status_code == 204
    assert Ciclo.objects.count() == 0

# --- Testes de integração dos endpoints customizados ---
@pytest.mark.django_db
def test_ciclo_ultimo_endpoint():
    usuario = Usuario.objects.create(
        nome="Ultimo Teste",
        email="ultimo@example.com",
        senha="senha123",
        data_nascimento=date(1990, 1, 1),
        gravidez=False,
        peso=60.0,
    )
    Ciclo.objects.create(usuario=usuario, data=date(2024, 5, 1), dia_menstruada=True, duracao_ciclo=28, duracao_menstruacao=5, fluxo_menstrual='MODERADO')
    Ciclo.objects.create(usuario=usuario, data=date(2024, 6, 1), dia_menstruada=True, duracao_ciclo=30, duracao_menstruacao=6, fluxo_menstrual='LEVE')
    client = APIClient()
    client.force_authenticate(user=usuario)
    response = client.get("/api/ciclos/ultimo/")
    assert response.status_code == 200
    assert response.data["data"] == "2024-06-01"

@pytest.mark.django_db
def test_ciclo_previsao_endpoint():
    usuario = Usuario.objects.create(
        nome="Previsao Teste",
        email="previsao@example.com",
        senha="senha123",
        data_nascimento=date(1990, 1, 1),
        gravidez=False,
        peso=60.0,
    )
    Ciclo.objects.create(usuario=usuario, data=date(2024, 5, 1), dia_menstruada=True, duracao_ciclo=28, duracao_menstruacao=5, fluxo_menstrual='MODERADO')
    Ciclo.objects.create(usuario=usuario, data=date(2024, 6, 1), dia_menstruada=True, duracao_ciclo=30, duracao_menstruacao=6, fluxo_menstrual='LEVE')
    client = APIClient()
    client.force_authenticate(user=usuario)
    response = client.get("/api/ciclos/previsao/")
    assert response.status_code == 200
    assert "previsao_proximo_ciclo" in response.data

@pytest.mark.django_db
def test_ciclo_duracao_media_endpoint():
    usuario = Usuario.objects.create(
        nome="Media Teste",
        email="media@example.com",
        senha="senha123",
        data_nascimento=date(1990, 1, 1),
        gravidez=False,
        peso=60.0,
    )
    Ciclo.objects.create(usuario=usuario, data=date(2024, 5, 1), dia_menstruada=True, duracao_ciclo=28, duracao_menstruacao=5, fluxo_menstrual='MODERADO')
    Ciclo.objects.create(usuario=usuario, data=date(2024, 6, 1), dia_menstruada=True, duracao_ciclo=30, duracao_menstruacao=6, fluxo_menstrual='LEVE')
    client = APIClient()
    client.force_authenticate(user=usuario)
    response = client.get("/api/ciclos/duracao_media/")
    assert response.status_code == 200
    assert "duracao_media_ciclos" in response.data
