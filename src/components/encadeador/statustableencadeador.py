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
import src.utils.data as data
from src.utils.settings import Settings


STATUS_TABLE_COLUMNS = [
    "NOME",
    "TEMPO DE EXECUCAO",
    "PROGRESSO (%)",
    "CASO ATUAL",
    "ESTADO",
]


class StatusTable(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "StatusTable",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        table = lambda aio_id: {
            "component": "StatusTable",
            "subcomponent": "table",
            "aio_id": aio_id,
        }
        data = lambda aio_id: {
            "component": "StatusTable",
            "subcomponent": "data",
            "aio_id": aio_id,
        }
        selected = lambda aio_id: {
            "component": "StatusTable",
            "subcomponent": "selected",
            "aio_id": aio_id,
        }
        updater = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "updater",
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
                        html.H4("ANDAMENTO", className="card-title"),
                        html.Div(
                            [],
                            className="card-menu",
                        ),
                    ],
                    className="card-header",
                ),
                html.Div(
                    dcc.Loading(
                        id="loading-statustable-encadeador",
                        children=dash_table.DataTable(
                            data=pd.DataFrame(
                                columns=STATUS_TABLE_COLUMNS
                            ).to_dict("records"),
                            columns=[
                                {"id": c, "name": c}
                                for c in STATUS_TABLE_COLUMNS
                            ],
                            cell_selectable=False,
                            row_selectable=False,
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
                        type="default",
                        className="loading-spinner",
                        color="rgba(204,213,207,1)",
                    ),
                    className="card-content",
                ),
                dcc.Store(
                    id=self.ids.data(aio_id),
                    data=None,
                    storage_type="memory",
                ),
                dcc.Store(
                    id=self.ids.studies(aio_id),
                    storage_type="memory",
                ),
                dcc.Interval(
                    id=self.ids.updater(aio_id),
                    interval=int(Settings.current_state_update_period),
                    n_intervals=0,
                ),
            ],
            className="card",
        )

    @callback(
        Output(ids.data(MATCH), "data"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_data(interval, studies):
        return data.update_status_data_encadeador(interval, studies)

    @callback(
        Output(ids.table(MATCH), "data"),
        Input(ids.data(MATCH), "data"),
    )
    def generate_status_table(status_data):
        return pd.read_json(status_data, orient="split").to_dict("records")
