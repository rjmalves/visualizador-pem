from dash import Output, Input, html, dcc, callback, MATCH
from src.components.casos.spatialviewfilters import SpatialViewFilters
import src.utils.spatialplots as plots
import uuid
import plotly.graph_objects as go


class SpatialViewGraph(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "SpatialViewGraph",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        graph = lambda aio_id: {
            "component": "SpatialViewGraph",
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
                            "OPERAÇÃO DO ESTÁGIO",
                            className="card-title",
                        ),
                        html.Div(
                            dcc.Loading(
                                id="loading-spatialview-casos",
                                children=[
                                    SpatialViewFilters(aio_id=aio_id),
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
                        id="loading-spatialview-graph",
                        children=dcc.Graph(
                            id=self.ids.graph(aio_id),
                            config={
                                "displayModeBar": False,
                                "scrollZoom": False,
                            },
                            style={"height": "640px"},
                        ),
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
        Output(SpatialViewFilters.ids.studies(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_current_studies_main(studies_data):
        return studies_data

    @callback(
        Output(ids.graph(MATCH), "figure"),
        Input(SpatialViewFilters.ids.data(MATCH), "data"),
        prevent_initial_call=True,
    )
    def generate_spatialview_graph(spatialview_data):
        return plots.view_SBM_EST(spatialview_data)
