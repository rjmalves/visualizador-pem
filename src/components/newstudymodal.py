from dash import html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc


modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle(
                        "ADICIONE UM NOVO ESTUDO",
                        className="new__study__form__title",
                    )
                ),
                dbc.ModalBody(
                    [
                        dcc.Input(
                            placeholder="Insira o ID do estudo a ser visualizado...",
                            id="new__study__id",
                            className="new__study__id__form__field",
                        )
                    ]
                ),
                dbc.ModalFooter(
                    html.Button(
                        "Adicionar",
                        id="confirm__study__button",
                        className="confirm__study__button",
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
        Input("add__study__button", "n_clicks"),
        Input("confirm__study__button", "n_clicks"),
    ],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
