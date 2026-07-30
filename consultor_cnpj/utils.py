"""
Funções utilitárias para validação e formatação de CNPJ
"""

from typing import Dict, List


def formatar_cnpj(cnpj: str) -> str:
    """Remove caracteres especiais do CNPJ"""
    return ''.join(filter(str.isdigit, cnpj))


def formatar_cnpj_visual(cnpj: str) -> str:
    """Formata o CNPJ visualmente (XX.XXX.XXX/XXXX-XX)"""
    cnpj_limpo = formatar_cnpj(cnpj)
    if len(cnpj_limpo) != 14:
        return cnpj_limpo
    return (
        f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}"
        f"/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
    )


def validar_cnpj(cnpj: str) -> bool:
    """Valida CNPJ usando algoritmo de validação"""
    cnpj_limpo = formatar_cnpj(cnpj)

    # Verifica tamanho
    if len(cnpj_limpo) != 14:
        return False

    # Verifica se todos os dígitos são iguais
    if len(set(cnpj_limpo)) == 1:
        return False

    # Calcula primeiro dígito verificador
    soma = 0
    peso = 5
    for i in range(12):
        soma += int(cnpj_limpo[i]) * peso
        peso -= 1
        if peso < 2:
            peso = 9

    digito = 11 - (soma % 11)
    if digito > 9:
        digito = 0

    if int(cnpj_limpo[12]) != digito:
        return False

    # Calcula segundo dígito verificador
    soma = 0
    peso = 6
    for i in range(13):
        soma += int(cnpj_limpo[i]) * peso
        peso -= 1
        if peso < 2:
            peso = 9

    digito = 11 - (soma % 11)
    if digito > 9:
        digito = 0

    return int(cnpj_limpo[13]) == digito


def gerar_relatorio(cnpjs: List[str]) -> Dict:
    """
    Gera relatório de múltiplos CNPJs

    Args:
        cnpjs: Lista de CNPJs

    Returns:
        Dict com estatísticas
    """
    from .core import cnpj_status

    resultados = {
        'total': len(cnpjs),
        'validos': 0,
        'invalidos': 0,
        'ativos': 0,
        'inativos': 0,
        'detalhes': {}
    }

    for cnpj in cnpjs:
        status = cnpj_status(cnpj)
        resultados['detalhes'][cnpj] = status

        if 'ERRO' in status:
            resultados['invalidos'] += 1
        else:
            resultados['validos'] += 1
            if 'ATIVA' in status:
                resultados['ativos'] += 1
            else:
                resultados['inativos'] += 1

    return resultados
