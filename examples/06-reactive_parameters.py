import pandas as pd
import panel as pn
import numpy as np

pn.extension()

data_url = "https://assets.holoviz.org/panel/tutorials/turbines.csv.gz"
df = pn.cache(pd.read_csv)(data_url)

dfrx = pn.rx(df)

cols = pn.widgets.MultiChoice(
    options=df.columns.to_list(),
    value=["p_name", "t_state", "t_county", "p_year", "p_cap"],
    height=300,
)
nrows = pn.widgets.IntSlider(start=5, end=20, step=5, value=15, name="Samples")
style = pn.rx("color: white; background-color: {color}")
color = pn.widgets.ColorPicker(value="darkblue", name="Highlight color")


def highlight_max(s, props=""):
    if s.dtype.kind not in "f":
        return np.full_like(s, False)
    return np.where(s == np.nanmax(s.values), props, "")


styled_df = (
    dfrx[cols]
    .sample(nrows)
    .style.apply(highlight_max, props=style.format(color=color), axis=0)
)

pn.panel(styled_df).servable()
