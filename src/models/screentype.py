from enum import Enum


class ScreenType(Enum):
    CASOS = "casos"
    ENCADEADOR = "encadeador"
    PPQ = "ppquente"

    @staticmethod
    def factory(s: str) -> "ScreenType":
        for status in ScreenType:
            if status.value == s:
                return status
        return ScreenType.CASOS
