"""
Testes para consultor_cnpj.utils
"""

from consultor_cnpj.utils import (
    formatar_cnpj,
    formatar_cnpj_visual,
    validar_cnpj,
    gerar_relatorio,
)

CNPJ_VALIDO = "11222333000181"


def test_formatar_cnpj_remove_caracteres_especiais():
    assert formatar_cnpj("11.222.333/0001-81") == CNPJ_VALIDO


def test_formatar_cnpj_ja_limpo():
    assert formatar_cnpj(CNPJ_VALIDO) == CNPJ_VALIDO


def test_formatar_cnpj_visual():
    assert formatar_cnpj_visual(CNPJ_VALIDO) == "11.222.333/0001-81"


def test_formatar_cnpj_visual_com_tamanho_invalido_retorna_original():
    assert formatar_cnpj_visual("123") == "123"


def test_validar_cnpj_valido():
    assert validar_cnpj(CNPJ_VALIDO) is True


def test_validar_cnpj_formatado_valido():
    assert validar_cnpj("11.222.333/0001-81") is True


def test_validar_cnpj_tamanho_invalido():
    assert validar_cnpj("123") is False


def test_validar_cnpj_digitos_repetidos():
    assert validar_cnpj("11111111111111") is False


def test_validar_cnpj_digito_verificador_invalido():
    assert validar_cnpj("11222333000199") is False


def test_gerar_relatorio_conta_validos_e_invalidos(monkeypatch):
    def fake_cnpj_status(cnpj):
        if cnpj == CNPJ_VALIDO:
            return "EMPRESA TESTE | ATIVA"
        return "CNPJ_INVALIDO | ERRO"

    monkeypatch.setattr("consultor_cnpj.core.cnpj_status", fake_cnpj_status)

    resultado = gerar_relatorio([CNPJ_VALIDO, "123"])

    assert resultado["total"] == 2
    assert resultado["validos"] == 1
    assert resultado["invalidos"] == 1
    assert resultado["ativos"] == 1
    assert resultado["inativos"] == 0
