import pandas as pd
import os

PARES_NOMES = {
    "Estagio": "estagio",
    "Patamar": "patamar",
    "Usina": "usina",
    "REE": "ree",
    "Submercado": "submercado",
    "Submercado De": "submercadoDe",
    "Submercado Para": "submercadoPara",
    "Data Inicio": "dataInicio",
    "Data Fim": "dataFim",
}

DIRETORIO = (
    "/home/rogerio/git/visualizador-encadeador-pem/tests/2540/NEWAVE/sintese"
)

arquivos = os.listdir(DIRETORIO)
for a in arquivos:
    caminho = os.path.join(DIRETORIO, a)
    df = pd.read_parquet(caminho)
    df = df.rename(columns=PARES_NOMES)
    df.to_parquet(caminho, compression="gzip")
