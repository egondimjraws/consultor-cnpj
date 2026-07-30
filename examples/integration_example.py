#!/usr/bin/env python3
"""
Exemplo de integração: checar uma carteira de fornecedores e sinalizar
os que estão com CNPJ inválido ou situação cadastral inativa.
"""

from consultor_cnpj.core import status_detalhado

FORNECEDORES = {
    "Fornecedor A": "11.222.333/0001-81",
    "Fornecedor B": "00.000.000/0001-91",
    "Fornecedor C": "123",
}


def checar_fornecedores(fornecedores):
    pendencias = []

    for nome, cnpj in fornecedores.items():
        dados = status_detalhado(cnpj)

        if "error" in dados:
            pendencias.append((nome, cnpj, "CNPJ não encontrado ou inválido"))
            continue

        if dados["status"] not in ("ATIVA", "N/A"):
            pendencias.append((nome, cnpj, f"situação: {dados['status']}"))

    return pendencias


def main():
    pendencias = checar_fornecedores(FORNECEDORES)

    if not pendencias:
        print("Todos os fornecedores estão com CNPJ ativo.")
        return

    print("Fornecedores que precisam de atenção:")
    for nome, cnpj, motivo in pendencias:
        print(f"  {nome} ({cnpj}): {motivo}")


if __name__ == "__main__":
    main()
