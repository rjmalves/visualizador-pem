from dash import (
    Output,
    Input,
    State,
    html,
    dcc,
    callback,
    MATCH,
    dash_table,
    ctx,
    no_update,
)
from flask_login import current_user
import dash_bootstrap_components as dbc
import pandas as pd
import uuid
import re
import src.utils.db as db
from src.utils.log import Log


class SaveScreenModal(html.Div):
    class ids:
        new_screen_name = lambda aio_id: {
            "component": "SaveScreenModal",
            "subcomponent": "new_screen_name",
            "aio_id": aio_id,
        }
        confirm_save_screen_btn = lambda aio_id: {
            "component": "SaveScreenModal",
            "subcomponent": "confirm_save_screen_btn",
            "aio_id": aio_id,
        }
        modal = lambda aio_id: {
            "component": "SaveScreenModal",
            "subcomponent": "modal",
            "aio_id": aio_id,
        }
        modal_container = lambda aio_id: {
            "component": "SaveScreenModal",
            "subcomponent": "modal_container",
            "aio_id": aio_id,
        }
        screen_type_str = lambda aio_id: {
            "component": "SaveScreenModal",
            "subcomponent": "screen_type_str",
            "aio_id": aio_id,
        }
        current_studies = lambda aio_id: {
            "component": "SaveScreenModal",
            "subcomponent": "current_studies",
            "aio_id": aio_id,
        }
        no_op = lambda aio_id: {
            "component": "SaveScreenModal",
            "subcomponent": "no_op",
            "aio_id": aio_id,
        }

    # Make the ids class a public class
    ids = ids

    # Define the arguments of the All-in-One component
    def __init__(
        self,
        aio_id=None,
    ):

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # Define the component's layout
        super().__init__(
            [
                dbc.Modal(
                    [
                        dbc.Form(
                            [
                                dbc.ModalHeader(
                                    dbc.ModalTitle(
                                        "ADICIONE UM CONJUNTO DE ESTUDOS",
                                        className="card-title",
                                    )
                                ),
                                dbc.ModalBody(
                                    [
                                        dbc.Label(
                                            "Nome do Conjunto",
                                            className="modal-form-comment",
                                        ),
                                        dbc.Input(
                                            placeholder="Insira um nome (deve possuir apenas caracteres alfanuméricos e '-'. )",
                                            id=self.ids.new_screen_name(
                                                aio_id
                                            ),
                                            className="modal-input-field",
                                            type="text",
                                            valid=False,
                                        ),
                                    ]
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Confirmar",
                                        id=self.ids.confirm_save_screen_btn(
                                            aio_id
                                        ),
                                        className="modal-button",
                                        disabled=True,
                                    )
                                ),
                            ]
                        )
                    ],
                    id=self.ids.modal(aio_id),
                    is_open=False,
                    backdrop=True,
                    keyboard=True,
                    centered=True,
                    size="lg",
                    fade=True,
                ),
                dcc.Store(
                    id=self.ids.screen_type_str(aio_id), storage_type="memory"
                ),
                dcc.Store(
                    id=self.ids.current_studies(aio_id), storage_type="memory"
                ),
                html.Div(
                    id=self.ids.no_op(aio_id), style={"display": "hidden"}
                ),
            ],
            id=self.ids.modal_container(aio_id),
            className="modal",
        )

    @callback(
        Output(ids.new_screen_name(MATCH), "valid"),
        Input(ids.new_screen_name(MATCH), "value"),
    )
    def validate_screen_name(name: str):
        if name is None:
            return True
        else:
            pattern = r"^[A-Za-z0-9-]+$"
            match = re.match(pattern, name)
            if match is None:
                return False
            else:
                return re.match(pattern, name).string == name

    @callback(
        Output(ids.confirm_save_screen_btn(MATCH), "disabled"),
        Input(ids.new_screen_name(MATCH), "valid"),
    )
    def validate_screen_name(valid):
        return not valid

    @callback(
        Output(ids.screen_type_str(MATCH), "data"),
        Input("page-location", "pathname"),
    )
    def update_screen_type_str(path):
        return db.find_screen_type_in_url(path)

    @callback(
        Output(ids.no_op(MATCH), "children"),
        Input(ids.confirm_save_screen_btn(MATCH), "n_clicks"),
        State(ids.new_screen_name(MATCH), "value"),
        State(ids.screen_type_str(MATCH), "data"),
        State(ids.current_studies(MATCH), "data"),
    )
    def add_screen_to_db(
        n_clicks, screen_name, screen_type_str, current_studies
    ):
        if n_clicks is not None:
            if current_studies is not None:
                return db.create_or_update_screen(
                    screen_name, screen_type_str, current_studies
                )
        return None
