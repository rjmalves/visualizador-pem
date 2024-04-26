import pandas as pd
import panel as pn
import param
from panel.widgets import IntSlider, Tabulator

pn.extension("tabulator")


class DataExplorer(pn.viewable.Viewer):

    data = param.DataFrame(doc="Stores a DataFrame to explore")
    page_size = param.Integer(
        default=10, doc="Number of rows per page.", bounds=(1, None)
    )
    theme = param.Selector(
        default="simple",
        objects=["simple", "default", "site", "midnight"],
    )
    show_index = param.Boolean(
        default=True, doc="Whether or not to display the index of the data"
    )

    def __panel__(self):
        return pn.Column(
            IntSlider.from_param(
                self.param.page_size, start=5, end=25, step=5
            ),
            self.param.theme,
            self.param.show_index,
            Tabulator.from_param(
                self.param.data,
                page_size=self.param.page_size,
                sizing_mode="stretch_width",
                theme=self.param.theme,
                show_index=self.param.show_index,
            ),
        )


data_url = "https://assets.holoviz.org/panel/tutorials/turbines.csv.gz"
df = pn.cache(pd.read_csv)(data_url)

DataExplorer(data=df).servable()
