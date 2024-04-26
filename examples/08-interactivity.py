import panel as pn
import pandas as pd

pn.extension("tabulator")

data_url = "https://assets.holoviz.org/panel/tutorials/turbines.csv.gz"

turbines = pn.cache(pd.read_csv)(data_url)

cols = pn.widgets.MultiChoice(
    options=turbines.columns.to_list(),
    value=["p_name", "t_state", "t_county", "p_year", "t_manu", "p_cap"],
    width=500,
    height=100,
    name="Columns",
)

table = pn.widgets.Tabulator(
    turbines[cols.value], page_size=5, pagination="remote"
)


def update_data(event):
    table.value = turbines[event.new]


cols.param.watch(update_data, "value")

pn.Column(cols, table).servable()
