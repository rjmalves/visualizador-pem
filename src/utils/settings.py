import os
import socket
import fcntl
import struct


def __get_ip_address(ifname: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack("256s".encode("utf-8"), ifname[:15].encode("utf-8")),
        )[20:24]
    )


LOCALHOST = __get_ip_address("eth0")


class Settings:
    basedir = os.getenv("BASEDIR")
    mode = os.getenv("MODE", "DEV")
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5050"))
    storage = os.getenv("STORAGE", "session")
    result_api = os.getenv("RESULT_API", f"http://{LOCALHOST}:5048/results")
    api_key = os.getenv("API_KEY", "")
    graphs_update_period = int(os.getenv("GRAPHS_UPDATE_PERIOD", "600000"))
    current_state_update_period = int(
        os.getenv("CURRENT_STATE_UPDATE_PERIOD", "30000")
    )
    url_prefix = os.getenv("URL_PREFIX", "/")
    synthesis_dir = os.getenv("SYNTHESIS_DIR", "sintese")
    newave_dir = os.getenv("NEWAVE_DIR", "NEWAVE")
    decomp_dir = os.getenv("DECOMP_DIR", "DECOMP")
    secret_key = os.getenv("SECRET_KEY", "test")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")

    @classmethod
    def read_environments(cls):
        cls.basedir = os.getenv("BASEDIR")
        cls.mode = os.getenv("MODE", "DEV")
        cls.host = os.getenv("HOST", "0.0.0.0")
        cls.port = int(os.getenv("PORT", "5050"))
        cls.storage = os.getenv("STORAGE", "session")
        cls.result_api = os.getenv(
            "RESULT_API", f"http://{LOCALHOST}:5048/results"
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
        cls.secret_key = os.getenv("SECRET_KEY", "test")
        cls.user = os.getenv("USER")
        cls.password = os.getenv("PASSWORD")
