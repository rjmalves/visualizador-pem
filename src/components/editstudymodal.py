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
import uuid


class EditStudyModal(html.Div):
    class ids:
        edit_study_id = lambda aio_id: {
            "component": "EditStudyModal",
            "subcomponent": "edit_study_id",
            "aio_id": aio_id,
        }
        edit_study_path = lambda aio_id: {
            "component": "EditStudyModal",
            "subcomponent": "edit_study_path",
            "aio_id": aio_id,
        }
        edit_study_name = lambda aio_id: {
            "component": "EditStudyModal",
            "subcomponent": "edit_study_name",
            "aio_id": aio_id,
        }
        edit_study_color = lambda aio_id: {
            "component": "EditStudyModal",
            "subcomponent": "edit_study_color",
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
                        dbc.Form(
                            [
                                dbc.ModalHeader(
                                    dbc.ModalTitle(
                                        "EDITANDO ESTUDO",
                                        className="card-title",
                                    )
                                ),
                                dbc.ModalBody(
                                    [
                                        dbc.Label(
                                            "Caminho",
                                            className="modal-form-comment",
                                        ),
                                        dbc.Input(
                                            placeholder="Insira o caminho. Deve ser um caminho absoluto UNIX válido (/home/...)",
                                            id=self.ids.edit_study_path(
                                                aio_id
                                            ),
                                            className="modal-input-field",
                                            type="text",
                                            readonly=True,
                                        ),
                                        dbc.Label(
                                            "Nome",
                                            className="modal-form-comment",
                                        ),
                                        dbc.Input(
                                            placeholder="Insira um nome... (opcional, o default é o nome do diretório mais interno)",
                                            id=self.ids.edit_study_name(
                                                aio_id
                                            ),
                                            className="modal-input-field",
                                            type="text",
                                        ),
                                        dbc.Label(
                                            "Cor",
                                            className="modal-form-comment",
                                        ),
                                        dbc.Input(
                                            type="color",
                                            id=self.ids.edit_study_color(
                                                aio_id
                                            ),
                                            className="modal-input-field",
                                        ),
                                        dcc.Store(
                                            id=self.ids.edit_study_id(aio_id),
                                            storage_type="memory",
                                        ),
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

    @callback(
        Output(ids.edit_study_path(MATCH), "readonly"),
        Input("url-login", "pathname"),
    )
    def update_allow_edit_path(path):
        if current_user.is_authenticated:
            return False
        else:
            return True
