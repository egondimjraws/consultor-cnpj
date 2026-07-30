"""
Módulo para integração com APIs de CNPJ
"""

import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import Optional, Dict


def _fazer_requisicao(url: str, timeout: int = 10) -> Optional[Dict]:
    """
    Faz requisição HTTP com tratamento de erros

    Args:
        url: URL para requisição
        timeout: Timeout em segundos

    Returns:
        Dict com resposta ou None em caso de erro
    """
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        with urlopen(req, timeout=timeout) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)

    except HTTPError as e:
        if e.code == 404:
            return {'error': 'Not Found'}
        return {'error': f'HTTP {e.code}: {e.reason}'}

    except URLError as e:
        return {'error': f'Connection error: {e.reason}'}

    except json.JSONDecodeError as e:
        return {'error': f'Invalid JSON: {e}'}

    except Exception as e:
        return {'error': f'Unexpected error: {e}'}


def consultar_receitaws(cnpj: str) -> Optional[Dict]:
    """
    Consulta CNPJ na API da ReceitaWS

    Args:
        cnpj: CNPJ apenas números

    Returns:
        Dict com dados ou None
    """
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    return _fazer_requisicao(url)


def consultar_brasilapi(cnpj: str) -> Optional[Dict]:
    """
    Consulta CNPJ na API da BrasilAPI

    Args:
        cnpj: CNPJ apenas números

    Returns:
        Dict com dados ou None
    """
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    return _fazer_requisicao(url)
