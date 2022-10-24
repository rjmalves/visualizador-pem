from dash import html

navbar = html.Header(
    [
        html.Div(
            [
                html.H1(
                    "VISUALIZADOR DE MODELOS ENERGÉTICOS",
                    className="header__title",
                ),
                html.H2(
                    "GERÊNCIA DE METODOLOGIAS E MODELOS ENERGÉTICOS",
                    className="header__subtitle",
                ),
            ],
        ),
        html.Div(
            [
                html.Img(src="assets/link.jpg", className="logo"),
                html.Nav(
                    html.Ul(
                        [
                            # html.Li(
                            #     html.A(
                            #         "CASOS",
                            #         href="/",
                            #     )
                            # ),
                            html.Li(
                                html.A(
                                    "ENCADEADOR",
                                    href="/",
                                )
                            ),
                            # html.Li(
                            #     html.A(
                            #         "PPQ",
                            #         href="/",
                            #     )
                            # ),
                        ],
                        className="navbar__links",
                    ),
                ),
                html.A(html.Button("Login"), href="/", className="login"),
            ],
            className="navbar",
        ),
    ],
)
