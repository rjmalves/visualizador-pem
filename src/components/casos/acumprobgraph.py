from dash import Output, Input, State, html, dcc, callback, MATCH
from src.components.casos.acumprobfilters import AcumProbFilters
import src.utils.plots as plots
import uuid


class AcumProbGraph(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "AcumProbGraph",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        graph = lambda aio_id: {
            "component": "AcumProbGraph",
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
                            "PERMANÊNCIA",
                            className="card-title",
                        ),
                        html.Div(
                            dcc.Loading(
                                id="loading-acumprob-casos",
                                children=AcumProbFilters(aio_id=aio_id),
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
                        id="loading-acumprob-graph",
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
        Output(AcumProbFilters.ids.studies(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_current_studies_main(studies_data):
        return studies_data

    @callback(
        Output(ids.graph(MATCH), "figure"),
        Input(AcumProbFilters.ids.data(MATCH), "data"),
        State(
            AcumProbFilters.ids.variable_dropdown(MATCH),
            "value",
        ),
        State(AcumProbFilters.ids.filters(MATCH), "data"),
        State(ids.studies(MATCH), "data"),
    )
    def generate_operation_graph(
        operation_data,
        variable,
        filters,
        studies,
    ):
        return plots.generate_acumprob_graph_casos(
            operation_data, variable, filters, studies
        )
