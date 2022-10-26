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
                                    href="/",
                                )
                            ),
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
                        className="navbar-links",
                    ),
                ),
                html.A(html.Button("Login"), href="/", className="login"),
            ],
            className="navbar",
        ),
    ],
)
