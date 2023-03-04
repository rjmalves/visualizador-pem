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
from src.utils import db


class LoadScreenModal(html.Div):
    class ids:
        load_screen_select = lambda aio_id: {
            "component": "LoadScreenModal",
            "subcomponent": "load_screen_select",
            "aio_id": aio_id,
        }
        confirm_load_screen_btn = lambda aio_id: {
            "component": "LoadScreenModal",
            "subcomponent": "confirm_load_screen_btn",
            "aio_id": aio_id,
        }
        modal = lambda aio_id: {
            "component": "LoadScreenModal",
            "subcomponent": "modal",
            "aio_id": aio_id,
        }
        modal_container = lambda aio_id: {
            "component": "LoadScreenModal",
            "subcomponent": "modal_container",
            "aio_id": aio_id,
        }
        screen_type_str = lambda aio_id: {
            "component": "LoadScreenModal",
            "subcomponent": "screen_type_str",
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
                                        "ESCOLHA UM CONJUNTO DE ESTUDOS",
                                        className="card-title",
                                    )
                                ),
                                dbc.ModalBody(
                                    [
                                        dbc.Label(
                                            "Conjuntos de Estudos",
                                            className="modal-form-comment",
                                        ),
                                        dbc.Select(
                                            options=[],
                                            id=self.ids.load_screen_select(
                                                aio_id
                                            ),
                                            className="modal-input-field",
                                            style={
                                                "width": "100%",
                                                "padding": "12px 20px",
                                                "margin": "8px 0",
                                                "border": "8px solid var(--card-border-color)",
                                            },
                                        ),
                                    ]
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Confirmar",
                                        id=self.ids.confirm_load_screen_btn(
                                            aio_id
                                        ),
                                        className="modal-button",
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
            ],
            id=self.ids.modal_container(aio_id),
            className="modal",
        )

    @callback(
        Output(ids.screen_type_str(MATCH), "data"),
        Input("page-location", "pathname"),
    )
    def update_screen_type_str(path):
        return db.find_screen_type_in_url(path)
