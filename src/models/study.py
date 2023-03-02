from datetime import datetime


class Study:
    def __init__(
        self,
        table_id: int,
        path: str,
        name: str,
        color: str,
        created_date: datetime,
    ) -> None:
        self.study_id: int = None  # type: ignore
        self.table_id = table_id
        self.path = path
        self.name = name
        self.color = color
        self.created_date = created_date

    def __eq__(self, o: object):
        if not isinstance(o, Study):
            return False
        return all(
            [
                self.study_id == o.study_id,
                self.table_id == o.table_id,
                self.path == o.path,
                self.name == o.name,
                self.color == o.color,
                self.created_date == o.created_date,
            ]
        )
