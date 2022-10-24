import os


class Settings:
    mode = os.getenv("MODE", "DEV")
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5050"))
    result_api = os.getenv("RESULT_API", "http://172.24.173.136:5048/results")
    api_key = os.getenv("API_KEY", "")
    graphs_update_period = int(os.getenv("GRAPHS_UPDATE_PERIOD", "600000"))
    current_state_update_period = int(
        os.getenv("CURRENT_STATE_UPDATE_PERIOD", "30000")
    )
    url_prefix = os.getenv("URL_PREFIX", "/")
    synthesis_dir = os.getenv("SYNTHESIS_DIR", "sintese")
    newave_dir = os.getenv("NEWAVE_DIR", "NEWAVE")
    decomp_dir = os.getenv("DECOMP_DIR", "DECOMP")

    @classmethod
    def read_environments(cls):
        cls.mode = os.getenv("MODE", "DEV")
        cls.host = os.getenv("HOST", "0.0.0.0")
        cls.port = int(os.getenv("PORT", "5050"))
        cls.result_api = os.getenv(
            "RESULT_API", "http://172.24.173.136:5048/results"
        )
        cls.api_key = os.getenv("API_KEY", "")
        cls.graphs_update_period = int(
            os.getenv("GRAPHS_UPDATE_PERIOD", "600000")
        )
        cls.current_state_update_period = int(
            os.getenv("CURRENT_STATE_UPDATE_PERIOD", "30000")
        )
        cls.url_prefix = os.getenv("URL_PREFIX", "/")
        cls.synthesis_dir = os.getenv("SYNTHESIS_DIR", "sintese")
        cls.newave_dir = os.getenv("NEWAVE_DIR", "NEWAVE")
        cls.decomp_dir = os.getenv("DECOMP_DIR", "DECOMP")
