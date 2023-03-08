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
from datetime import datetime, timedelta
from src.utils.api import API


class NewStudyModal(html.Div):
    class ids:
        new_study_name = lambda aio_id: {
            "component": "NewStudyModal",
            "subcomponent": "new_study_name",
            "aio_id": aio_id,
        }
        new_study_label = lambda aio_id: {
            "component": "NewStudyModal",
            "subcomponent": "new_study_label",
            "aio_id": aio_id,
        }
        new_study_color = lambda aio_id: {
            "component": "NewStudyModal",
            "subcomponent": "new_study_color",
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
        path_validation_timer = lambda aio_id: {
            "component": "NewStudyModal",
            "subcomponent": "path_validation_timer",
            "aio_id": aio_id,
        }
        path_validation_interval = lambda aio_id: {
            "component": "NewStudyModal",
            "subcomponent": "path_validation_interval",
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
                                        dbc.Label(
                                            "Caminho",
                                            className="modal-form-comment",
                                        ),
                                        dbc.Input(
                                            placeholder="Insira o caminho. Deve ser um caminho absoluto UNIX válido (/home/...)",
                                            id=self.ids.new_study_name(aio_id),
                                            className="modal-input-field",
                                            type="text",
                                        ),
                                        dbc.Label(
                                            "Nome",
                                            className="modal-form-comment",
                                        ),
                                        dbc.Input(
                                            placeholder="Insira um nome... (opcional, o default é o nome do diretório mais interno)",
                                            id=self.ids.new_study_label(
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
                                            id=self.ids.new_study_color(
                                                aio_id
                                            ),
                                            className="modal-input-field",
                                            value="#ffffff",
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
                dcc.Store(
                    id=self.ids.path_validation_timer(aio_id),
                    data=datetime.now().isoformat(),
                ),
                dcc.Interval(
                    id=self.ids.path_validation_interval(aio_id),
                    interval=500,
                    n_intervals=0,
                ),
            ],
            id=self.ids.modal_container(aio_id),
            className="modal",
        )

    @callback(
        Output(ids.path_validation_timer(MATCH), "data"),
        Output(ids.new_study_name(MATCH), "valid"),
        Input(ids.new_study_name(MATCH), "value"),
        Input(ids.path_validation_interval(MATCH), "n_intervals"),
        State(ids.path_validation_timer(MATCH), "data"),
        State(ids.new_study_name(MATCH), "valid"),
        State(ids.modal(MATCH), "is_open"),
        prevent_initial_call=True,
    )
    def update_validation_timer(
        path: str,
        intervals: bool,
        last_update_time: str,
        valid_input: bool,
        is_open: bool,
    ):
        if (
            ctx.triggered_id["subcomponent"]
            == NewStudyModal.ids.new_study_name(MATCH)["subcomponent"]
        ):
            return [datetime.now().isoformat(), False]
        else:
            if is_open:
                # Make a request do the options route and check validity
                time_since_last_change = (
                    datetime.now() - datetime.fromisoformat(last_update_time)
                )
                if (path is not None) and (
                    time_since_last_change > timedelta(seconds=1)
                ):
                    results = API.fetch_available_results(path)
                    return [
                        datetime.now().isoformat(),
                        results is not None,
                    ]
                else:
                    return [last_update_time, valid_input]
            else:
                return [last_update_time, valid_input]

    @callback(
        Output(ids.new_study_name(MATCH), "style"),
        Input(ids.new_study_name(MATCH), "valid"),
    )
    def update_field_style(valid):
        color = (
            "var(--valid-form-field)" if valid else "var(--invalid-form-field)"
        )
        return {"background-color": color}

    @callback(
        Output(ids.confirm_study_btn(MATCH), "disabled"),
        Input(ids.new_study_name(MATCH), "valid"),
    )
    def disable_confirm_btn(valid):
        return not valid
