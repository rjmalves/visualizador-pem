from dash import Output, Input, State, html, dcc, callback, MATCH
from src.components.encadeador.violationfiltersencadeador import (
    ViolationFilters,
)
import src.utils.plots as plots
from src.utils.settings import Settings
import uuid


class ViolationGraph(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "ViolationGraph",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        graph = lambda aio_id: {
            "component": "ViolationGraph",
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
                            "INVIABILIDADES",
                            className="card-title",
                        ),
                        html.Div(
                            dcc.Loading(
                                id="loading-violation-encadeador",
                                children=ViolationFilters(aio_id=aio_id),
                                type="default",
                                className="loading-spinner",
                                color="rgba(204,213,207,1)",
                            ),
                            className="card-menu",
                        ),
                    ],
                    className="card-header",
                ),
                html.Div(
                    dcc.Loading(
                        id="loading-violations-graph-encadeador",
                        children=dcc.Graph(id=self.ids.graph(aio_id)),
                        type="default",
                        className="loading-spinner",
                        color="rgba(204,213,207,1)",
                    ),
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
        Output(ViolationFilters.ids.studies(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_current_studies_main(studies_data):
        return studies_data

    @callback(
        Output(ids.graph(MATCH), "figure"),
        Input(ViolationFilters.ids.data(MATCH), "data"),
        State(
            ViolationFilters.ids.violation_dropdown(MATCH),
            "value",
        ),
        State(
            ViolationFilters.ids.filters(MATCH),
            "data",
        ),
    )
    def generate_tempo_custos_graph(
        violation_data,
        violation,
        filters,
    ):
        return plots.generate_violation_graph_encadeador(
            violation_data, violation
        )
