from dash import html

footer = html.Footer(
    html.Div(
        [
            html.Hr(className="divider"),
            html.Div(
                "DPL/PE/PEM",
                className="rights",
            ),
        ],
        className="footer__container",
    )
)
