#!/usr/bin/env python3
"""
Exemplo de formatação: diferentes representações de um mesmo CNPJ.
"""

from consultor_cnpj import formatar_cnpj
from consultor_cnpj.utils import formatar_cnpj_visual

ENTRADAS = [
    "11222333000181",
    "11.222.333/0001-81",
    "11 222 333 0001 81",
]


def main():
    for entrada in ENTRADAS:
        limpo = formatar_cnpj(entrada)
        visual = formatar_cnpj_visual(entrada)
        print(f"Entrada: {entrada!r:30} -> limpo: {limpo} | visual: {visual}")


if __name__ == "__main__":
    main()
