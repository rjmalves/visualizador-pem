from typing import List
from src.models.screentype import ScreenType
from datetime import datetime


class Screen:
    def __init__(
        self, name: str, type: ScreenType, created_date: datetime
    ) -> None:
        self.screen_id: int = None  # type: ignore
        self.name = name
        self.type = type
        self.created_date = created_date

    def __eq__(self, o: object):
        if not isinstance(o, Screen):
            return False
        return all(
            [
                self.screen_id == o.screen_id,
                self.name == o.name,
                self.type == o.type,
                self.created_date == o.created_date,
            ]
        )
