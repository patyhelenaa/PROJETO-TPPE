import pytest
from rest_framework.test import APIClient
from sintomas.models import Fisico, Humor, Libido, Secrecao, Intensidade, HumorEnum, TexturaSecrecao
from datetime import date

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestFisicoAPI:

    def test_criar_fisico(self, api_client):
        data = {
            "intensidade": Intensidade.LEVE,
            "descricao": "Dor leve",
            "nome_sintoma": "Dor muscular",
            "data": "2025-06-24",
            "pratica": True,
            "remedio_tomado": "Nenhum"
        }
        response = api_client.post("/api/fisico/", data, format="json")
        assert response.status_code == 201
        assert response.data["nome_sintoma"] == "Dor muscular"
        assert response.data["pratica"] is True

    def test_listar_fisico(self, api_client):
        Fisico.objects.create(
            intensidade=Intensidade.MODERADO,
            descricao="Dor moderada",
            nome_sintoma="Dor nas costas",
            data=date.today(),
            pratica=False,
            remedio_tomado="Paracetamol"
        )
        response = api_client.get("/api/fisico/")
        assert response.status_code == 200
        assert any(f["nome_sintoma"] == "Dor nas costas" for f in response.data)

@pytest.mark.django_db
class TestHumorAPI:

    def test_criar_humor(self, api_client):
        data = {
            "intensidade": Intensidade.INTENSO,
            "descricao": "Senti tristeza profunda",
            "nome_sintoma": "Tristeza",
            "data": "2025-06-24",
            "gatilho": "Discussão",
            "humor": HumorEnum.TRISTEZA,
        }
        response = api_client.post("/api/humor/", data, format="json")
        assert response.status_code == 201
        assert response.data["humor"] == HumorEnum.TRISTEZA

    def test_listar_humor(self, api_client):
        Humor.objects.create(
            intensidade=Intensidade.LEVE,
            descricao="Alegria leve",
            nome_sintoma="Felicidade",
            data=date.today(),
            gatilho="Boa notícia",
            humor=HumorEnum.FELICIDADE,
        )
        response = api_client.get("/api/humor/")
        assert response.status_code == 200
        assert any(h["nome_sintoma"] == "Felicidade" for h in response.data)

@pytest.mark.django_db
class TestLibidoAPI:

    def test_criar_libido(self, api_client):
        data = {
            "intensidade": Intensidade.MODERADO,
            "descricao": "Teve relações com parceiro",
            "nome_sintoma": "Libido",
            "data": "2025-06-24",
            "relacoes_com_parceiro": True,
            "relacoes_sem_parceiro": False,
        }
        response = api_client.post("/api/libido/", data, format="json")
        assert response.status_code == 201
        assert response.data["relacoes_com_parceiro"] is True

    def test_listar_libido(self, api_client):
        Libido.objects.create(
            intensidade=Intensidade.LEVE,
            descricao="Sem relações",
            nome_sintoma="Libido baixa",
            data=date.today(),
            relacoes_com_parceiro=False,
            relacoes_sem_parceiro=False,
        )
        response = api_client.get("/api/libido/")
        assert response.status_code == 200
        assert any(l["nome_sintoma"] == "Libido baixa" for l in response.data)

@pytest.mark.django_db
class TestSecrecaoAPI:

    def test_criar_secrecao(self, api_client):
        data = {
            "intensidade": Intensidade.MUITO_INTENSO,
            "descricao": "Secreção pegajosa",
            "nome_sintoma": "Secreção vaginal",
            "data": "2025-06-24",
            "textura": TexturaSecrecao.PEGAJOSA,
            "remedio_tomado": "Nenhum"
        }
        response = api_client.post("/api/secrecao/", data, format="json")
        assert response.status_code == 201
        assert response.data["textura"] == TexturaSecrecao.PEGAJOSA

    def test_listar_secrecao(self, api_client):
        Secrecao.objects.create(
            intensidade=Intensidade.MODERADO,
            descricao="Secreção cremosa",
            nome_sintoma="Secreção vaginal",
            data=date.today(),
            textura=TexturaSecrecao.CREMOSA,
            remedio_tomado="Pomada"
        )
        response = api_client.get("/api/secrecao/")
        assert response.status_code == 200
        assert any(s["descricao"] == "Secreção cremosa" for s in response.data)
