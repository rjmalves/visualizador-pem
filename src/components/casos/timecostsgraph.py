from dash import Output, Input, State, html, dcc, callback, MATCH
from src.components.casos.timecostsfilters import TimeCostsFilters
import src.utils.plots as plots
import uuid


class TimeCostsGraph(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "TimeCostsGraph",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        graph = lambda aio_id: {
            "component": "TimeCostsGraph",
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
                            "CUSTOS e TEMPO DE EXECUÇÃO",
                            className="card-title",
                        ),
                        html.Div(
                            dcc.Loading(
                                id="loading-timecosts-casos",
                                children=TimeCostsFilters(aio_id=aio_id),
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
                        id="loading-timecosts-graph",
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
        Output(TimeCostsFilters.ids.studies(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_current_studies_main(studies_data):
        return studies_data

    @callback(
        Output(ids.graph(MATCH), "figure"),
        Input(TimeCostsFilters.ids.data(MATCH), "data"),
        State(
            TimeCostsFilters.ids.variable_dropdown(MATCH),
            "value",
        ),
        State(ids.studies(MATCH), "data"),
    )
    def generate_tempo_custos_graph(timecosts_data, variable, studies):
        return plots.generate_timecosts_graph_casos(
            timecosts_data, variable, studies
        )
