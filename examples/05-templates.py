import panel as pn
import pandas as pd
import altair as alt

pn.extension("vega")

ACCENT = "teal"

image = pn.pane.JPG(
    "https://assets.holoviz.org/panel/tutorials/wind_turbines_sunset.png"
)

if pn.config.theme == "dark":
    alt.themes.enable("dark")
else:
    alt.themes.enable("default")


@pn.cache  # Add caching to only download data once
def get_data():
    return pd.read_csv(
        "https://assets.holoviz.org/panel/tutorials/turbines.csv.gz"
    )


df = get_data()

top_manufacturers = (
    df.groupby("t_manu").p_cap.sum().sort_values().iloc[-10:].index.to_list()
)
df = df[df.t_manu.isin(top_manufacturers)]
fig = (
    alt.Chart(
        df.sample(5000),
        title="Capacity by Manufacturer",
    )
    .mark_circle(size=8)
    .encode(
        y="t_manu:N",
        x="p_cap:Q",
        yOffset="jitter:Q",
        color=alt.Color("t_manu:N").legend(None),
        tooltip=["t_manu", "p_cap"],
    )
    .transform_calculate(jitter="sqrt(-2*log(random()))*cos(2*PI*random())")
    .properties(
        height="container",
        width="container",
    )
)
plot = pn.pane.Vega(fig, sizing_mode="stretch_both", max_height=800, margin=20)

pn.template.FastListTemplate(
    title="Wind Turbine Manufacturers",
    sidebar=[
        image,
        "**Note**: Only the 10 Manufacturers with the largest installed capacity are shown in the plot.",
    ],
    main=["# Installed Capacity", plot],
    accent=ACCENT,
    main_layout=None,
).servable()
