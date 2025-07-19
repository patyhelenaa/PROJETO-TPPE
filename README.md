# Meu Diário de Ciclos

[Projeto original (fork)](https://github.com/patyhelenaa/Diario-de-ciclos-menstruais)

## 💡 Ideia do Projeto

Este projeto foi desenvolvido para a disciplina de **Técnicas de Programação em Plataformas Emergentes (TPPE)**, com o objetivo de reconstruir e aprimorar um sistema já existente, utilizando uma linguagem e framework diferentes do original.

O **Meu Diário de Ciclos** é um sistema web para acompanhamento de ciclos menstruais, sintomas físicos, emocionais e outros dados relevantes para a saúde da mulher. O objetivo é fornecer uma ferramenta intuitiva para registro, análise e visualização dos ciclos, sintomas e padrões, promovendo autoconhecimento e saúde. Esta versão foi construída com **Python** e o framework **Django**.

## 🚀 Tecnologias e Linguagens Utilizadas

- **Backend:** Python 3, Django, Django REST Framework
- **Banco de Dados:** PostgreSQL
- **Docker:** Para ambiente de desenvolvimento e produção
- **Testes:** Pytest, Django Test, DRF Test, parametrização
- **Documentação de API:** Swagger (drf-yasg)
- **Análise de código:** flake8

## 🛠️ Como rodar o projeto (Backend)

### 1. Pré-requisitos
- Docker e Docker Compose

### 2. Clonar o repositório
```bash
git clone https://github.com/patyhelenaa/Diario-de-ciclos-menstruais.git
```
### 2. mover para pasta src
```bash
cd src
```
### 4. Rodar com Docker
```bash
docker-compose up --build
```
- Acesse a API em: http://localhost:8000/
- Acesse a documentação Swagger em: http://localhost:8000/swagger/

> **Observação:**
> Todos os testes automatizados e a análise de código com flake8 são executados automaticamente ao subir o Docker. Não é necessário rodar comandos manuais para garantir a qualidade do código.

## 📄 Documentações

- [Backlog](docs/backlog.md)
- [Testes de Integração e Parametrizados](docs/TESTES.md)
- [Diagrama de Classes (PNG)](docs/diagramaClasses.png)
- [Diagrama de Classes (PDF)](docs/UML_DiagramaClasses.pdf)
- [UML Geral (JPG)](docs/UMLTPPEv2.jpg)
- [DLD - Diagrama Lógico de Dados (PNG)](docs/DLD.png)
- [Manual do Projeto (PDF)](docs/MEU%20DIARIO%20DE%20CICLOS.pdf)

---

Sinta-se à vontade para contribuir ou sugerir melhorias!
