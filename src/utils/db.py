from datetime import datetime
from io import StringIO
from typing import List, Optional

import pandas as pd

from src.models.screen import Screen
from src.models.screenstudy import ScreenStudy
from src.models.screentype import ScreenType
from src.models.study import Study
from src.services.unitofwork import SQLUnitOfWork
from src.utils.log import Log
from src.utils.settings import Settings


def find_screen_type_in_url(url: str) -> str:
    valid = url.split(Settings.url_prefix)[1]
    parts = valid.split("/")
    kind = parts[0]
    return kind


def _create_screen(
    screen_name: str, screen_type: ScreenType, studies: List[Study]
):
    uow = SQLUnitOfWork()
    with uow:
        screen = Screen(screen_name, screen_type, datetime.now())
        uow.screens.create(screen)
        uow.commit()
        for study in studies:
            uow.studies.create(study)
            uow.commit()
            screen_study = ScreenStudy(screen.screen_id, study.study_id)
            uow.screen_studies.create(screen_study)
            uow.commit()


def _delete_screen(screen_name: str):
    uow = SQLUnitOfWork()
    with uow:
        screen = uow.screens.read_by_name(screen_name)
        screen_studies = uow.screen_studies.list_by_screen(screen.screen_id)
        studies = [uow.studies.read(ss.study_id) for ss in screen_studies]
        uow.screen_studies.delete(screen.screen_id)
        for study in studies:
            uow.studies.delete(study.study_id)
        uow.screens.delete(screen.screen_id)
        uow.commit()


def _update_screen(
    screen_name: str, screen_type: ScreenType, studies: List[Study]
):
    _delete_screen(screen_name)
    if len(studies) > 0:
        _create_screen(screen_name, screen_type, studies)


def create_or_update_screen(
    screen_name: str, screen_type_str: str, current_studies
):
    screen_type = ScreenType.factory(screen_type_str)
    studies_df = pd.read_json(StringIO(current_studies), orient="split")
    if studies_df.shape[0] == 0:
        return None
    studies_df["created_date"] = pd.to_datetime(studies_df["created_date"])
    studies = Study.from_df(studies_df)
    uow = SQLUnitOfWork()
    should_update = False
    with uow:
        existing_screens = uow.screens.list()
        should_update = any([e.name == screen_name for e in existing_screens])
    if should_update:
        Log.log().info(f"Atualizando TELA - {screen_type}/{screen_name}")
        _update_screen(screen_name, screen_type, studies)
    else:
        Log.log().info(f"Criando TELA - {screen_type}/{screen_name}")
        _create_screen(screen_name, screen_type, studies)


def load_screen(
    screen_name: str, screen_type_str: str
) -> Optional[pd.DataFrame]:
    Log.log().info(f"Carregando TELA - {screen_name}")
    uow = SQLUnitOfWork()
    with uow:
        screen_type = ScreenType.factory(screen_type_str)
        screens = uow.screens.list_by_type(screen_type)
        selected_screens = [s for s in screens if s.name == screen_name]
        if len(selected_screens) == 1:
            screen_studies = uow.screen_studies.list_by_screen(
                selected_screens[0].screen_id
            )
            studies_ids = [s.study_id for s in screen_studies]
            if len(studies_ids) > 0:
                studies = [
                    s for s in uow.studies.list() if s.study_id in studies_ids
                ]
                return pd.DataFrame(
                    data={
                        "study_id": [s.study_id for s in studies],
                        "table_id": [s.table_id for s in studies],
                        "path": [s.path for s in studies],
                        "name": [s.name for s in studies],
                        "color": [s.color for s in studies],
                        "created_date": [s.created_date for s in studies],
                    }
                )
        else:
            return None


def list_screens(screen_type_str: str) -> List[str]:
    uow = SQLUnitOfWork()
    with uow:
        screen_type = ScreenType.factory(screen_type_str)
        screens: list = uow.screens.list_by_type(screen_type)
        screens.sort(reverse=True)
        return [s.name for s in screens]
