"""
Lógica principal do consultor de CNPJ
"""

from typing import Dict
from .api import consultar_receitaws, consultar_brasilapi
from .utils import formatar_cnpj, validar_cnpj
from .exceptions import InvalidCNPJError, APIError


def consultar_cnpj(cnpj: str) -> Dict:
    """
    Consulta CNPJ com fallback automático entre APIs

    Args:
        cnpj: CNPJ com ou sem formatação

    Returns:
        Dict com dados do CNPJ ou erro

    Raises:
        InvalidCNPJError: Quando o CNPJ é inválido
        APIError: Quando todas as APIs falham
    """
    cnpj_limpo = formatar_cnpj(cnpj)

    if not validar_cnpj(cnpj_limpo):
        raise InvalidCNPJError(f"CNPJ inválido: {cnpj}")

    # Tenta ReceitaWS primeiro
    dados = consultar_receitaws(cnpj_limpo)
    if dados and dados.get('status') != 'ERROR':
        return dados

    # Fallback para BrasilAPI
    dados = consultar_brasilapi(cnpj_limpo)
    if dados and 'message' not in dados:
        return dados

    raise APIError("Todas as APIs falharam na consulta")


def cnpj_status(cnpj: str) -> str:
    """
    Retorna EMPRESA | STATUS para o CNPJ informado

    Args:
        cnpj: CNPJ com ou sem formatação

    Returns:
        String no formato "EMPRESA | STATUS"
    """
    try:
        dados = consultar_cnpj(cnpj)

        nome = dados.get('nome', 'NOME_NAO_DISPONIVEL')
        status = dados.get('situacao', dados.get('situacao_cadastral', 'STATUS_INDISPONIVEL'))

        return f"{nome} | {status}"

    except InvalidCNPJError:
        return "CNPJ_INVALIDO | ERRO"
    except APIError:
        return "NAO_ENCONTRADO | ERRO"
    except Exception:
        return "ERRO_INESPERADO | ERRO"


def status_detalhado(cnpj: str) -> Dict:
    """
    Retorna status detalhado da empresa

    Args:
        cnpj: CNPJ com ou sem formatação

    Returns:
        Dict com dados detalhados
    """
    try:
        dados = consultar_cnpj(cnpj)

        return {
            'cnpj': formatar_cnpj(cnpj),
            'nome': dados.get('nome', 'N/A'),
            'status': dados.get('situacao', dados.get('situacao_cadastral', 'N/A')),
            'abertura': dados.get('abertura', 'N/A'),
            'atividade_principal': dados.get('atividade_principal', [{}])[0].get('text', 'N/A'),
            'cidade': dados.get('municipio', 'N/A'),
            'uf': dados.get('uf', 'N/A'),
            'telefone': dados.get('telefone', 'N/A')
        }
    except (InvalidCNPJError, APIError):
        return {'error': 'CNPJ_NAO_ENCONTRADO'}
