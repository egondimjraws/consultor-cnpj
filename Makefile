.PHONY: help install test lint format clean build publish

help:
	@echo "Comandos disponíveis:"
	@echo "  install      Instala as dependências"
	@echo "  test         Executa os testes"
	@echo "  lint         Verifica o código com flake8"
	@echo "  format       Formata o código com black"
	@echo "  clean        Remove arquivos temporários"
	@echo "  build        Constrói o pacote"
	@echo "  publish      Publica no PyPI"

install:
	pip install -r requirements-dev.txt
	pip install -e .

test:
	pytest tests/ -v --cov=consultor_cnpj --cov-report=html

lint:
	flake8 consultor_cnpj tests
	mypy consultor_cnpj

format:
	black consultor_cnpj tests
	isort consultor_cnpj tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	twine upload dist/*