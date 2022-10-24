import pandas as pd
import dash
from dash import html, callback, Output, Input, State, dash_table, dcc, ctx
from src.utils.api import API

DUMMY_DATA = {
    "id": [1],
    "CAMINHO": [
        "/home/rogerio/git/visualizador-encadeador-pem/tests/2520",
    ],
}

df = pd.DataFrame(data=DUMMY_DATA)

current_studies = dcc.Store(
    id="current_studies", data=df.to_json(orient="split")
)
selected_study = dcc.Store(id="selected_study")

table = html.Div(
    html.Div(
        [
            html.Div(
                [
                    html.H4(
                        "ESTUDOS ATUAIS", className="table__header__title"
                    ),
                    html.Div(
                        [
                            html.Button("Adicionar", id="add__study__button"),
                            html.Button("Remover", id="remove__study__button"),
                        ],
                        className="table__editing__menu",
                    ),
                ],
                className="table__header",
            ),
            dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[{"id": c, "name": c} for c in df.columns],
                cell_selectable=False,
                row_selectable="single",
                id="current_studies_table",
                style_data={
                    "color": "black",
                    "backgroundColor": "rgba(218, 215, 205, 0.7)",
                    "fontWeight": "bolder",
                    "fontSize": "1rem",
                },
                style_data_conditional=[
                    {
                        "if": {"row_index": "odd"},
                        "backgroundColor": "rgb(220, 220, 220)",
                    }
                ],
                style_header={
                    "backgroundColor": "#a3b18a",
                    "color": "#dad7cd",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            ),
        ],
        className="table__container",
    ),
    className="card",
)


@callback(
    Output("current_studies_table", "data"),
    Input("current_studies", "data"),
)
def update_current_studies_table(current_data):
    return pd.read_json(current_data, orient="split").to_dict("records")


@callback(
    Output("selected_study", "data"),
    Input("current_studies_table", "derived_virtual_selected_row_ids"),
)
def update_selected_study(sel_rows):
    return sel_rows


@callback(
    Output("current_studies", "data"),
    Input("confirm__study__button", "n_clicks"),
    Input("remove__study__button", "n_clicks"),
    State("new__study__id", "value"),
    State("selected_study", "data"),
    State("current_studies", "data"),
)
def edit_current_study_data(
    add_study_button_clicks,
    remove_study_button_clicks,
    new_study_id,
    selected_study,
    current_studies,
):
    if ctx.triggered_id == "confirm__study__button":
        if add_study_button_clicks:
            if not new_study_id:
                return current_studies
            elif len(new_study_id) == 0:
                return current_studies
            current_data = pd.read_json(current_studies, orient="split")
            if new_study_id in current_data["CAMINHO"].tolist():
                return current_studies
            else:
                last_id = int(current_data["id"].to_list()[-1])
                new_data = pd.DataFrame(
                    data={
                        "id": [str(last_id + 1)],
                        "CAMINHO": [new_study_id],
                    }
                )
                return pd.concat(
                    [current_data, new_data], ignore_index=True
                ).to_json(orient="split")
        else:
            return current_studies
    elif ctx.triggered_id == "remove__study__button":
        if remove_study_button_clicks:
            current_data = pd.read_json(current_studies, orient="split")
            new_data = current_data.loc[
                ~current_data["id"].isin(selected_study)
            ]
            return new_data.to_json(orient="split")
        else:
            return current_studies
    else:
        return current_studies


@callback(
    Output("current_studies_table", "style_data_conditional"),
    Input("selected_study", "data"),
)
def style_selected_rows(sel_rows):
    if sel_rows is None:
        return dash.no_update
    val = [
        {
            "if": {"filter_query": "{{id}} ={}".format(i)},
            "backgroundColor": "#344e41",
            "color": "#dad7cd",
        }
        for i in sel_rows
    ]
    return val
