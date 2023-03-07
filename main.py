import pathlib
from dotenv import load_dotenv
import os

from src.utils.settings import Settings
from src.utils.setup import start_db

# Lê as configurações das variáveis de ambiente
load_dotenv(override=True)

BASEDIR = pathlib.Path().resolve()
os.environ["BASEDIR"] = str(BASEDIR)
Settings.read_environments()

if __name__ == "__main__":
    from src.utils.log import Log
    from src.app import App

    Log.config_logging(BASEDIR)
    start_db()
    app = App()
    app.serve()
