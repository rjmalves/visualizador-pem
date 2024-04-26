import panel as pn
import numpy as np

pn.extension()

pn.indicators.Number(
    name="Wind Speed",
    value=8.6,
    format="{value} m/s",
    colors=[(10, "green"), (100, "red")],
).servable()


def get_wind_speeds(n):
    # Replace this with your own wind speed data source
    return {"x": np.arange(n), "y": 8 + np.random.randn(n)}


pn.indicators.Trend(
    name="Wind Speed (m/s, hourly avg.)",
    data=get_wind_speeds(24),
    width=500,
    height=500,
).servable()
