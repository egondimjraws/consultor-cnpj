#!/usr/bin/env python3
"""
Interface de linha de comando para o consultor CNPJ
"""

import sys
from .core import cnpj_status
from .utils import validar_cnpj


def main():
    """Função principal do CLI"""

    # Se recebeu argumento via CLI
    if len(sys.argv) > 1:
        cnpj = sys.argv[1]

        # Validação rápida
        if not validar_cnpj(cnpj):
            print("CNPJ_INVALIDO | ERRO")
            return

        resultado = cnpj_status(cnpj)
        print(resultado)
        return

    # Modo interativo
    print("=" * 60)
    print("🔍 CONSULTOR CNPJ - EMPRESA | STATUS")
    print("=" * 60)
    print("\nDigite um CNPJ para consultar ou 'sair' para encerrar")
    print("Exemplo: 06.990.590/0001-23 ou 06990590000123\n")

    while True:
        try:
            cnpj = input("CNPJ: ").strip()

            if cnpj.lower() in ['sair', 'exit', 'quit']:
                print("👋 Encerrando...")
                break

            if not cnpj:
                print("⚠️ Digite um CNPJ válido")
                continue

            # Validação local
            if not validar_cnpj(cnpj):
                print("  CNPJ_INVALIDO | ERRO")
                continue

            resultado = cnpj_status(cnpj)
            print(f"  {resultado}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Encerrando...")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}\n")


if __name__ == "__main__":
    main()
