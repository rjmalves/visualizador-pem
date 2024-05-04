# TODO - bootstrap template

# Data source selection in sidebar

# Graph shown in main area

# Begin with only line graphs, add more types later
import param
import panel as pn
import pandas as pd
from panel.viewable import Viewer

CARD_STYLE = """
:host {{
  box-shadow: rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px;
  padding: {padding};
}} """

METADATA_URL = "./data/newave/sintese/METADADOS_OPERACAO.parquet"


@pn.cache(ttl=15 * 60)
def get_metadata():
    return pd.read_parquet(METADATA_URL)


class DataStore(Viewer):
    data = param.DataFrame()

    filters = param.List(constant=True)

    def __init__(self, **params):
        super().__init__(**params)
        dfx = self.param.data.rx()
        widgets = []
        for filt in self.filters:
            dtype = self.data.dtypes[filt]
            if dtype.kind == "f":
                widget = pn.widgets.RangeSlider(
                    name=filt, start=dfx[filt].min(), end=dfx[filt].max()
                )
                condition = dfx[filt].between(*widget.rx())
            else:
                options = dfx[filt].unique().tolist()
                widget = pn.widgets.MultiChoice(name=filt, options=options)
                condition = dfx[filt].isin(
                    widget.rx().rx.where(widget, options)
                )
            dfx = dfx[condition].copy()
            widgets.append(widget)
        self.filtered = dfx
        self.count = dfx.rx.len()
        self._widgets = widgets

    def filter(
        self,
    ):
        return

    def __panel__(self):
        return pn.Column(
            "## Filters",
            *self._widgets,
            stylesheets=[CARD_STYLE.format(padding="5px 10px")],
            margin=10
        )


class View(Viewer):
    data_store = param.ClassSelector(class_=DataStore)


class Table(View):
    columns = param.List(
        default=[
            "chave",
            "nome_longo_variavel",
            "nome_longo_agregacao",
            "unidade",
        ]
    )

    def __panel__(self):
        data = self.data_store.filtered[self.param.columns]
        return pn.widgets.Tabulator(
            data,
            pagination="remote",
            page_size=8,
            stylesheets=[CARD_STYLE.format(padding="10px")],
            margin=10,
            show_index=False,
        )


class App(Viewer):
    data_store = param.ClassSelector(class_=DataStore)

    title = param.String()

    views = param.List()

    def __init__(self, **params):
        super().__init__(**params)
        updating = self.data_store.filtered.rx.updating()
        updating.rx.watch(
            lambda updating: (
                pn.state.curdoc.hold()
                if updating
                else pn.state.curdoc.unhold()
            )
        )
        self._views = pn.FlexBox(
            *(view(data_store=self.data_store) for view in self.views),
            loading=updating
        )
        self._template = pn.template.BootstrapTemplate(title=self.title)
        self._template.sidebar.append(self.data_store)
        self._template.main.append(self._views)

    def servable(self):
        if pn.state.served:
            return self._template.servable()
        return self

    def __panel__(self):
        return pn.Row(self.data_store, self._views)


data = get_metadata()
ds = DataStore(
    data=data, filters=["nome_longo_variavel", "nome_longo_agregacao"]
)

App(data_store=ds, views=[Table], title="Metadata Explorer").servable()
