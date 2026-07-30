"""
Testes para consultor_cnpj.api
"""

import json
from urllib.error import HTTPError, URLError

from consultor_cnpj.api import (
    _fazer_requisicao,
    consultar_receitaws,
    consultar_brasilapi,
)


class _RespostaFalsa:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_fazer_requisicao_retorna_json_decodificado(monkeypatch):
    monkeypatch.setattr(
        "consultor_cnpj.api.urlopen",
        lambda req, timeout=10: _RespostaFalsa({"nome": "EMPRESA TESTE"}),
    )

    resultado = _fazer_requisicao("https://exemplo.com")

    assert resultado == {"nome": "EMPRESA TESTE"}


def test_fazer_requisicao_trata_http_error_404(monkeypatch):
    def levantar_erro(req, timeout=10):
        raise HTTPError("https://exemplo.com", 404, "Not Found", {}, None)

    monkeypatch.setattr("consultor_cnpj.api.urlopen", levantar_erro)

    resultado = _fazer_requisicao("https://exemplo.com")

    assert resultado == {"error": "Not Found"}


def test_fazer_requisicao_trata_url_error(monkeypatch):
    def levantar_erro(req, timeout=10):
        raise URLError("conexão recusada")

    monkeypatch.setattr("consultor_cnpj.api.urlopen", levantar_erro)

    resultado = _fazer_requisicao("https://exemplo.com")

    assert "error" in resultado


def test_consultar_receitaws_monta_url_correta(monkeypatch):
    urls_chamadas = []

    def fake_fazer_requisicao(url, timeout=10):
        urls_chamadas.append(url)
        return {"nome": "EMPRESA TESTE"}

    monkeypatch.setattr("consultor_cnpj.api._fazer_requisicao", fake_fazer_requisicao)

    consultar_receitaws("11222333000181")

    assert urls_chamadas == ["https://www.receitaws.com.br/v1/cnpj/11222333000181"]


def test_consultar_brasilapi_monta_url_correta(monkeypatch):
    urls_chamadas = []

    def fake_fazer_requisicao(url, timeout=10):
        urls_chamadas.append(url)
        return {"nome": "EMPRESA TESTE"}

    monkeypatch.setattr("consultor_cnpj.api._fazer_requisicao", fake_fazer_requisicao)

    consultar_brasilapi("11222333000181")

    assert urls_chamadas == ["https://brasilapi.com.br/api/cnpj/v1/11222333000181"]
