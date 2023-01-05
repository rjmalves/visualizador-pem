from dash import Output, Input, State, html, dcc, callback, MATCH
from src.components.encadeador.operationfiltersencadeador import (
    OperationFiltersEncadeador,
)
import src.utils.plots as plots
from src.utils.settings import Settings
import uuid


class OperationGraphEncadeador(html.Div):
    class ids:
        filters = lambda aio_id: {
            "component": "OperationGraphEncadeador",
            "subcomponent": "filters",
            "aio_id": aio_id,
        }
        studies = lambda aio_id: {
            "component": "OperationGraphEncadeador",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        graph = lambda aio_id: {
            "component": "OperationGraphEncadeador",
            "subcomponent": "graph",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        aio_id=None,
    ):

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        super().__init__(
            [
                html.Div(
                    [
                        html.H4(
                            "VARIÁVEIS DA OPERAÇÂO",
                            className="card-title",
                        ),
                        html.Div(
                            OperationFiltersEncadeador(aio_id=aio_id),
                            className="card-menu",
                        ),
                    ],
                    className="card-header",
                ),
                html.Div(
                    dcc.Graph(id=self.ids.graph(aio_id)),
                    className="card-content",
                ),
                dcc.Store(
                    id=self.ids.studies(aio_id),
                    storage_type="memory",
                ),
            ],
            className="card",
        )

    @callback(
        Output(OperationFiltersEncadeador.ids.studies(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_current_studies(studies_data):
        return studies_data

    @callback(
        Output(ids.graph(MATCH), "figure"),
        Input(OperationFiltersEncadeador.ids.data(MATCH), "data"),
        State(
            OperationFiltersEncadeador.ids.variable_dropdown(MATCH),
            "value",
        ),
        State(OperationFiltersEncadeador.ids.filters(MATCH), "data"),
    )
    def generate_operation_graph(operation_data, variable, filters):
        return plots.generate_operation_graph_encadeador(
            operation_data, variable, filters
        )
