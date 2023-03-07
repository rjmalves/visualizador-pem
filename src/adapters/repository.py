from abc import ABC, abstractmethod
from sqlalchemy import select, update, delete  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from typing import List, Dict, Optional, Type
from pathlib import Path
from os.path import exists
from os import makedirs
from json import dump, load
from datetime import datetime

from src.models.study import Study
from src.models.screen import Screen
from src.models.screentype import ScreenType
from src.models.screenstudy import ScreenStudy


class SQLStudyRepository:
    def __init__(self, session: Session):
        self.__session = session

    def create(self, rodada: Study):
        return self.__session.add(rodada)

    def read(self, id: int) -> Optional[Study]:
        statement = select(Study).filter_by(study_id=id)
        try:
            j = self.__session.execute(statement).one()[0]
            return j
        except Exception:
            return None

    def update(self, study: Study):
        statement = (
            update(Study)
            .where(Study.study_id == study.study_id)
            .values(
                {
                    "path": study.path,
                    "name": study.name,
                    "color": study.color,
                }
            )
        )
        return self.__session.execute(statement)

    def delete(self, id: int):
        statement = delete(Study).where(Study.study_id == id)
        return self.__session.execute(statement)

    def list(self) -> List[Study]:
        statement = select(Study)
        return [j[0] for j in self.__session.execute(statement).all()]


class SQLScreenRepository:
    def __init__(self, session: Session):
        self.__session = session

    def create(self, rodada: Screen):
        return self.__session.add(rodada)

    def read(self, id: int) -> Optional[Screen]:
        statement = select(Screen).filter_by(screen_id=id)
        try:
            j = self.__session.execute(statement).one()[0]
            return j
        except Exception:
            return None

    def read_by_name(self, name: str) -> Optional[Screen]:
        statement = select(Screen).filter_by(name=name)
        try:
            j = self.__session.execute(statement).one()[0]
            return j
        except Exception:
            return None

    def update(self, screen: Screen):
        statement = (
            update(Screen)
            .where(Screen.screen_id == screen.id)
            .values(
                {
                    "name": screen.name,
                }
            )
        )
        return self.__session.execute(statement)

    def delete(self, id: int):
        statement = delete(Screen).where(Screen.screen_id == id)
        return self.__session.execute(statement)

    def list(self) -> List[Screen]:
        statement = select(Screen)
        return [j[0] for j in self.__session.execute(statement).all()]

    def list_by_type(self, type: ScreenType) -> List[Screen]:
        statement = select(Screen).where(Screen.type == type)
        return [j[0] for j in self.__session.execute(statement).all()]


class SQLScreenStudyRepository:
    def __init__(self, session: Session):
        self.__session = session

    def create(self, rodada: ScreenStudy):
        return self.__session.add(rodada)

    def delete(self, screen_id: int):
        statement = delete(ScreenStudy).where(
            ScreenStudy.screen_id == screen_id
        )
        return self.__session.execute(statement)

    def list(self) -> List[ScreenStudy]:
        statement = select(ScreenStudy)
        return [j[0] for j in self.__session.execute(statement).all()]

    def list_by_screen(self, screen_id: int) -> List[ScreenStudy]:
        statement = select(ScreenStudy).where(
            ScreenStudy.screen_id == screen_id
        )
        return [j[0] for j in self.__session.execute(statement).all()]
