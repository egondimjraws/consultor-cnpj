#!/usr/bin/env python3
"""
Exemplo básico: validar, formatar e consultar um único CNPJ.
"""

from consultor_cnpj import consultar_cnpj, cnpj_status, formatar_cnpj, validar_cnpj
from consultor_cnpj.exceptions import InvalidCNPJError, APIError

CNPJ = "11.222.333/0001-81"


def main():
    print(f"CNPJ informado: {CNPJ}")
    print(f"CNPJ limpo: {formatar_cnpj(CNPJ)}")
    print(f"CNPJ válido? {validar_cnpj(CNPJ)}")

    # Formato padronizado "EMPRESA | STATUS", nunca levanta exceção
    print(f"Status: {cnpj_status(CNPJ)}")

    # Consulta com o dicionário bruto retornado pela API, para quem
    # precisa dos dados completos e quer tratar os erros manualmente
    try:
        dados = consultar_cnpj(CNPJ)
        print(f"Dados brutos: {dados}")
    except InvalidCNPJError:
        print("CNPJ inválido.")
    except APIError:
        print("Não foi possível consultar nenhuma das APIs.")


if __name__ == "__main__":
    main()
