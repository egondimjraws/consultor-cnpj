# 🔍 CNPJ Consultor

> Biblioteca Python para consulta de CNPJ com fallback automático entre APIs

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Code style](https://img.shields.io/badge/code%20style-pep8-orange.svg?style=flat-square)](https://www.python.org/dev/peps/pep-0008/)

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Instalação](#-instalação)
  - [Como Git Submodule](#como-git-submodule)
- [Como Usar](#-como-usar)
  - [Como Biblioteca](#1️⃣-como-biblioteca)
  - [Como CLI](#2️⃣-como-cli)
  - [Modo Interativo](#3️⃣-modo-interativo)
- [API Reference](#-api-reference)
- [Exemplos](#-exemplos)
- [APIs Utilizadas](#-apis-utilizadas)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

**CNPJ Consultor** é uma biblioteca Python leve e eficiente que consulta a situação cadastral de empresas brasileiras através do CNPJ, retornando de forma simples e direta o **nome da empresa** e seu **status atual**.

### Por que usar?

- ✅ **Zero dependências** - apenas bibliotecas nativas do Python
- 🔄 **Fallback automático** - tenta múltiplas APIs em caso de falha
- 💻 **Multi-modo** - use como biblioteca, CLI ou modo interativo
- 📊 **Saída padronizada** - formato consistente `EMPRESA | STATUS`
- 🛡️ **Validação local** - validação de CNPJ sem consulta externa
- ⚡ **Rápido e leve** - menos de 200 linhas de código
- 🔒 **Seguro** - sem armazenamento de dados

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| 🚀 **Zero Dependências** | Apenas bibliotecas nativas do Python |
| 🔄 **Fallback Automático** | ReceitaWS → BrasilAPI (alta disponibilidade) |
| 💻 **Multi-modo** | Biblioteca, CLI e modo interativo |
| 📊 **Saída Padronizada** | Formato `EMPRESA | STATUS` |
| 🛡️ **Validação Local** | Valida CNPJ sem consulta externa |
| 🔧 **Formatação** | Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX |
| 📈 **Relatórios** | Gera relatórios para múltiplos CNPJs |
| ⚡ **Rápido** | Consultas em milissegundos |

---

## 🚀 Instalação

### Via GitHub (recomendado)

```bash
# Clone o repositório
git clone https://github.com/egondimjraws/consultor-cnpj.git
cd consultor-cnpj

# Crie um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale o pacote
pip install -e .
```

### Como Git Submodule

Para usar o `consultor-cnpj` dentro de outro projeto, mantendo o histórico e as atualizações vinculados ao repositório original, adicione-o como submódulo:

```bash
# Dentro do repositório que vai consumir a biblioteca
git submodule add https://github.com/egondimjraws/consultor-cnpj.git libs/consultor-cnpj
git submodule update --init --recursive
```

Instale o pacote do submódulo em modo editável no ambiente do projeto principal:

```bash
pip install -e libs/consultor-cnpj
```

Ao clonar um projeto que já usa esse submódulo, traga o conteúdo do submódulo com:

```bash
git clone --recurse-submodules <url-do-projeto-principal>
# ou, se já clonou sem a flag:
git submodule update --init --recursive
```

Para atualizar o submódulo para a versão mais recente do `consultor-cnpj`:

```bash
cd libs/consultor-cnpj
git pull origin main
cd ../..
git add libs/consultor-cnpj
git commit -m "chore: atualiza submódulo consultor-cnpj"
```

---

## 📖 Como Usar

### 1️⃣ Como Biblioteca

```python
from consultor_cnpj import consultar_cnpj, cnpj_status, formatar_cnpj, validar_cnpj

cnpj = "11.222.333/0001-81"

# Validação local (sem consulta externa)
validar_cnpj(cnpj)          # True
formatar_cnpj(cnpj)         # "11222333000181"

# Consulta em formato padronizado "EMPRESA | STATUS"
cnpj_status(cnpj)           # "EMPRESA EXEMPLO LTDA | ATIVA"

# Consulta com o dicionário bruto retornado pela API (ReceitaWS ou BrasilAPI)
consultar_cnpj(cnpj)        # {"nome": "...", "situacao": "ATIVA", ...}
```

Para o status detalhado (nome, situação, abertura, atividade principal, cidade, UF e telefone) e para gerar relatórios de múltiplos CNPJs, importe direto dos submódulos:

```python
from consultor_cnpj.core import status_detalhado
from consultor_cnpj.utils import gerar_relatorio, formatar_cnpj_visual

status_detalhado(cnpj)
# {"cnpj": "...", "nome": "...", "status": "...", "abertura": "...",
#  "atividade_principal": "...", "cidade": "...", "uf": "...", "telefone": "..."}

gerar_relatorio(["11222333000181", "12345678000199"])
# {"total": 2, "validos": 1, "invalidos": 1, "ativos": ..., "inativos": ..., "detalhes": {...}}

formatar_cnpj_visual("11222333000181")  # "11.222.333/0001-81"
```

### 2️⃣ Como CLI

Após `pip install -e .`, o comando `cnpj-consultor` fica disponível no PATH:

```bash
cnpj-consultor 11.222.333/0001-81
# EMPRESA EXEMPLO LTDA | ATIVA
```

### 3️⃣ Modo Interativo

Rode sem argumentos para entrar no modo interativo (consulta contínua até digitar `sair`, `exit` ou `quit`):

```bash
cnpj-consultor
```

---

## 📚 API Reference

| Função | Assinatura | Descrição |
|--------|------------|-----------|
| `consultar_cnpj` | `(cnpj: str) -> Dict` | Consulta com fallback automático ReceitaWS → BrasilAPI. Levanta `InvalidCNPJError` ou `APIError`. |
| `cnpj_status` | `(cnpj: str) -> str` | Retorna `"EMPRESA \| STATUS"`, nunca levanta exceção. |
| `status_detalhado` | `(cnpj: str) -> Dict` | Retorna dicionário com nome, status, abertura, atividade principal, cidade, UF e telefone. |
| `validar_cnpj` | `(cnpj: str) -> bool` | Valida os dígitos verificadores do CNPJ localmente. |
| `formatar_cnpj` | `(cnpj: str) -> str` | Remove formatação, retornando apenas os 14 dígitos. |
| `formatar_cnpj_visual` | `(cnpj: str) -> str` | Formata para `XX.XXX.XXX/XXXX-XX`. |
| `gerar_relatorio` | `(cnpjs: List[str]) -> Dict` | Gera estatísticas (válidos, inválidos, ativos, inativos) para uma lista de CNPJs. |

**Exceções** (`consultor_cnpj.exceptions`): `CNPJError` (base), `InvalidCNPJError`, `APIError`, `RateLimitError`.

---

## 💡 Exemplos

A pasta [`examples/`](examples/) contém scripts de referência prontos para rodar (após `pip install -e .`):

| Script | Descrição |
|--------|-----------|
| [`basic_usage.py`](examples/basic_usage.py) | Validação, formatação e consulta de um único CNPJ, incluindo tratamento de exceções. |
| [`batch_processing.py`](examples/batch_processing.py) | Consulta uma lista de CNPJs e gera um relatório agregado com `gerar_relatorio`. |
| [`custom_formatting.py`](examples/custom_formatting.py) | Mostra diferentes formatações de entrada (limpo e visual) para o mesmo CNPJ. |
| [`integration_example.py`](examples/integration_example.py) | Exemplo de integração: checa uma carteira de fornecedores e sinaliza CNPJs inválidos ou com situação cadastral inativa. |

Para executar qualquer um deles:

```bash
python examples/basic_usage.py
python examples/batch_processing.py
python examples/custom_formatting.py
python examples/integration_example.py
```

---

## 🌐 APIs Utilizadas

| API | URL |
|-----|-----|
| ReceitaWS | https://www.receitaws.com.br |
| BrasilAPI | https://brasilapi.com.br |

O `consultor_cnpj` tenta a ReceitaWS primeiro e faz fallback automático para a BrasilAPI em caso de erro.

---

## 🤝 Contribuição

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para o passo a passo de como abrir um Pull Request e os padrões de código do projeto.

---

## 📄 Licença

Distribuído sob a licença MIT.
