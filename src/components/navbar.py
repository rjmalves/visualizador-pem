from dash import html

navbar = html.Header(
    [
        html.Div(
            [
                html.Img(src="assets/link.jpg", className="logo"),
                html.Nav(
                    html.Ul(
                        [
                            html.Li(
                                html.A(
                                    "CASOS",
                                    href="/casos",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "ENCADEADOR",
                                    href="/encadeador",
                                )
                            ),
                            # html.Li(
                            #     html.A(
                            #         "PPQ",
                            #         href="/",
                            #     )
                            # ),
                        ],
                        className="navbar-links",
                    ),
                ),
                html.A(html.Button("Login"), href="/login", className="login"),
            ],
            className="navbar",
        ),
    ],
)
