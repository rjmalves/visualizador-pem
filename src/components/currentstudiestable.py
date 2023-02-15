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
import pandas as pd
import uuid
from src.utils.settings import Settings


df = pd.DataFrame(columns=["id", "CAMINHO", "NOME", "COR"])


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
                                        ),
                                        html.Button(
                                            "Editar",
                                            id=self.ids.edit_study_btn(aio_id),
                                        ),
                                        html.Button(
                                            "Remover",
                                            id=self.ids.remove_study_btn(
                                                aio_id
                                            ),
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
                        data=df.to_dict("records"),
                        columns=[{"id": c, "name": c} for c in df.columns],
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
                    data=df.to_json(orient="split"),
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
    )
    def update_current_studies_table(current_data):
        return pd.read_json(current_data, orient="split").to_dict("records")

    @callback(
        Output(ids.selected(MATCH), "data"),
        Input(ids.table(MATCH), "derived_virtual_selected_row_ids"),
    )
    def update_selected_study(sel_rows):
        return sel_rows

    @callback(
        Output(ids.table(MATCH), "style_data_conditional"),
        Input(ids.selected(MATCH), "data"),
    )
    def style_selected_rows(sel_rows):
        if sel_rows is None:
            return no_update
        val = [
            {
                "if": {"filter_query": "{{id}} ={}".format(i)},
                "backgroundColor": "#344e41",
                "color": "#dad7cd",
            }
            for i in sel_rows
        ]
        return val
