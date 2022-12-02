from dash import Output, Input, State, html, dcc, callback, MATCH, ALL
from src.components.casos.resourcesfilters import ResourcesFilters
import src.utils.plots as plots
from src.utils.settings import Settings
import uuid


class ResourcesGraph(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "ResourcesGraph",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        graph = lambda aio_id: {
            "component": "ResourcesGraph",
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
                            "RECURSOS COMPUTACIONAIS",
                            className="card-title",
                        ),
                        html.Div(
                            [
                                ResourcesFilters(aio_id=aio_id),
                            ],
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
                    storage_type=Settings.storage,
                ),
            ],
            className="card",
        )

    @callback(
        Output(ResourcesFilters.ids.studies(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_current_studies_main(studies_data):
        return studies_data

    @callback(
        Output(ids.graph(MATCH), "figure"),
        Input(ResourcesFilters.ids.clusterData(MATCH), "data"),
        Input(ResourcesFilters.ids.jobData(MATCH), "data"),
        Input(ResourcesFilters.ids.timeData(MATCH), "data"),
        Input(ResourcesFilters.ids.convergenceData(MATCH), "data"),
        Input(
            ResourcesFilters.ids.studies_dropdown(MATCH),
            "value",
        ),
    )
    def generate_operation_graph(
        clusterData,
        jobData,
        timeData,
        convergenceData,
        study,
    ):
        return plots.generate_resources_graph_casos(
            clusterData,
            jobData,
            timeData,
            convergenceData,
            study,
        )
