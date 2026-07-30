#!/usr/bin/env python3
"""
Exemplo de processamento em lote: consulta vários CNPJs e gera um relatório.
"""

from consultor_cnpj.utils import gerar_relatorio

CNPJS = [
    "11.222.333/0001-81",
    "00.000.000/0001-91",
    "123",  # CNPJ inválido, propositalmente, para aparecer no relatório
]


def main():
    relatorio = gerar_relatorio(CNPJS)

    print(f"Total consultado: {relatorio['total']}")
    print(f"Válidos: {relatorio['validos']}")
    print(f"Inválidos: {relatorio['invalidos']}")
    print(f"Ativos: {relatorio['ativos']}")
    print(f"Inativos: {relatorio['inativos']}")

    print("\nDetalhes:")
    for cnpj, status in relatorio["detalhes"].items():
        print(f"  {cnpj}: {status}")


if __name__ == "__main__":
    main()
