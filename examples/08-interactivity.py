import pandas as pd
import panel as pn
import param
from panel.viewable import Viewer

pn.extension("tabulator")

data_url = "https://assets.holoviz.org/panel/tutorials/turbines.csv.gz"

turbines = pn.cache(pd.read_csv)(data_url)


class DataExplorer(Viewer):
    data = param.DataFrame(doc="Stores a DataFrame to explore")

    columns = param.ListSelector(
        default=["p_name", "t_state", "t_county", "p_year", "t_manu", "p_cap"]
    )

    year = param.Range(default=(1981, 2022), bounds=(1981, 2022))

    capacity = param.Range(default=(0, 1100), bounds=(0, 1100))

    filtered_data = param.Parameter()

    number_of_rows = param.Parameter()

    def __init__(self, **params):
        super().__init__(**params)
        self.param.columns.objects = self.data.columns.to_list()

        dfrx = self.param.data.rx()

        p_year_min = self.param.year.rx().rx.pipe(lambda x: x[0])
        p_year_max = self.param.year.rx().rx.pipe(lambda x: x[1])
        p_cap_min = self.param.capacity.rx().rx.pipe(lambda x: x[0])
        p_cap_max = self.param.capacity.rx().rx.pipe(lambda x: x[1])

        self.filtered_data = dfrx[
            dfrx.p_year.between(p_year_min, p_year_max)
            & dfrx.p_cap.between(p_cap_min, p_cap_max)
        ][self.param.columns]

        self.number_of_rows = pn.rx("Rows: {len_df}").format(
            len_df=pn.rx(len)(dfrx)
        )

    def __panel__(self):
        return pn.Column(
            pn.Row(
                pn.widgets.MultiChoice.from_param(
                    self.param.columns, width=400
                ),
                pn.Column(self.param.year, self.param.capacity),
            ),
            self.number_of_rows,
            pn.widgets.Tabulator(
                self.filtered_data, page_size=10, pagination="remote"
            ),
        )


DataExplorer(data=turbines).servable()
