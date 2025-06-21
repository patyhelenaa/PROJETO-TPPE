import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from usuarios.models import Profile
from ciclos.models import Ciclo
from datetime import date, timedelta

@pytest.mark.django_db
def test_user_password_check():
    user = User.objects.create_user(username="teste", email="teste@ex.com", password="senha123")
    Profile.objects.create(user=user, nome="Teste", data_nascimento=date(2000, 1, 1), peso=60)
    assert user.check_password("senha123")
    assert not user.check_password("errada")

@pytest.mark.parametrize("username,email,senha,nome,peso", [
    ("ana", "ana@ex.com", "senha1", "Ana", 55.0),
    ("bia", "bia@ex.com", "senha2", "Bia", 60.5),
    ("carla", "carla@ex.com", "senha3", "Carla", 70.2),
])
@pytest.mark.django_db
def test_cadastro_parametrizado(username, email, senha, nome, peso):
    client = APIClient()
    data = {
        "username": username,
        "email": email,
        "password": senha,
        "profile": {
            "nome": nome,
            "data_nascimento": "1990-01-01",
            "peso": peso
        }
    }
    response = client.post("/api/usuarios/", data, format='json')
    assert response.status_code == 201
    assert response.data["username"] == username
    assert response.data["email"] == email
    assert response.data["profile"]["nome"] == nome
    assert response.data["profile"]["peso"] == peso
    assert "password" not in response.data

@pytest.mark.django_db
def test_user_me_endpoint():
    user = User.objects.create_user(username="beatriz", email="beatriz.costa@example.com", password="senha123")
    Profile.objects.create(user=user, nome="Beatriz Costa", data_nascimento=date(1992, 8, 23), peso=58.5)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/usuarios/me/")
    assert response.status_code == 200
    assert response.data["profile"]["nome"] == "Beatriz Costa"
    assert "password" not in response.data

@pytest.mark.django_db
def test_atualizar_user_me_endpoint():
    user = User.objects.create_user(username="carla", email="carla.fernandes@example.com", password="senha123")
    Profile.objects.create(user=user, nome="Carla Fernandes", data_nascimento=date(1985, 11, 30), peso=70.0)
    client = APIClient()
    client.force_authenticate(user=user)
    data = {
        "username": "carla",
        "email": "carla.fernandes@example.com",
        "password": "novasenha456",
        "profile": {
            "nome": "Carla Fernandes",
            "data_nascimento": "1985-11-30",
            "peso": 72.5
        }
    }
    response = client.put("/api/usuarios/me/", data, format='json')
    assert response.status_code == 200
    assert response.data["profile"]["peso"] == 72.5
    assert response.data["email"] == "carla.fernandes@example.com"
    assert "password" not in response.data
    user.refresh_from_db()
    assert user.check_password("novasenha456")

@pytest.mark.django_db
def test_deletar_user_me_endpoint():
    user = User.objects.create_user(username="daniela", email="daniela.rocha@example.com", password="senha123")
    Profile.objects.create(user=user, nome="Daniela Rocha", data_nascimento=date(1995, 1, 10), peso=64.0)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.delete("/api/usuarios/me/")
    assert response.status_code == 204
    assert User.objects.count() == 0

@pytest.mark.django_db
def test_user_nao_ve_outros():
    user1 = User.objects.create_user(username="user1", email="user1@example.com", password="senha1")
    Profile.objects.create(user=user1, nome="Usuário 1", data_nascimento=date(1990, 1, 1), peso=60.0)
    user2 = User.objects.create_user(username="user2", email="user2@example.com", password="senha2")
    Profile.objects.create(user=user2, nome="Usuário 2", data_nascimento=date(1991, 2, 2), peso=65.0)
    client = APIClient()
    client.force_authenticate(user=user1)
    response = client.get(f"/api/usuarios/{user2.id}/")
    assert response.status_code in (403, 404)
