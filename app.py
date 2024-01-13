import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import param

pn.extension(design="material")

csv_file = "https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv"
data = pd.read_csv(csv_file, parse_dates=["date"], index_col="date")


def view_hvplot(avg, highlight):
    return avg.hvplot(
        height=300, width=400, legend=False
    ) * highlight.hvplot.scatter(color="orange", padding=0.1, legend=False)


def find_outliers(
    variable="Temperature", window=30, sigma=10, view_fn=view_hvplot
):
    avg = data[variable].rolling(window=window).mean()
    residual = data[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = np.abs(residual) > std * sigma
    return view_fn(avg, avg[outliers])


class RoomOccupancy(param.Parameterized):
    variable = param.Selector(
        default="Temperature", objects=list(data.columns)
    )
    window = param.Integer(default=30, bounds=(1, 60))
    sigma = param.Number(default=10, bounds=(0, 20))

    def view(self):
        return find_outliers(
            self.variable, self.window, self.sigma, view_fn=view_hvplot
        )


obj = RoomOccupancy()

pn.Column(obj.param, obj.view).servable()
