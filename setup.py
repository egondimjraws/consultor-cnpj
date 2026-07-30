"""
Configuração de instalação do pacote
"""

from setuptools import setup, find_packages

setup(
    name="consultor-cnpj",
    version="1.0.0",
    author="Emanuel Gondim",
    author_email="egondimjraws@gmail.com",
    description="Consulta de CNPJ com fallback automático entre APIs",
    long_description="Consulta de CNPJ com fallback automático entre APIs",
    url="https://github.com/egondimjraws/consultor-cnpj",
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "cnpj-consultor=consultor_cnpj.cli:main",
        ],
    },
)
