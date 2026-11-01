import subprocess
import sys
from pathlib import Path

PASTA_SRC = Path(__file__).resolve().parent

etapas = [
    "extrair_cdi.py",
    "extrair_dolar.py",
    "extrair_ibovespa.py",
    "extrair_ipca.py",
    "juntar_series.py",
]

for nome in etapas:
    print(f"\n=== Rodando {nome} ===")
    resultado = subprocess.run([sys.executable, str(PASTA_SRC / nome)])
    if resultado.returncode != 0:
        print(f"\nERRO em {nome}. Pipeline interrompido.")
        sys.exit(1)

print("\nPipeline concluído com sucesso.")