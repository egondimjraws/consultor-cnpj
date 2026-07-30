"""
Testes para consultor_cnpj.core
"""

import pytest

from consultor_cnpj.core import consultar_cnpj, cnpj_status, status_detalhado
from consultor_cnpj.exceptions import InvalidCNPJError, APIError

CNPJ_VALIDO = "11222333000181"


def test_consultar_cnpj_invalido_levanta_excecao():
    with pytest.raises(InvalidCNPJError):
        consultar_cnpj("123")


def test_consultar_cnpj_usa_receitaws_quando_disponivel(monkeypatch):
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_receitaws",
        lambda cnpj: {"nome": "EMPRESA TESTE", "situacao": "ATIVA"},
    )
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_brasilapi",
        lambda cnpj: None,
    )

    dados = consultar_cnpj(CNPJ_VALIDO)

    assert dados["nome"] == "EMPRESA TESTE"


def test_consultar_cnpj_faz_fallback_para_brasilapi(monkeypatch):
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_receitaws",
        lambda cnpj: {"status": "ERROR"},
    )
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_brasilapi",
        lambda cnpj: {"nome": "EMPRESA TESTE", "situacao_cadastral": "ATIVA"},
    )

    dados = consultar_cnpj(CNPJ_VALIDO)

    assert dados["nome"] == "EMPRESA TESTE"


def test_consultar_cnpj_levanta_api_error_quando_ambas_falham(monkeypatch):
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_receitaws",
        lambda cnpj: {"status": "ERROR"},
    )
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_brasilapi",
        lambda cnpj: {"message": "not found"},
    )

    with pytest.raises(APIError):
        consultar_cnpj(CNPJ_VALIDO)


def test_cnpj_status_retorna_formato_esperado(monkeypatch):
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_receitaws",
        lambda cnpj: {"nome": "EMPRESA TESTE", "situacao": "ATIVA"},
    )
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_brasilapi",
        lambda cnpj: None,
    )

    assert cnpj_status(CNPJ_VALIDO) == "EMPRESA TESTE | ATIVA"


def test_cnpj_status_cnpj_invalido():
    assert cnpj_status("123") == "CNPJ_INVALIDO | ERRO"


def test_cnpj_status_nao_encontrado(monkeypatch):
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_receitaws",
        lambda cnpj: {"status": "ERROR"},
    )
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_brasilapi",
        lambda cnpj: {"message": "not found"},
    )

    assert cnpj_status(CNPJ_VALIDO) == "NAO_ENCONTRADO | ERRO"


def test_status_detalhado_retorna_dados_completos(monkeypatch):
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_receitaws",
        lambda cnpj: {
            "nome": "EMPRESA TESTE",
            "situacao": "ATIVA",
            "abertura": "01/01/2000",
            "atividade_principal": [{"text": "Comércio"}],
            "municipio": "SAO PAULO",
            "uf": "SP",
            "telefone": "1111-1111",
        },
    )
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_brasilapi",
        lambda cnpj: None,
    )

    resultado = status_detalhado(CNPJ_VALIDO)

    assert resultado["nome"] == "EMPRESA TESTE"
    assert resultado["cidade"] == "SAO PAULO"
    assert resultado["uf"] == "SP"


def test_status_detalhado_cnpj_nao_encontrado(monkeypatch):
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_receitaws",
        lambda cnpj: {"status": "ERROR"},
    )
    monkeypatch.setattr(
        "consultor_cnpj.core.consultar_brasilapi",
        lambda cnpj: {"message": "not found"},
    )

    assert status_detalhado(CNPJ_VALIDO) == {"error": "CNPJ_NAO_ENCONTRADO"}
