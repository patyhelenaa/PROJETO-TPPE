# Regra de Negócio: Atribuição Automática de Sintoma ao Ciclo

## Descrição

Ao criar um sintoma (físico, humor, libido ou secreção), o sistema **atribui automaticamente** o sintoma ao ciclo menstrual correspondente, com base na data informada pelo usuário.

## Lógica de Atribuição
- O usuário informa apenas a data do sintoma.
- O backend busca o ciclo do usuário cuja data de início seja **menor ou igual** à data do sintoma e, se houver mais de um, pega o mais recente.
- O sintoma é salvo vinculado a esse ciclo.
- Se não houver ciclo correspondente para a data, o backend retorna erro informando que não há ciclo para aquela data.

## Impacto no Frontend
- O frontend **não precisa mais enviar o campo `ciclo`** ao criar um sintoma.
- O formulário de sintoma fica mais simples para o usuário.
- Ao exibir sintomas, pode-se mostrar "Do ciclo: iniciado em ..." usando o campo `ciclo` retornado pelo backend.

## Impacto no Backend
- A lógica de atribuição foi implementada nos métodos `perform_create` dos ViewSets de sintomas.
- O backend garante que todo sintoma criado estará sempre associado a um ciclo válido do usuário.

## Benefícios
- Experiência do usuário mais simples e intuitiva.
- Menos chance de erro por parte do usuário.
- Dados mais consistentes no sistema. 