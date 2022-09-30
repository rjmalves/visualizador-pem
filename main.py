import pathlib
from os.path import join
from dotenv import load_dotenv

from visualizador.modelos.configuracoes import Configuracoes
from visualizador.modelos.log import Log
from visualizador.app import App, CFG_FILENAME

# Lê as configurações das variáveis de ambiente
load_dotenv(override=True)

DIR_BASE = pathlib.Path().resolve()

load_dotenv(join(DIR_BASE, CFG_FILENAME), override=True)

if __name__ == "__main__":
    Log.configura_logging(DIR_BASE)
    Configuracoes.le_variaveis_ambiente()
    app = App()
    app.serve()
