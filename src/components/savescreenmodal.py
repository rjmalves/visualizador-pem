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
            "subcomponent": "modal_container",
            "aio_id": aio_id,
        }
        current_studies = lambda aio_id: {
            "component": "SaveScreenModal",
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
                                            placeholder="Insira o caminho. Deve ser um caminho absoluto UNIX válido (/home/...)",
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
            ],
            id=self.ids.modal_container(aio_id),
            className="modal",
        )

    @callback(
        Output(ids.new_screen_name(MATCH), "valid"),
        Input(ids.new_screen_name(MATCH), "value"),
    )
    def validate_screen_name(name: str):
        pattern = r"[A-Za-z0-9-]+"
        return re.search(name, pattern) is not None

    @callback(
        Output(ids.screen_type_str(MATCH), "data"),
        Input("url-login", "pathname"),
    )
    def update_screen_type_str(path):
        return db.find_screen_type_in_url(path)


# TODO
# 1 - implementar a função que salva os casos atuais,
# criando todos os objetos no db (redirecionar para o link em seguida)
# 2 - adicionar suporte para, caso o nome de tela
# já existe, atualizar o conteúdo desta (apagar e recriar tudo)
# 3 - implementar a lógica de, partindo do url atual,
# popular corretamente a tabela de casos (buscar do DB)
