from src.services.unitofwork import SQLUnitOfWork
from src.utils.settings import Settings
from src.models.screentype import ScreenType
from typing import Optional
import pandas as pd


def find_screen_type_in_url(url: str) -> str:
    valid = url.split(Settings.url_prefix)[1]
    parts = valid.split("/")
    if len(parts) == 1:
        kind = ""
    elif len(parts) == 2:
        kind = parts[0]
    return kind


def find_studies_by_url(url: str) -> Optional[pd.DataFrame]:
    valid = url.split(Settings.url_prefix)[1]
    parts = valid.split("/")
    name = ""
    if len(parts) == 1:
        if len(parts[0]) == 0:
            studies = None
        else:
            kind = ScreenType.factory("")
            name = parts[0]
    elif len(parts) == 2:
        kind = ScreenType.factory(parts[0])
        name = parts[1]
    if len(name) > 0:
        uow = SQLUnitOfWork()
        with uow:
            screens = uow.screens.list_by_type(kind)
            selected_screens = [s for s in screens if s.name == name]
            if len(selected_screens) == 1:
                screen_studies = uow.screen_studies.list_by_screen(
                    selected_screens[0].screen_id
                )
                studies_ids = [s.study_id for s in screen_studies]
                if len(studies_ids) > 0:
                    studies = [
                        s
                        for s in uow.studies.list()
                        if s.study_id in studies_ids
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
                studies = None
    else:
        studies = None

    return studies
