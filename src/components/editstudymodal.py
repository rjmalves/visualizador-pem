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
import dash_bootstrap_components as dbc
import pandas as pd
import uuid


class EditStudyModal(html.Div):
    class ids:
        new_study_name = lambda aio_id: {
            "component": "EditStudyModal",
            "subcomponent": "new_study_name",
            "aio_id": aio_id,
        }
        confirm_study_btn = lambda aio_id: {
            "component": "EditStudyModal",
            "subcomponent": "confirm_study_btn",
            "aio_id": aio_id,
        }
        modal = lambda aio_id: {
            "component": "EditStudyModal",
            "subcomponent": "modal",
            "aio_id": aio_id,
        }
        modal_container = lambda aio_id: {
            "component": "EditStudyModal",
            "subcomponent": "modal_container",
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
                        dbc.ModalHeader(
                            dbc.ModalTitle(
                                "EDITE UM ESTUDO EXISTENTE",
                                className="card-title",
                            )
                        ),
                        dbc.ModalBody(
                            [
                                dcc.Input(
                                    placeholder="Insira o ID do estudo a ser visualizado...",
                                    id=self.ids.new_study_name(aio_id),
                                    className="modal-input-field",
                                    type="text",
                                )
                            ]
                        ),
                        dbc.ModalFooter(
                            html.Button(
                                "Confirmar",
                                id=self.ids.confirm_study_btn(aio_id),
                                className="modal-button",
                            )
                        ),
                    ],
                    id=self.ids.modal(aio_id),
                    is_open=False,
                    backdrop=True,
                    keyboard=True,
                    centered=True,
                    size="lg",
                    fade=True,
                ),
            ],
            id=self.ids.modal_container(aio_id),
            className="modal",
        )
