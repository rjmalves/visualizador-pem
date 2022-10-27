import pathlib
from dotenv import load_dotenv

from src.utils.settings import Settings

# Lê as configurações das variáveis de ambiente
load_dotenv(override=True)

BASEDIR = pathlib.Path().resolve()
Settings.read_environments()

if __name__ == "__main__":
    from src.utils.log import Log
    from src.app import App

    Log.config_logging(BASEDIR)
    app = App()
    app.serve()
