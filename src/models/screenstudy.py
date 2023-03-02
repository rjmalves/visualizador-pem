class ScreenStudy:
    def __init__(
        self,
        screen_id: int,
        study_id: int,
    ) -> None:
        self.id == None
        self.screen_id = screen_id
        self.study_id = study_id

    def __eq__(self, o: object):
        if not isinstance(o, ScreenStudy):
            return False
        return all(
            [
                self.screen_id == o.screen_id,
                self.study_id == o.study_id,
            ]
        )
