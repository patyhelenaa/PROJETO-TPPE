# Documentação dos Testes Automatizados

Este projeto utiliza testes automatizados com o framework `pytest` e o Django REST Framework para garantir a qualidade e a integração dos endpoints da API.

## Tipos de Teste

- **Teste de Integração:**
  - Testa o funcionamento completo dos endpoints da API, simulando requisições HTTP reais e validando a integração entre views, serializers, models e autenticação.
  - Utiliza o `APIClient` do DRF para simular chamadas HTTP.

- **Teste Parametrizado:**
  - Usa o decorator `@pytest.mark.parametrize` para rodar o mesmo teste com diferentes conjuntos de dados, aumentando a cobertura de cenários e evitando repetição de código.

---

## Onde estão os testes

### Testes de Integração
- **Arquivo:** `meu_projeto/src/ciclos/ciclo_test.py`
  - Todos os testes deste arquivo são de integração, pois usam o `APIClient` para testar os endpoints de ciclo.
- **Arquivo:** `meu_projeto/src/sintomas/sintomas_test.py`
  - Todos os testes deste arquivo são de integração, testando os endpoints de sintomas (físico, humor, libido, secreção).
- **Arquivo:** `meu_projeto/src/usuarios/usuario_test.py`
  - Todos os testes deste arquivo são de integração, testando cadastro, autenticação, atualização e deleção de usuário.

### Testes Parametrizados
- **Arquivo:** `meu_projeto/src/ciclos/ciclo_test.py`
  - Função: `test_criar_ciclo_parametrizado` (testa criação de ciclos com diferentes parâmetros)
- **Arquivo:** `meu_projeto/src/usuarios/usuario_test.py`
  - Função: `test_cadastro_parametrizado` (testa cadastro de usuários com diferentes dados)

---

## Resumo
- Todos os fluxos principais da API são cobertos por testes de integração.
- Os testes parametrizados aumentam a robustez e a cobertura dos cenários mais comuns.

Se desejar adicionar mais testes, siga o padrão dos arquivos acima para garantir integração e cobertura parametrizada. 