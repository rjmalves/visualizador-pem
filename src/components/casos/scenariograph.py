from dash import Output, Input, State, html, dcc, callback, MATCH
from src.components.casos.scenariofilters import ScenarioFilters
import src.utils.plots as plots
import uuid


class ScenarioGraph(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "ScenarioGraph",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        graph = lambda aio_id: {
            "component": "ScenarioGraph",
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
                            "CENÁRIOS",
                            className="card-title",
                        ),
                        html.Div(
                            dcc.Loading(
                                id="loading-scenario-casos",
                                children=[
                                    ScenarioFilters(aio_id=aio_id),
                                ],
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
                        id="loading-scenario-graph",
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
        Output(ScenarioFilters.ids.studies(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_current_studies_main(studies_data):
        return studies_data

    @callback(
        Output(ids.graph(MATCH), "figure"),
        Input(ScenarioFilters.ids.data(MATCH), "data"),
        State(
            ScenarioFilters.ids.variable_dropdown(MATCH),
            "value",
        ),
        State(ScenarioFilters.ids.filters(MATCH), "data"),
        State(ids.studies(MATCH), "data"),
    )
    def generate_scenario_graph(
        scenario_data,
        variable,
        filters,
        studies,
    ):
        return plots.generate_scenario_graph_casos(
            scenario_data,
            variable,
            filters,
            studies,
        )
