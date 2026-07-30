"""
CNPJ Consultor - Consulta de CNPJ com fallback automático entre APIs
"""

from .core import consultar_cnpj, cnpj_status
from .api import consultar_receitaws, consultar_brasilapi
from .utils import validar_cnpj, formatar_cnpj
from .exceptions import CNPJError, APIError, InvalidCNPJError
from .__version__ import __version__

__all__ = [
    'consultar_cnpj',
    'cnpj_status',
    'consultar_receitaws',
    'consultar_brasilapi',
    'validar_cnpj',
    'formatar_cnpj',
    'CNPJError',
    'APIError',
    'InvalidCNPJError',
    '__version__'
]
