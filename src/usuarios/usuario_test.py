import pytest
from rest_framework.test import APIClient
from usuarios.models import Usuario
from datetime import date

@pytest.mark.django_db
def test_criar_usuario_api():
    client = APIClient()
    data = {
        "nome": "João Souza",
        "data_nascimento": "1985-10-20",
        "gravidez": True,
        "peso": 70.0
    }
    response = client.post("/api/usuarios/", data, format='json')

    assert response.status_code == 201
    assert response.data["nome"] == "João Souza"
    assert response.data["gravidez"] is True
    assert response.data["peso"] == 70.0

@pytest.mark.django_db
def test_listar_usuarios_api():
    Usuario.objects.create(
        nome="Maria Silva",
        data_nascimento=date(1990, 5, 15),
        gravidez=False,
        peso=65.5
    )
    client = APIClient()
    response = client.get("/api/usuarios/")

    assert response.status_code == 200
    assert any(usuario["nome"] == "Maria Silva" for usuario in response.data)

@pytest.mark.django_db
def test_atualizar_usuario_api():
    usuario = Usuario.objects.create(
        nome="Maria Silva",
        data_nascimento=date(1990, 5, 15),
        gravidez=False,
        peso=65.5
    )
    client = APIClient()
    data = {
        "nome": "Maria Silva",
        "data_nascimento": "1990-05-15",
        "gravidez": True,
        "peso": 68.0
    }
    response = client.put(f"/api/usuarios/{usuario.id}/", data, format='json')

    assert response.status_code == 200
    assert response.data["peso"] == 68.0
    assert response.data["gravidez"] is True

@pytest.mark.django_db
def test_deletar_usuario_api():
    usuario = Usuario.objects.create(
        nome="Maria Silva",
        data_nascimento=date(1990, 5, 15),
        gravidez=False,
        peso=65.5
    )
    client = APIClient()
    response = client.delete(f"/api/usuarios/{usuario.id}/")

    assert response.status_code == 204
    assert Usuario.objects.count() == 0
