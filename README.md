# Favorite Cart (LuizaLabs)

Backend para registro de carrinho de produtos favoritos.

[![Licença](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Versão do Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/downloads/)
[![Cobertura](https://img.shields.io/badge/coverage-84%25-green.svg)](https://example.com/coverage)
[![Testes](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://example.com/tests)

## Índice

- [Descrição](#descrição)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Uso](#uso)
- [Contribuições](#contribuições)
- [Contato](#contato)
- [Referências](#referências)

## Descrição

Este projeto é um desafio de desenvolvimento de API para avaliação de conhecimento técnico na posição de Engenheiro de Software no LuizaLabs.

### Estrutura do Projeto

O projeto segue padrões de arquitetura baseados em separação por domínios e seus adaptadores. Exemplo da estrutura do domínio `Customer`:

```bash
customer/
├── adapters/           # Camada de interfaces e adaptadores do domínio Customer
│   ├── repository.py   # Interface e implementação do adaptador dos repositórios de dados
│   └── schemas.py      # Schemas comuns aos adapters
├── exceptions.py       # Exceções comuns ao domínio
├── models.py           # Modelos do domínio
└── services.py         # Camada de serviço para orquestração de fluxos de trabalho e definição de casos de uso
```

A camada de entrada da aplicação, responsável pelas fábricas de dispositivos externos e pelo framework FastAPI:

```bash
entrypoints/            # Principais pontos de entrada da aplicação
├── fastapi/            # Implementação do framework FastAPI
│   ├── endpoints/      # Implementação dos endpoints do FastAPI
│   ├── exceptions/     # Exceções específicas do FastAPI
│   └── main.py         # Arquivo de inicialização do FastAPI
└── factories.py        # Fábrica de conectores, dispositivos e features para injeção de dependência
```

## Instalação

Para rodar esta aplicação, você precisará de:

- [Python 3.12](https://asdf-vm.com/)
- [Make](https://www.gnu.org/software/make/)
- [Poetry 1.8.x](https://python-poetry.org/docs/)
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose v2](https://docs.docker.com/compose/install/linux/)

Dependências opcionais:

- [MongoDB](https://www.mongodb.com/pt-br/docs/manual/administration/install-community/)
- [MongoDB Compass](https://www.mongodb.com/try/download/shell)

## Uso

### Comandos Principais

obs.: Para o correto funcionamento da API é necessário substituir a a env `CHALLENGE_API` por uma API de produtos valida,
tendo em vista que a do luiza labs se encontra fora do ar.

- **Rodar a aplicação:**
  ```bash
  make run
  ```
  - Copia o env.default gerando um .env
  - Gera um `requirements` seguro da aplicação.
  - Constrói uma imagem baseada no `Dockerfile`.
  - Inicia o container da aplicação e do MongoDB.

- **Acessar a API:**
  - [Swagger UI](http://127.0.0.1:8000/docs) para testar a API.
  - [OpenAPI JSON](http://127.0.0.1:8000/openapi.json) para exportar o schema.

### Outros Comandos

- Rodar formatadores e linters:
  ```bash
  make format
  ```
- Rodar testes:
  ```bash
  make test
  ```
- Rodar cobertura de testes:
  ```bash
  make coverage
  ```

## Contribuições

Se quiser contribuir para o projeto:

1. Crie um fork do repositório.
2. Crie uma branch para sua contribuição:
   ```bash
   git checkout -b minha-feature
   ```
3. instale o pre-commit nos hooks do seu git.
    ```bash
    `poetry run pre-commit install`
    ```
4. Faça as modificações e commit:
   ```bash
   git commit -m 'Adicionando minha feature'
   ```
5. Envie para o repositório remoto:
   ```bash
   git push origin minha-feature
   ```
6. Abra um Pull Request para a branch `main`.

## Contato

Olá, meu nome é **José**! 👋

Estou muito feliz e animado para fazer parte do time de engenheiros do **LuizaLabs**. Se quiser conversar sobre este sistema, entre em contato:

- 📧 **LinkedIn:** [José Bernardino Neto](https://www.linkedin.com/in/jose-bernardino-neto-98407b66)
- 📞 **Telefone:** (83) 99950-5284

## Referências

- Percival, H., & Gregory, B. (2020). **Architecture Patterns with Python: Enabling Test-Driven Development, Domain-Driven Design, and Event-Driven Microservices.** O'Reilly Media, Inc. [(cosmicpython.com)](https://www.cosmicpython.com/)
- Martin, R. C. (2019). **Arquitetura limpa: o guia do artesão para estrutura e design de software.** Alta Books Editora.
