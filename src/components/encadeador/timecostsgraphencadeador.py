from dash import Output, Input, State, html, dcc, callback, MATCH
from src.components.encadeador.timecostsfiltersencadeador import (
    TimeCostsFiltersEncadeador,
)
import src.utils.plots as plots
import uuid


class TimeCostsGraphEncadeador(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "TimeCostsGraphEncadeador",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        graph = lambda aio_id: {
            "component": "TimeCostsGraphEncadeador",
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
                                id="loading-timecosts-encadeador",
                                children=TimeCostsFiltersEncadeador(
                                    aio_id=aio_id
                                ),
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
                        id="loading-timecosts-graph-encadeador",
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
        Output(TimeCostsFiltersEncadeador.ids.studies(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_current_studies_main(studies_data):
        return studies_data

    @callback(
        Output(ids.graph(MATCH), "figure"),
        Input(TimeCostsFiltersEncadeador.ids.data(MATCH), "data"),
        State(
            TimeCostsFiltersEncadeador.ids.variable_dropdown(MATCH),
            "value",
        ),
        State(
            TimeCostsFiltersEncadeador.ids.filters(MATCH),
            "data",
        ),
        State(ids.studies(MATCH), "data"),
    )
    def generate_tempo_custos_graph(
        timecosts_data, variable, filters, studies
    ):
        return plots.generate_timecosts_graph_encadeador(
            timecosts_data, variable, studies
        )
