from dash import Output, Input, State, html, dcc, callback, MATCH, ALL
from src.components.casos.operationfilters import OperationFilters
from src.components.casos.operationfilterstwin import OperationFiltersTwin
import src.utils.plots as plots
from src.utils.settings import Settings
import uuid


class OperationGraph(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "OperationGraph",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        graph = lambda aio_id: {
            "component": "OperationGraph",
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
                            "EVOLUÇÂO TEMPORAL",
                            className="card-title",
                        ),
                        html.Div(
                            dcc.Loading(
                                id="loading-operation-casos",
                                children=[
                                    OperationFilters(aio_id=aio_id),
                                    OperationFiltersTwin(aio_id=aio_id),
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
                        id="loading-operation-graph",
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
        Output(OperationFilters.ids.studies(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_current_studies_main(studies_data):
        return studies_data

    @callback(
        Output(OperationFiltersTwin.ids.studies(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_current_studies_twin(studies_data):
        return studies_data

    @callback(
        Output(ids.graph(MATCH), "figure"),
        Input(OperationFilters.ids.data(MATCH), "data"),
        Input(OperationFiltersTwin.ids.data(MATCH), "data"),
        State(
            OperationFilters.ids.variable_dropdown(MATCH),
            "value",
        ),
        State(OperationFilters.ids.filters(MATCH), "data"),
        State(
            OperationFiltersTwin.ids.variable_dropdown(MATCH),
            "value",
        ),
        State(OperationFiltersTwin.ids.filters(MATCH), "data"),
        State(ids.studies(MATCH), "data"),
    )
    def generate_operation_graph(
        operation_data,
        operation_data_twinx,
        variable,
        filters,
        variable_twinx,
        filters_twinx,
        studies,
    ):
        return plots.generate_operation_graph_casos_twinx(
            operation_data,
            variable,
            filters,
            operation_data_twinx,
            variable_twinx,
            filters_twinx,
            studies,
        )
