import sqlalchemy.orm  # type: ignore

registry = sqlalchemy.orm.registry()

from sqlalchemy import (  # type: ignore
    Table,
    Column,
    Integer,
    ForeignKey,
    String,
    DateTime,
    Enum,
)

from src.models.screen import Screen
from src.models.screentype import ScreenType
from src.models.study import Study
from src.models.screenstudy import ScreenStudy


study_table = Table(
    "studies",
    registry.metadata,
    Column("study_id", Integer, primary_key=True, autoincrement=True),
    Column("table_id", Integer, nullable=False),
    Column("path", String(255), nullable=False),
    Column("name", String(255), nullable=False),
    Column("color", String(255), nullable=False),
    Column("created_date", DateTime),
)


screen_table = Table(
    "screens",
    registry.metadata,
    Column("screen_id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), unique=True),
    Column("type", Enum(ScreenType)),
    Column("created_date", DateTime),
)

screen_studies_table = Table(
    "screenstudies",
    registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("screen_id", ForeignKey("screens.screen_id")),
    Column("study_id", ForeignKey("studies.study_id")),
)


def start_mappers():
    registry.map_imperatively(Screen, screen_table)
    registry.map_imperatively(Study, study_table)
    registry.map_imperatively(ScreenStudy, screen_studies_table)
