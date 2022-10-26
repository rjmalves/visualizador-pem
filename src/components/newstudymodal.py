from dash import html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc


modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle(
                        "ADICIONE UM NOVO ESTUDO",
                        className="new-study-form-title",
                    )
                ),
                dbc.ModalBody(
                    [
                        dcc.Input(
                            placeholder="Insira o ID do estudo a ser visualizado...",
                            id="new-study",
                            className="new-study-id-form-field",
                        )
                    ]
                ),
                dbc.ModalFooter(
                    html.Button(
                        "Adicionar",
                        id="confirm-study-button",
                        className="confirm-study-button",
                    )
                ),
            ],
            id="modal",
            is_open=False,
            backdrop=True,
            keyboard=True,
            centered=True,
            size="lg",
            fade=True,
        ),
    ],
    id="modal__container",
    className="modal",
)


@callback(
    Output("modal", "is_open"),
    [
        Input("add-study-button", "n_clicks"),
        Input("confirm-study-button", "n_clicks"),
    ],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
