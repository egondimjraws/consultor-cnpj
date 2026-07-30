"""
Exceções personalizadas do projeto
"""


class CNPJError(Exception):
    """Exceção base para erros do CNPJ"""
    pass


class InvalidCNPJError(CNPJError):
    """Exceção para CNPJ inválido"""
    pass


class APIError(CNPJError):
    """Exceção para erros nas APIs"""
    pass


class RateLimitError(APIError):
    """Exceção para limite de requisições"""
    pass
