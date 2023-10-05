from dash import (
    Output,
    Input,
    State,
    html,
    dcc,
    callback,
    MATCH,
    dash_table,
)
from dash.exceptions import PreventUpdate
import pandas as pd
import uuid
from src.utils.settings import Settings
from flask_login import current_user

data_df = pd.DataFrame(
    columns=[
        "study_id",
        "table_id",
        "path",
        "name",
        "color",
        "created_date",
        "options",
        "program",
    ]
)
table_df = pd.DataFrame(columns=["id", "PROGRAMA", "CAMINHO", "NOME", "COR"])


class CurrentStudiesTable(html.Div):
    class ids:
        add_study_btn = lambda aio_id: {
            "component": "CurrentStudiesTable",
            "subcomponent": "add_study_btn",
            "aio_id": aio_id,
        }
        edit_study_btn = lambda aio_id: {
            "component": "CurrentStudiesTable",
            "subcomponent": "edit_study_btn",
            "aio_id": aio_id,
        }
        remove_study_btn = lambda aio_id: {
            "component": "CurrentStudiesTable",
            "subcomponent": "remove_study_btn",
            "aio_id": aio_id,
        }
        save_study_btn = lambda aio_id: {
            "component": "CurrentStudiesTable",
            "subcomponent": "save_study_btn",
            "aio_id": aio_id,
        }
        load_study_btn = lambda aio_id: {
            "component": "CurrentStudiesTable",
            "subcomponent": "load_study_btn",
            "aio_id": aio_id,
        }
        button_type_div = lambda aio_id: {
            "component": "CurrentStudiesTable",
            "subcomponent": "button_type_div",
            "aio_id": aio_id,
        }
        table = lambda aio_id: {
            "component": "CurrentStudiesTable",
            "subcomponent": "table",
            "aio_id": aio_id,
        }
        data = lambda aio_id: {
            "component": "CurrentStudiesTable",
            "subcomponent": "data",
            "aio_id": aio_id,
        }
        selected = lambda aio_id: {
            "component": "CurrentStudiesTable",
            "subcomponent": "selected",
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
                html.Div(
                    [
                        html.H4("ESTUDOS ATUAIS", className="card-title"),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Button(
                                            "Adicionar",
                                            id=self.ids.add_study_btn(aio_id),
                                            style={"display": "none"},
                                        ),
                                        html.Button(
                                            "Editar",
                                            id=self.ids.edit_study_btn(aio_id),
                                            disabled=True,
                                        ),
                                        html.Button(
                                            "Remover",
                                            id=self.ids.remove_study_btn(
                                                aio_id
                                            ),
                                            style={"display": "none"},
                                            disabled=True,
                                        ),
                                        html.Div(
                                            id=self.ids.button_type_div(
                                                aio_id
                                            ),
                                            style={
                                                "border-right": "6px solid #a3b18a",
                                                "height": "auto",
                                                "border-radius": "4px",
                                                "margin-left": "10px",
                                                "display": "none",
                                            },
                                        ),
                                        html.Button(
                                            "Salvar",
                                            id=self.ids.save_study_btn(aio_id),
                                            style={"display": "none"},
                                        ),
                                        html.Button(
                                            "Carregar",
                                            id=self.ids.load_study_btn(aio_id),
                                            style={"display": "none"},
                                        ),
                                    ],
                                    className="card-menu-row",
                                ),
                            ],
                            className="card-menu",
                        ),
                    ],
                    className="card-header",
                ),
                html.Div(
                    # TODO - remove styling from here
                    dash_table.DataTable(
                        data=table_df.to_dict("records"),
                        columns=[
                            {"id": c, "name": c} for c in table_df.columns
                        ],
                        cell_selectable=False,
                        row_selectable="single",
                        id=self.ids.table(aio_id),
                        style_data={
                            "color": "black",
                            "backgroundColor": "rgba(218, 215, 205, 0.7)",
                            "fontWeight": "bolder",
                            "fontSize": "1rem",
                        },
                        style_data_conditional=[
                            {
                                "if": {"row_index": "odd"},
                                "backgroundColor": "rgb(220, 220, 220)",
                            }
                        ],
                        style_header={
                            "backgroundColor": "#a3b18a",
                            "color": "#dad7cd",
                            "fontWeight": "bold",
                            "textAlign": "center",
                        },
                    ),
                    className="card-content",
                ),
                dcc.Store(
                    id=self.ids.data(aio_id),
                    data=data_df.to_json(orient="split"),
                    storage_type=Settings.storage,
                ),
                dcc.Store(
                    id=self.ids.selected(aio_id), storage_type=Settings.storage
                ),
            ],
            className="card",
        )

    @callback(
        Output(ids.table(MATCH), "data"),
        Input(ids.data(MATCH), "data"),
        prevent_initial_callback=True,
    )
    def update_current_studies_table(current_data):
        # Atribui renomeando as colunas e filtrando as informações
        all_data = pd.read_json(current_data, orient="split")
        renamed_data = all_data.rename(
            columns={
                "table_id": "id",
                "path": "CAMINHO",
                "name": "NOME",
                "color": "COR",
                "program": "PROGRAMA",
            }
        )
        return renamed_data[
            ["id", "PROGRAMA", "CAMINHO", "NOME", "COR"]
        ].to_dict("records")

    @callback(
        Output(ids.selected(MATCH), "data"),
        Input(ids.table(MATCH), "derived_virtual_selected_row_ids"),
        prevent_initial_callback=True,
    )
    def update_selected_study(sel_rows):
        return sel_rows

    @callback(
        Output(ids.table(MATCH), "style_data_conditional"),
        Input(ids.selected(MATCH), "data"),
        prevent_initial_callback=True,
    )
    def style_selected_rows(sel_rows):
        if sel_rows is None:
            raise PreventUpdate
        val = [
            {
                "if": {"filter_query": "{{id}} ={}".format(i)},
                "backgroundColor": "#344e41",
                "color": "#dad7cd",
            }
            for i in sel_rows
        ]
        return val

    @callback(
        Output(ids.edit_study_btn(MATCH), "disabled"),
        Input(ids.selected(MATCH), "data"),
    )
    def disable_edit_btn(value):
        return value is None

    @callback(
        Output(ids.remove_study_btn(MATCH), "disabled"),
        Input(ids.selected(MATCH), "data"),
    )
    def disable_remove_btn(value):
        return value is None

    @callback(
        Output(ids.add_study_btn(MATCH), "style"),
        Input("page-location", "pathname"),
        State(ids.add_study_btn(MATCH), "style"),
    )
    def update_display_add_button(path, current_style):
        if current_user.is_authenticated:
            display = "flex"
        else:
            display = "none"
        return {**current_style, "display": display}

    @callback(
        Output(ids.remove_study_btn(MATCH), "style"),
        Input("page-location", "pathname"),
        State(ids.remove_study_btn(MATCH), "style"),
    )
    def update_display_remove_button(path, current_style):
        if current_user.is_authenticated:
            display = "flex"
        else:
            display = "none"
        return {**current_style, "display": display}

    @callback(
        Output(ids.save_study_btn(MATCH), "style"),
        Input("page-location", "pathname"),
        State(ids.save_study_btn(MATCH), "style"),
    )
    def update_display_save_button(path, current_style):
        if current_user.is_authenticated:
            display = "flex"
        else:
            display = "none"
        return {**current_style, "display": display}

    @callback(
        Output(ids.load_study_btn(MATCH), "style"),
        Input("page-location", "pathname"),
        State(ids.load_study_btn(MATCH), "style"),
    )
    def update_display_load_button(path, current_style):
        if current_user.is_authenticated:
            display = "flex"
        else:
            display = "none"
        return {**current_style, "display": display}

    @callback(
        Output(ids.button_type_div(MATCH), "style"),
        Input("page-location", "pathname"),
        State(ids.button_type_div(MATCH), "style"),
    )
    def update_display_button_type_div(path, current_style):
        if current_user.is_authenticated:
            display = "flex"
        else:
            display = "none"
        return {**current_style, "display": display}
