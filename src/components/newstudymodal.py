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


class NewStudyModal(html.Div):
    class ids:
        new_study_name = lambda aio_id: {
            "component": "NewStudyModal",
            "subcomponent": "new_study_name",
            "aio_id": aio_id,
        }
        confirm_study_btn = lambda aio_id: {
            "component": "NewStudyModal",
            "subcomponent": "confirm_study_btn",
            "aio_id": aio_id,
        }
        modal = lambda aio_id: {
            "component": "NewStudyModal",
            "subcomponent": "modal",
            "aio_id": aio_id,
        }
        modal_container = lambda aio_id: {
            "component": "NewStudyModal",
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
                        dbc.Form(
                            [
                                dbc.ModalHeader(
                                    dbc.ModalTitle(
                                        "ADICIONE UM NOVO ESTUDO",
                                        className="card-title",
                                    )
                                ),
                                dbc.ModalBody(
                                    [
                                        dbc.Input(
                                            placeholder="Insira o caminho...",
                                            id=self.ids.new_study_name(aio_id),
                                            className="modal-input-field",
                                            type="text",
                                        ),
                                        dbc.FormText(
                                            "Deve ser um caminho absoluto UNIX válido (/home/...)",
                                            className="modal-form-comment",
                                        ),
                                        # dbc.Input(
                                        #     type="color",
                                        #     id="modal-color-picker",
                                        #     value="#000000",
                                        # ),
                                    ]
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Confirmar",
                                        id=self.ids.confirm_study_btn(aio_id),
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
            ],
            id=self.ids.modal_container(aio_id),
            className="modal",
        )
