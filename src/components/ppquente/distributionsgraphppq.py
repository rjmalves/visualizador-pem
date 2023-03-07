from dash import Output, Input, State, html, dcc, callback, MATCH
from src.components.ppquente.distributionfiltersppq import (
    DistributionFiltersPPQ,
)
import src.utils.plots as plots
from src.utils.settings import Settings
import uuid


class DistributionsGraphPPQ(html.Div):
    class ids:
        filters = lambda aio_id: {
            "component": "DistributionsGraphPPQ",
            "subcomponent": "filters",
            "aio_id": aio_id,
        }
        studies = lambda aio_id: {
            "component": "DistributionsGraphPPQ",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        graph = lambda aio_id: {
            "component": "DistributionsGraphPPQ",
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
                            "ESTABILIDADE DAS VARIÁVEIS",
                            className="card-title",
                        ),
                        html.Div(
                            dcc.Loading(
                                id="loading-operation-ppq",
                                children=DistributionFiltersPPQ(aio_id=aio_id),
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
        Output(DistributionFiltersPPQ.ids.studies(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_current_studies(studies_data):
        return studies_data

    @callback(
        Output(ids.graph(MATCH), "figure"),
        Input(DistributionFiltersPPQ.ids.data(MATCH), "data"),
        State(
            DistributionFiltersPPQ.ids.variable_dropdown(MATCH),
            "value",
        ),
        State(DistributionFiltersPPQ.ids.filters(MATCH), "data"),
        State(ids.studies(MATCH), "data"),
    )
    def generate_distribution_graph(
        operation_data, variable, filters, studies
    ):
        return plots.generate_distribution_graph_ppq(
            operation_data, variable, filters, studies
        )

    @callback(
        Output(
            DistributionFiltersPPQ.ids.estagio_dropdown_container(MATCH),
            "style",
        ),
        Input(DistributionFiltersPPQ.ids.data(MATCH), "data"),
    )
    def show_estagio_dropdown(variable):
        return {"display": "flex"}
