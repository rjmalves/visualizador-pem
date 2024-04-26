import panel as pn

pn.extension()

image = pn.pane.PNG(
    "https://assets.holoviz.org/panel/tutorials/wind_turbine.png",
    height=150,
    sizing_mode="scale_width",
)

card1 = pn.Card(image, title="Turbine 1", width=200)
card2 = pn.Card(image, title="Turbine 2", width=200)

pn.Column(
    card1,
    card2,
    sizing_mode="fixed",
    width=400,
    height=400,
    styles={"border": "1px solid black"},
).servable()
