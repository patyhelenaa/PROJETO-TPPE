import pytest
from rest_framework.test import APIClient
from usuarios.models import Usuario
from ciclos.models import Ciclo
from datetime import date, timedelta

def test_usuario_check_password():
    usuario = Usuario(nome="Teste", email="teste@ex.com", data_nascimento=date(2000,1,1), gravidez=False, peso=60)
    usuario.set_password("senha123")
    assert usuario.check_password("senha123")
    assert not usuario.check_password("errada")

@pytest.mark.parametrize("nome,email,senha,gravidez,peso", [
    ("Ana", "ana@ex.com", "senha1", True, 55.0),
    ("Bia", "bia@ex.com", "senha2", False, 60.5),
    ("Carla", "carla@ex.com", "senha3", True, 70.2),
])
@pytest.mark.django_db
def test_cadastro_parametrizado(nome, email, senha, gravidez, peso):
    client = APIClient()
    data = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "data_nascimento": "1990-01-01",
        "gravidez": gravidez,
        "peso": peso
    }
    response = client.post("/api/usuarios/", data, format='json')
    assert response.status_code == 201
    assert response.data["nome"] == nome
    assert response.data["email"] == email
    assert response.data["gravidez"] == gravidez
    assert response.data["peso"] == peso
    assert "senha" not in response.data

@pytest.mark.django_db
def test_usuario_me_endpoint():
    usuario = Usuario(
        nome="Beatriz Costa",
        email="beatriz.costa@example.com",
        data_nascimento=date(1992, 8, 23),
        gravidez=False,
        peso=58.5
    )
    usuario.set_password("senha123")
    usuario.save()
    client = APIClient()
    client.force_authenticate(user=usuario)
    response = client.get("/api/usuarios/me/")
    assert response.status_code == 200
    assert response.data["nome"] == "Beatriz Costa"
    assert "senha" not in response.data

@pytest.mark.django_db
def test_atualizar_usuario_me_endpoint():
    usuario = Usuario(
        nome="Carla Fernandes",
        email="carla.fernandes@example.com",
        data_nascimento=date(1985, 11, 30),
        gravidez=False,
        peso=70.0
    )
    usuario.set_password("senha123")
    usuario.save()
    client = APIClient()
    client.force_authenticate(user=usuario)
    data = {
        "nome": "Carla Fernandes",
        "email": "carla.fernandes@example.com",
        "senha": "novasenha456",
        "data_nascimento": "1985-11-30",
        "gravidez": True,
        "peso": 72.5
    }
    response = client.put("/api/usuarios/me/", data, format='json')
    assert response.status_code == 200
    assert response.data["peso"] == 72.5
    assert response.data["gravidez"] is True
    assert response.data["email"] == "carla.fernandes@example.com"
    assert "senha" not in response.data
    usuario.refresh_from_db()
    assert usuario.check_password("novasenha456")

@pytest.mark.django_db
def test_deletar_usuario_me_endpoint():
    usuario = Usuario(
        nome="Daniela Rocha",
        email="daniela.rocha@example.com",
        data_nascimento=date(1995, 1, 10),
        gravidez=False,
        peso=64.0
    )
    usuario.set_password("senha123")
    usuario.save()
    client = APIClient()
    client.force_authenticate(user=usuario)
    response = client.delete("/api/usuarios/me/")
    assert response.status_code == 204
    assert Usuario.objects.count() == 0

@pytest.mark.django_db
def test_usuario_nao_ve_outros():
    usuario1 = Usuario(
        nome="Usuário 1",
        email="user1@example.com",
        data_nascimento=date(1990, 1, 1),
        gravidez=False,
        peso=60.0
    )
    usuario1.set_password("senha1")
    usuario1.save()
    usuario2 = Usuario(
        nome="Usuário 2",
        email="user2@example.com",
        data_nascimento=date(1991, 2, 2),
        gravidez=True,
        peso=65.0
    )
    usuario2.set_password("senha2")
    usuario2.save()
    client = APIClient()
    client.force_authenticate(user=usuario1)
    response = client.get(f"/api/usuarios/{usuario2.id}/")
    assert response.status_code in (403, 404)

def test_usuario_calcular_duracao_media_ciclos():
    usuario = Usuario(nome="Teste", email="teste@ex.com", data_nascimento=date(2000,1,1), gravidez=False, peso=60)
    usuario.save()
    Ciclo.objects.create(usuario=usuario, data=date(2024, 6, 1), dia_menstruada=True, duracao_ciclo=28, duracao_menstruacao=5, fluxo_menstrual='MODERADO')
    Ciclo.objects.create(usuario=usuario, data=date(2024, 5, 4), dia_menstruada=True, duracao_ciclo=30, duracao_menstruacao=6, fluxo_menstrual='LEVE')
    Ciclo.objects.create(usuario=usuario, data=date(2024, 4, 6), dia_menstruada=True, duracao_ciclo=27, duracao_menstruacao=4, fluxo_menstrual='INTENSO')
    media = usuario.calcular_duracao_media_ciclos()
    assert media == pytest.approx((28+30+27)/3)

def test_usuario_prever_proximo_ciclo():
    usuario = Usuario(nome="Teste2", email="teste2@ex.com", data_nascimento=date(2000,1,1), gravidez=False, peso=60)
    usuario.save()
    Ciclo.objects.create(usuario=usuario, data=date(2024, 6, 1), dia_menstruada=True, duracao_ciclo=28, duracao_menstruacao=5, fluxo_menstrual='MODERADO')
    Ciclo.objects.create(usuario=usuario, data=date(2024, 5, 4), dia_menstruada=True, duracao_ciclo=30, duracao_menstruacao=6, fluxo_menstrual='LEVE')
    Ciclo.objects.create(usuario=usuario, data=date(2024, 4, 6), dia_menstruada=True, duracao_ciclo=27, duracao_menstruacao=4, fluxo_menstrual='INTENSO')
    # Último ciclo: 2024-06-01, média: 28.33... dias
    previsao = usuario.prever_proximo_ciclo()
    esperado = date(2024, 6, 1) + timedelta(days=int((28+30+27)/3))
    assert previsao == esperado
