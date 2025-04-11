from datetime import timedelta
from io import StringIO

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

from src.utils.constants import END_DATE_COLUMN, START_DATE_COLUMN
from src.utils.data import DISCRETE_COLOR_PALLETE
from src.utils.log import Log

pio.templates.default = "plotly_white"

DISCRETE_COLOR_PALLETE_COSTS = [
    "rgba(249, 65, 68, 1)",
    "rgba(87, 117, 144, 1)",
    "rgba(144, 190, 109, 1)",
    "rgba(243, 114, 44, 1)",
    "rgba(67, 170, 139, 1)",
    "rgba(39, 125, 161, 1)",
    "rgba(249, 132, 74, 1)",
    "rgba(77, 144, 142, 1)",
    "rgba(249, 199, 79, 1)",
    "rgba(248, 150, 30, 1)",
]


LINE_WIDTH = 2
YAXIS_TICKFORMAT = ",.2f"
X_TITLE_POS = 0.05
Y_TITLE_POS = 0.9

NOT_SCENARIO_COLUMNS = [
    "iteracao",
    "estudo",
    "caso",
    "estagio",
    "codigo_submercado",
    "codigo_submercado_de",
    "codigo_submercado_para",
    "codigo_ree",
    "codigo_usina",
    "limite_inferior",
    "limite_superior",
    "data_inicio",
    "data_fim",
    "unidade",
]


def _generate_yaxis_title(
    variable: str, filters: dict, studies: pd.DataFrame
) -> str:
    aggregation = filters["agregacao"]
    operation_options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["operacao"]), orient="split")
            for opt in studies["options"]
        ],
        ignore_index=True,
    )
    units = operation_options_df.loc[
        (operation_options_df["nome_longo_variavel"] == variable)
        & (operation_options_df["nome_longo_agregacao"] == aggregation),
        "unidade",
    ].tolist()
    units = list(set(units))
    axis_text = " | ".join(units)
    return axis_text


def pivot_df_for_plot(df: pd.DataFrame, col: str = "valor") -> pd.DataFrame:
    if "cenario" in df.columns:
        index_cols = [c for c in df.columns if c in NOT_SCENARIO_COLUMNS]
        df_plot = df.pivot(index=index_cols, columns="cenario", values=col)
        return df_plot.reset_index()
    else:
        return df.rename(columns={col: "mean"})


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def generate_operation_graph_casos(
    operation_data, variable, filters, studies_data
):
    fig = go.Figure()
    if operation_data is None:
        return fig
    Log.log().info(f"Plotando gráfico - CASOS ({variable})")
    dados = pd.read_json(StringIO(operation_data), orient="split")
    dados[START_DATE_COLUMN] = pd.to_datetime(
        dados[START_DATE_COLUMN], unit="ms"
    )
    dados[END_DATE_COLUMN] = pd.to_datetime(dados[END_DATE_COLUMN], unit="ms")
    studies_df = pd.read_json(StringIO(studies_data), orient="split")
    line_shape = "linear"
    mode = "lines"
    visibilidade_p = __background_area_visibility(studies_df["name"])
    for _, linha_df in studies_df.iterrows():
        estudo = linha_df["name"]
        rgb = hex_to_rgb(linha_df["color"])
        cor = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 1.0)"
        cor_fundo = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 0.3)"
        if dados is not None:
            dados_estudo = pivot_df_for_plot(
                dados.loc[dados["estudo"] == estudo]
            )
            if not dados_estudo.empty:
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo[START_DATE_COLUMN],
                        y=dados_estudo["mean"],
                        line={
                            "color": cor,
                            "width": LINE_WIDTH,
                            "shape": line_shape,
                        },
                        mode=mode,
                        name=estudo,
                        legendgroup="mean",
                        legendgrouptitle_text="mean",
                    )
                )
                if "p10" in dados_estudo.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=dados_estudo[START_DATE_COLUMN],
                            y=dados_estudo["p10"],
                            line_color=cor_fundo,
                            line_shape=line_shape,
                            mode=mode,
                            legendgroup="p10",
                            legendgrouptitle_text="p10",
                            name=estudo,
                            visible=visibilidade_p,
                        )
                    )
                if "p90" in dados_estudo.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=dados_estudo[START_DATE_COLUMN],
                            y=dados_estudo["p90"],
                            line_color=cor_fundo,
                            fillcolor=cor_fundo,
                            line_shape=line_shape,
                            mode=mode,
                            fill="tonexty",
                            legendgroup="p90",
                            legendgrouptitle_text="p90",
                            name=estudo,
                            visible=visibilidade_p,
                        )
                    )

    if variable is not None:
        fig.update_layout(
            title={
                "text": __make_operation_plot_title(
                    variable, filters, studies_df
                ),
                "x": X_TITLE_POS,
                "y": Y_TITLE_POS,
            },
            xaxis_title="Data",
            yaxis_title=_generate_yaxis_title(variable, filters, studies_df),
            yaxis_tickformat=YAXIS_TICKFORMAT,
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
        )
    return fig


def generate_operation_graph_casos_twinx(
    operation_data,
    variable,
    filters,
    operation_data_twinx,
    variable_twinx,
    filters_twinx,
    studies_data,
):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if operation_data is None and operation_data_twinx is None:
        return fig
    if operation_data is not None and operation_data_twinx is None:
        return generate_operation_graph_casos(
            operation_data, variable, filters, studies_data
        )
    elif operation_data is None and operation_data_twinx is not None:
        return generate_operation_graph_casos(
            operation_data_twinx, variable_twinx, filters_twinx, studies_data
        )

    Log.log().info(f"Plotando gráfico - CASOS ({variable})")
    dados = pd.read_json(StringIO(operation_data), orient="split")
    dados[START_DATE_COLUMN] = pd.to_datetime(
        dados[START_DATE_COLUMN], unit="ms"
    )
    dados[END_DATE_COLUMN] = pd.to_datetime(dados[END_DATE_COLUMN], unit="ms")
    dados_twinx = pd.read_json(StringIO(operation_data_twinx), orient="split")
    dados_twinx[START_DATE_COLUMN] = pd.to_datetime(
        dados_twinx[START_DATE_COLUMN], unit="ms"
    )
    dados_twinx[END_DATE_COLUMN] = pd.to_datetime(
        dados_twinx[END_DATE_COLUMN], unit="ms"
    )
    studies_df = pd.read_json(StringIO(studies_data), orient="split")

    line_shape = "linear"
    mode = "lines"
    visibilidade_p = __background_area_visibility(studies_df["name"])
    for _, linha_df in studies_df.iterrows():
        estudo = linha_df["name"]
        rgb = hex_to_rgb(linha_df["color"])
        cor = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 1.0)"
        cor_fundo = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 0.3)"
        dados_estudo = pivot_df_for_plot(dados.loc[dados["estudo"] == estudo])
        dados_legend = __make_operation_plot_legend_name(
            estudo, variable, filters, studies_df
        )
        dados_twinx_legend = __make_operation_plot_legend_name(
            estudo, variable_twinx, filters_twinx, studies_df
        )
        if not dados_estudo.empty:
            fig.add_trace(
                go.Scatter(
                    x=dados_estudo[START_DATE_COLUMN],
                    y=dados_estudo["mean"],
                    line={
                        "color": cor,
                        "width": LINE_WIDTH,
                        "shape": line_shape,
                    },
                    mode=mode,
                    name="mean",
                    legendgroup=dados_legend,
                    legendgrouptitle_text=dados_legend,
                )
            )
            if "p10" in dados_estudo.columns:
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo[START_DATE_COLUMN],
                        y=dados_estudo["p10"],
                        line_color=cor_fundo,
                        line_shape=line_shape,
                        mode=mode,
                        name="p10",
                        legendgroup=dados_legend,
                        visible=visibilidade_p,
                    )
                )
            if "p90" in dados_estudo.columns:
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo[START_DATE_COLUMN],
                        y=dados_estudo["p90"],
                        line_color=cor_fundo,
                        fillcolor=cor_fundo,
                        line_shape=line_shape,
                        mode=mode,
                        fill="tonexty",
                        name="p90",
                        legendgroup=dados_legend,
                        visible=visibilidade_p,
                    )
                )

        dados_estudo = pivot_df_for_plot(
            dados_twinx.loc[dados_twinx["estudo"] == estudo]
        )
        if not dados_estudo.empty:
            fig.add_trace(
                go.Scatter(
                    x=dados_estudo[START_DATE_COLUMN],
                    y=dados_estudo["mean"],
                    line={
                        "color": cor,
                        "width": LINE_WIDTH,
                        "shape": line_shape,
                        "dash": "dash",
                    },
                    name="mean",
                    legendgroup=dados_twinx_legend,
                    legendgrouptitle_text=dados_twinx_legend,
                ),
                secondary_y=True,
            )
            if "p10" in dados_estudo.columns:
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo[START_DATE_COLUMN],
                        y=dados_estudo["p10"],
                        line_color=cor_fundo,
                        line_shape=line_shape,
                        name="p10",
                        legendgroup=dados_twinx_legend,
                        visible=visibilidade_p,
                    ),
                    secondary_y=True,
                )
            if "p90" in dados_estudo.columns:
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo[START_DATE_COLUMN],
                        y=dados_estudo["p90"],
                        line_color=cor_fundo,
                        fillcolor=cor_fundo,
                        line_shape=line_shape,
                        fill="tonexty",
                        fillpattern=go.scatter.Fillpattern(
                            bgcolor=cor_fundo, shape="."
                        ),
                        name="p90",
                        legendgroup=dados_twinx_legend,
                        visible=visibilidade_p,
                    ),
                    secondary_y=True,
                )

    full_title = (
        f"{__make_operation_plot_title(variable, filters, studies_df)}"
        + f" | {__make_operation_plot_title(variable_twinx, filters_twinx, studies_df)}"
    )
    fig.update_layout(
        title={"text": full_title, "x": X_TITLE_POS, "y": Y_TITLE_POS},
        xaxis_title="Data",
        yaxis_title=_generate_yaxis_title(variable, filters, studies_df),
        yaxis_tickformat=YAXIS_TICKFORMAT,
        hovermode="x unified",
        legend=dict(groupclick="toggleitem"),
    )
    fig.update_yaxes(
        title_text=_generate_yaxis_title(
            variable_twinx, filters_twinx, studies_df
        ),
        tickformat=YAXIS_TICKFORMAT,
        secondary_y=True,
    )

    return fig


def generate_scenario_graph_casos(
    scenario_data, variable, filters, studies_data
):
    fig = go.Figure()
    if scenario_data is None:
        return fig
    Log.log().info(f"Plotando gráfico - CASOS ({variable})")
    dados = pd.read_json(StringIO(scenario_data), orient="split")
    dados[START_DATE_COLUMN] = pd.to_datetime(
        dados[START_DATE_COLUMN], unit="ms"
    )
    dados[END_DATE_COLUMN] = pd.to_datetime(dados[END_DATE_COLUMN], unit="ms")

    df_estudos = pd.read_json(StringIO(studies_data), orient="split")

    nomes_estudos = df_estudos["name"].tolist()
    cores_estudos = df_estudos["color"].tolist()
    mapas_cores = {}
    for nome, cor in zip(nomes_estudos, cores_estudos):
        rgb = hex_to_rgb(cor)
        mapas_cores[nome] = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 1.0)"
    fig = px.box(
        dados,
        x=START_DATE_COLUMN,
        y="valor_mlt",
        color="estudo",
        color_discrete_map=mapas_cores,
    )
    if variable is not None:
        fig.update_layout(
            title={
                "text": __make_scenario_plot_title(
                    variable, filters, df_estudos
                ),
                "x": X_TITLE_POS,
                "y": Y_TITLE_POS,
            },
            xaxis_title="Data",
            yaxis_title="% MLT",
            yaxis_tickformat=".0%",
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
        )
    return fig


def generate_operation_graph_encadeador(
    operation_data, variable: str, filters: dict, studies_data
):
    fig = go.Figure()
    if operation_data is None:
        return fig
    Log.log().info(f"Plotando gráfico - ENCADEADOR ({variable})")
    dados = pd.read_json(StringIO(operation_data), orient="split")
    dados[START_DATE_COLUMN] = pd.to_datetime(
        dados[START_DATE_COLUMN], unit="ms"
    )
    dados[END_DATE_COLUMN] = pd.to_datetime(dados[END_DATE_COLUMN], unit="ms")
    df_estudos = pd.read_json(StringIO(studies_data), orient="split")
    programas = df_estudos["program"].unique().tolist()

    filtro_newave = dados["programa"] == "NEWAVE"
    filtro_decomp = dados["programa"] == "DECOMP"
    df_newave = dados.loc[filtro_newave]
    df_decomp = dados.loc[filtro_decomp]
    mode = "lines"
    visibilidade_newave = __background_area_visibility(df_estudos["name"])
    for _, linha_df in df_estudos.iterrows():
        estudo = linha_df["name"]
        rgb = hex_to_rgb(linha_df["color"])
        cor = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 1.0)"
        cor_fundo = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 0.3)"

        if df_decomp is not None:
            estudo_decomp = pivot_df_for_plot(
                df_decomp.loc[df_decomp["estudo"] == estudo]
            )
            if not estudo_decomp.empty:
                fig.add_trace(
                    go.Scatter(
                        x=estudo_decomp[END_DATE_COLUMN],
                        y=estudo_decomp["mean"],
                        line={
                            "color": cor,
                            "width": 3,
                        },
                        mode=mode,
                        name=estudo,
                        legendgroup="DECOMP",
                        legendgrouptitle_text="DECOMP",
                    )
                )
        if df_newave is not None:
            estudo_newave = pivot_df_for_plot(
                df_newave.loc[df_newave["estudo"] == estudo]
            )
            if not estudo_newave.empty:
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave[END_DATE_COLUMN],
                        y=estudo_newave["mean"],
                        line={
                            "color": cor,
                            "dash": "dot",
                            "width": 2,
                        },
                        mode=mode,
                        name=estudo,
                        legendgroup="NEWAVEm",
                        legendgrouptitle_text="NEWAVEm",
                        visible=visibilidade_newave,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave[END_DATE_COLUMN],
                        y=estudo_newave["p10"],
                        line_color=cor_fundo,
                        mode=mode,
                        legendgroup="NEWAVEp10",
                        legendgrouptitle_text="NEWAVEp10",
                        name=estudo,
                        visible=visibilidade_newave,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave[END_DATE_COLUMN],
                        y=estudo_newave["p90"],
                        line_color=cor_fundo,
                        fillcolor=cor_fundo,
                        mode=mode,
                        fill="tonexty",
                        legendgroup="NEWAVEp90",
                        legendgrouptitle_text="NEWAVEp90",
                        name=estudo,
                        visible=visibilidade_newave,
                    )
                )
    if variable is not None:
        fig.update_layout(
            title=__make_operation_plot_title(variable, filters, df_estudos),
            xaxis_title="Data",
            yaxis_title=_generate_yaxis_title(variable, filters, df_estudos),
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
        )
    Log.log().info(f"Gráfico plotado - ENCADEADOR ({variable})")
    return fig


def generate_operation_graph_ppq(
    operation_data, variable, filters, studies_data
):
    fig = go.Figure()
    if operation_data is None:
        return fig
    dados = pd.read_json(StringIO(operation_data), orient="split")
    dados[START_DATE_COLUMN] = pd.to_datetime(
        dados[START_DATE_COLUMN], unit="ms"
    )
    dados[END_DATE_COLUMN] = pd.to_datetime(dados[END_DATE_COLUMN], unit="ms")

    line_shape = "linear"

    dados = dados.loc[dados["estudo"] == filters["estudo"]]

    if dados is not None:
        iteracoes = sorted(dados["iteracao"].unique().tolist())
        visibilidade_p = "legendonly" if len(iteracoes) > 2 else None
        for i, iteracao in enumerate(iteracoes):
            rgb = hex_to_rgb(
                DISCRETE_COLOR_PALLETE[i % len(DISCRETE_COLOR_PALLETE)]
            )
            cor = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 1.0)"
            cor_fundo = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 0.3)"
            dados_estudo = pivot_df_for_plot(
                dados.loc[dados["iteracao"] == iteracao]
            )
            nome = f"it {iteracao}"
            mode = "lines"
            if not dados_estudo.empty:
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo[START_DATE_COLUMN],
                        y=dados_estudo["mean"],
                        line={
                            "color": cor,
                            "width": 3,
                            "shape": line_shape,
                        },
                        mode=mode,
                        name=nome,
                        legendgroup="mean",
                        legendgrouptitle_text="mean",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo[START_DATE_COLUMN],
                        y=dados_estudo["p10"],
                        line_color=cor_fundo,
                        line_shape=line_shape,
                        mode=mode,
                        legendgroup="p10",
                        legendgrouptitle_text="p10",
                        name=nome,
                        visible=visibilidade_p,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo[START_DATE_COLUMN],
                        y=dados_estudo["p90"],
                        line_color=cor_fundo,
                        fillcolor=cor_fundo,
                        line_shape=line_shape,
                        mode=mode,
                        fill="tonexty",
                        legendgroup="p90",
                        legendgrouptitle_text="p90",
                        name=nome,
                        visible=visibilidade_p,
                    )
                )

    if variable is not None:
        fig.update_layout(
            title=__make_operation_plot_title(variable, filters, dados_estudo),
            xaxis_title="Data",
            yaxis_title=_generate_yaxis_title(variable, filters, dados_estudo),
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
        )
    return fig


def generate_distribution_graph_ppq(
    operation_data, variable, filters, studies_data
):
    fig = go.Figure()
    if operation_data is None:
        return fig
    dados = pd.read_json(StringIO(operation_data), orient="split")
    df_estudos = pd.read_json(StringIO(studies_data), orient="split")
    mapa_cor = {
        linha["name"]: linha["color"] for _, linha in df_estudos.iterrows()
    }
    ordem_estudos = dados["estudo"].unique().tolist()
    fig = px.box(
        dados,
        x="iteracao",
        y="valor",
        color="estudo",
        color_discrete_map=mapa_cor,
        category_orders={"estudo": ordem_estudos},
    )
    fig.update_layout(
        title=__make_operation_plot_title(variable, filters, dados),
        xaxis_title="Iteracao",
        yaxis_title=_generate_yaxis_title(variable, filters, dados),
        hovermode="x unified",
        legend=dict(groupclick="toggleitem"),
    )

    return fig


def __process_acumprob(operation_data: pd.DataFrame) -> pd.DataFrame:
    all_scenarios = operation_data["cenario"].unique().tolist()
    stats_scenarios = ["mean", "min", "max", "median", "std"] + [
        c for c in all_scenarios if "p" in str(c)
    ]
    vals = (
        operation_data.loc[
            ~operation_data["cenario"].isin(stats_scenarios), "valor"
        ]
        .to_numpy()
        .flatten()
    )
    df = pd.DataFrame(data={"values": vals})
    df["cdf"] = df.rank(method="average", pct=True)
    return df.sort_values("values")


def generate_acumprob_graph_casos(
    operation_data, variable, filters, studies_data
):
    fig = go.Figure()
    if operation_data is None:
        return fig
    dados = pd.read_json(StringIO(operation_data), orient="split")
    df_estudos = pd.read_json(StringIO(studies_data), orient="split")
    line_shape = "hv"
    for _, linha_df in df_estudos.iterrows():
        estudo = linha_df["name"]
        rgb = hex_to_rgb(linha_df["color"])
        cor = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 1.0)"
        if dados is not None:
            dados_estudo = dados.loc[dados["estudo"] == estudo]
            if not dados_estudo.empty:
                dados_estudo = __process_acumprob(dados_estudo)
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["cdf"] * 100,
                        y=dados_estudo["values"],
                        line_color=cor,
                        line_shape=line_shape,
                        line_width=LINE_WIDTH,
                        name=estudo,
                    )
                )

    if variable is not None:
        fig.update_layout(
            title={
                "text": __make_operation_plot_title(
                    variable, filters, df_estudos
                ),
                "x": X_TITLE_POS,
                "y": Y_TITLE_POS,
            },
            xaxis_title="%",
            yaxis_title=_generate_yaxis_title(variable, filters, df_estudos),
            yaxis_tickformat=YAXIS_TICKFORMAT,
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
        )
    return fig


def generate_timecosts_graph_encadeador(time_costs, variable, studies_data):
    fig = go.Figure()
    if time_costs is None:
        return fig
    Log.log().info(f"Plotando gráfico - ENCADEADOR ({variable})")
    dados = pd.read_json(StringIO(time_costs), orient="split")
    ordem_estudos = dados["estudo"].unique().tolist()
    df_estudos = pd.read_json(StringIO(studies_data), orient="split")
    mapa_cor = {
        linha["name"]: linha["color"] for _, linha in df_estudos.iterrows()
    }
    if "etapa" in dados.columns:
        dados = dados.loc[dados["etapa"] == "Tempo Total", :]
        dados = (
            dados.groupby(["estudo", "caso"])
            .sum(numeric_only=True)
            .reset_index()
        )
        dados["tempo"] = pd.to_timedelta(dados["tempo"], unit="s") / timedelta(
            hours=1
        )
        dados["label"] = [
            str(timedelta(hours=d)) for d in dados["tempo"].tolist()
        ]
        y_col = "tempo"
        title = "Tempo de Execução"
        unit = "Tempo (horas)"
        error_y = None
    else:
        n_parcelas = len(dados["parcela"].unique().tolist())
        df_plot = pd.DataFrame()
        for estudo in ordem_estudos:
            df_estudo = dados.loc[dados["estudo"] == estudo]
            casos = df_estudo["caso"].unique().tolist()
            for c in casos:
                df_caso = df_estudo.loc[df_estudo["caso"] == c]
                n_linhas_caso = df_caso.shape[0]
                n_exec_caso = int(n_linhas_caso / n_parcelas)
                indice_inicial_caso = (n_exec_caso - 1) * n_parcelas
                indice_final = n_exec_caso * n_parcelas + 1
                df_plot = pd.concat(
                    [
                        df_plot,
                        df_caso.iloc[indice_inicial_caso:indice_final, :],
                    ],
                    ignore_index=True,
                )

        dados = df_plot
        dados = dados.loc[dados["mean"] > 0, :]
        dados = (
            dados.groupby(["estudo", "caso"])
            .sum(numeric_only=True)
            .reset_index()
        )
        dados["label"] = dados["mean"].round(2)
        y_col = "mean"
        title = "Custos de Operação"
        unit = "Custo ($)"
        # CI de 95%
        dados["std"] *= 1.96
        error_y = "std"

    fig = px.bar(
        dados,
        x="caso",
        y=y_col,
        error_y=error_y,
        color="estudo",
        color_discrete_map=mapa_cor,
        text="label",
        category_orders={"estudo": ordem_estudos},
        barmode="group",
    )
    if variable is not None:
        fig.update_traces(textposition="inside")
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")
        fig.update_layout(
            title=title,
            yaxis_title=unit,
        )
    Log.log().info(f"Gráfico plotado - ENCADEADOR ({variable})")
    return fig


def generate_timecosts_graph_casos(time_costs, variable, studies_data):
    fig = go.Figure()
    if time_costs is None:
        return fig
    Log.log().info(f"Plotando gráfico - CASOS ({variable})")
    dados = pd.read_json(StringIO(time_costs), orient="split")
    df_estudos = pd.read_json(StringIO(studies_data), orient="split")
    mapa_cor = {
        linha["name"]: linha["color"] for _, linha in df_estudos.iterrows()
    }
    if "etapa" in dados.columns:
        dados["tempo"] = pd.to_timedelta(dados["tempo"], unit="s") / timedelta(
            hours=1
        )
        dados["label"] = [
            str(timedelta(hours=d)) for d in dados["tempo"].tolist()
        ]
        y_col = "tempo"
        color_col = "etapa"
        title = "Tempo de Execução"
        unit = "Tempo (horas)"
        error_y = None
        fig = px.bar(
            dados,
            x="estudo",
            y=y_col,
            error_y=error_y,
            color=color_col,
            color_discrete_map=mapa_cor,
            text="label",
        )
    else:
        dados = dados.loc[dados["valor_esperado"] > 0, :]
        dados["label"] = dados["valor_esperado"]
        y_col = "valor_esperado"
        color_col = "parcela"
        title = "Custos de Operação"
        unit = "Custo ($)"
        # CI de 95%
        dados["desvio_padrao"] *= 1.96
        error_y = "desvio_padrao"

        fig = px.bar(
            dados,
            x="estudo",
            y=y_col,
            error_y=error_y,
            color=color_col,
            color_discrete_sequence=DISCRETE_COLOR_PALLETE_COSTS,
            text="label",
        )
    if variable is not None:
        fig.update_traces(textposition="inside")
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")
        fig.update_layout(
            title={
                "text": title,
            },
            yaxis_tickformat=YAXIS_TICKFORMAT,
            yaxis_title=unit,
        )
    Log.log().info(f"Gráfico plotado - CASOS ({variable})")
    return fig


def generate_violation_graph_encadeador(
    violation_data, violation, studies_data
):
    fig = go.Figure()
    if violation_data is None:
        return fig

    Log.log().info(f"Plotando gráfico - ENCADEADOR ({violation})")
    dados = pd.read_json(StringIO(violation_data), orient="split")

    df_estudos = pd.read_json(StringIO(studies_data), orient="split")
    mapa_cor = {
        linha["name"]: linha["color"] for _, linha in df_estudos.iterrows()
    }

    ordem_estudos = dados["estudo"].unique().tolist()
    if violation in ["TI", "RHQ", "RE", "RHE", "RHV"]:
        unit = str(dados["unidade"].tolist()[0])
        # Grafico com montantes
        dados = (
            dados.groupby(["estudo", "caso"])
            .sum(numeric_only=True)
            .reset_index()
        )
        y_col = "violacao"
        title = f"Montante de Violação - {violation}"
    else:
        # Grafico com contagens
        unit = "Núm. Inviabilidades"
        # Grafico com montantes
        dados = dados.groupby(["estudo", "caso"]).count().reset_index()
        y_col = "violacao"
        title = f"Número de Violações - {violation}"

    fig = px.bar(
        dados,
        x="caso",
        y=y_col,
        color="estudo",
        color_discrete_map=mapa_cor,
        category_orders={"estudo": ordem_estudos},
        barmode="group",
    )
    if violation is not None:
        fig.update_traces(textposition="inside")
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")
        fig.update_layout(
            title=title,
            yaxis_title=unit,
        )
    Log.log().info(f"Gráfico plotado - ENCADEADOR ({violation})")
    return fig


def generate_convergence_graph_casos(convergence_data, variable, studies_data):
    fig = go.Figure()
    if convergence_data is None or variable is None:
        return fig
    dados = pd.read_json(StringIO(convergence_data), orient="split")
    if dados.empty:
        return fig
    dados["tempo"] = pd.to_timedelta(dados["tempo"], unit="s")
    dados["tempo"] /= timedelta(minutes=1)
    x_col = "iteracao"
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=dados[x_col], y=dados["tempo"], name="tempo"),
        secondary_y=True,
    )
    df_estudos = pd.read_json(StringIO(studies_data), orient="split")
    mapa_cor = {
        linha["name"]: linha["color"] for _, linha in df_estudos.iterrows()
    }
    if variable is not None:
        if variable == "tempo":
            fig = px.bar(
                dados,
                x=x_col,
                y=variable,
                color="estudo",
                color_discrete_map=mapa_cor,
                barmode="group",
            )
            unit = "Tempo (minutos)"
        else:
            fig = px.line(
                dados,
                x=x_col,
                y=variable,
                color="estudo",
                color_discrete_map=mapa_cor,
            )
            unit = "" if variable != "delta_zinf" else "(%)"
        fig.update_layout(
            title={
                "text": f"Convergência - {variable}",
            },
            xaxis_title="Iteração",
            yaxis_tickformat=YAXIS_TICKFORMAT,
            hovermode="x unified",
        )
        fig.update_yaxes(
            title_text=unit,
        )
    return fig


def generate_resources_graph_casos(
    cluster_data, job_data, time_data, convergence_data, study
):
    fig = go.Figure()
    if cluster_data is None:
        return fig
    if job_data is None:
        return fig
    if time_data is None:
        return fig
    if convergence_data is None:
        return fig
    master = pd.read_json(StringIO(cluster_data), orient="split")
    master = master.loc[master["estudo"] == study, :]
    job = pd.read_json(StringIO(job_data), orient="split")
    job = job.loc[job["estudo"] == study, :]
    tim = pd.read_json(StringIO(time_data), orient="split")
    tim = tim.loc[tim["estudo"] == study, :]
    conv = pd.read_json(StringIO(convergence_data), orient="split")
    conv = conv.loc[conv["estudo"] == study, :]
    if master.empty:
        return fig
    if job.empty:
        return fig
    if tim.empty:
        return fig
    if conv.empty:
        return fig
    tim["tempo"] = pd.to_timedelta(tim["tempo"], unit="s")
    conv["tempo"] = pd.to_timedelta(conv["tempo"], unit="s")
    master["timeInstant"] = pd.to_datetime(master["timeInstant"], unit="ms")
    job["timeInstant"] = pd.to_datetime(job["timeInstant"])

    # Regra: se tem múltiplos jobs pro caso, pega o último
    if "jobId" in job.columns:
        jobIds = job["jobId"]
        if len(jobIds.dropna()) > 0:
            job = job.loc[
                job["jobId"] == job.at[job["timeInstant"].idxmax(), "jobId"]
            ]

    COLS_CALCULOS_INICIAIS = [
        "Leitura de Dados",
        "Calculos Iniciais",
    ]

    tempo_total_job = tim.loc[tim["etapa"] == "Tempo Total", "tempo"].tolist()[
        0
    ]
    tempo_antes_politica = tim.loc[
        tim["etapa"].isin(COLS_CALCULOS_INICIAIS), "tempo"
    ].sum()
    instante_inicial = job["timeInstant"].tolist()[0]
    instante_inicial_politica = instante_inicial + tempo_antes_politica
    instante_final = instante_inicial + tempo_total_job

    job = job.drop(job.loc[job["timeInstant"] < instante_inicial].index)
    master = master.drop(
        master.loc[master["timeInstant"] < instante_inicial].index
    )
    job = job.drop(job.loc[job["timeInstant"] > instante_final].index)
    master = master.drop(
        master.loc[master["timeInstant"] > instante_final].index
    )

    tempos_iteracoes = conv.loc[:, ["iter", "tempo"]]
    tempos_iteracoes["paridade"] = tempos_iteracoes["iter"] % 2
    instante_final_politica = (
        instante_inicial_politica + tempos_iteracoes["tempo"].sum()
    )
    tempos_iteracoes.loc[:, "timeInstant"] = tempos_iteracoes["tempo"].cumsum()

    tempos_iteracoes["timeInstant"] += instante_inicial_politica
    tempos_iteracoes_com_inicial = [
        instante_inicial_politica
    ] + tempos_iteracoes["timeInstant"].to_list()

    job["cpuDiff"] = [0.0] + list(
        job["cpuSeconds"].to_numpy()[1:] - job["cpuSeconds"].to_numpy()[:-1]
    )
    job["memDiff"] = [0.0] + list(
        job["memoryCpuSeconds"].to_numpy()[1:]
        - job["memoryCpuSeconds"].to_numpy()[:-1]
    )
    job["memoryPerCore"] = job["memDiff"] / job["cpuDiff"]

    max_y = 1.1 * master["totalMem"].max()

    area_calculos_iniciais_x = np.array([
        instante_inicial,
        instante_inicial_politica,
    ])
    area_calculos_iniciais_y = np.ones_like(area_calculos_iniciais_x) * max_y
    area_sf_x = np.array([instante_final_politica, instante_final])
    area_sf_y = np.ones_like(area_sf_x) * max_y

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=master["timeInstant"],
            y=master["totalMem"],
            name="totalMem",
            line={"color": "rgb(38, 70, 83)", "width": 2, "dash": "dash"},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=master["timeInstant"],
            y=master["cachedMem"],
            name="cachedMem",
            line={"color": "rgb(38, 70, 83)", "width": 2, "dash": "dot"},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=master["timeInstant"],
            y=master["freeMem"],
            name="freeMem",
            line={"color": "rgb(38, 70, 83)", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=job["timeInstant"],
            y=job["memoryPerCore"],
            name="memoryPerCore",
            line={"color": "rgb(231, 111, 81)", "width": 3},
        ),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(
            x=area_calculos_iniciais_x,
            y=area_calculos_iniciais_y,
            fill="tozeroy",
            line_color="rgba(42, 157, 143, 0.5)",
            fillcolor="rgba(42, 157, 143, 0.5)",
            name="CI",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=area_sf_x,
            y=area_sf_y,
            fill="tozeroy",
            line_color="rgba(42, 157, 143, 0.5)",
            fillcolor="rgba(42, 157, 143, 0.5)",
            name="SF",
        )
    )

    for i in range(1, len(tempos_iteracoes_com_inicial), 2):
        area_x = np.array([
            tempos_iteracoes_com_inicial[i - 1],
            tempos_iteracoes_com_inicial[i],
        ])
        area_y = np.ones_like(area_x) * max_y
        fig.add_trace(
            go.Scatter(
                x=area_x,
                y=area_y,
                fill="tozeroy",
                line_color="rgba(233, 197, 106, 0.5)",
                fillcolor="rgba(233, 197, 106, 0.5)",
                showlegend=i == 1,
                name="oddIterations",
                legendgroup="iterations",
            )
        )

    for i in range(2, len(tempos_iteracoes_com_inicial), 2):
        area_x = np.array([
            tempos_iteracoes_com_inicial[i - 1],
            tempos_iteracoes_com_inicial[i],
        ])
        area_y = np.ones_like(area_x) * max_y
        fig.add_trace(
            go.Scatter(
                x=area_x,
                y=area_y,
                fill="tozeroy",
                line_color="rgba(231, 111, 81, 0.5)",
                fillcolor="rgba(231, 111, 81, 0.5)",
                showlegend=i == 2,
                name="evenIterations",
                legendgroup="iterations",
            )
        )

    fig.update_yaxes(
        title_text="Memória - Master Node (GB)",
        range=[0, 1.1 * master["totalMem"].max()],
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text="Memória por Processo (GB)",
        range=[0, 1.1 * job["memoryPerCore"].max()],
        secondary_y=True,
    )
    fig.update_layout(title=f"Uso de Recursos - {study}", hovermode="x unified")
    return fig


def __get_system_element_name(
    system_options_df: pd.DataFrame, system_elem: str, filters: dict
) -> str:
    if system_elem == "EST":
        return system_options_df.loc[
            system_options_df["estagio"] == int(filters["estagio"]), "estagio"
        ].iloc[0]
    elif system_elem == "SBM":
        return system_options_df.loc[
            system_options_df["codigo_submercado"]
            == int(filters["codigo_submercado"]),
            "submercado",
        ].iloc[0]
    elif system_elem == "SBP":
        src = system_options_df.loc[
            system_options_df["codigo_submercado"]
            == int(filters["codigo_submercado_de"]),
            "submercado",
        ].iloc[0]
        dst = system_options_df.loc[
            system_options_df["codigo_submercado"]
            == int(filters["codigo_submercado_para"]),
            "submercado",
        ].iloc[0]
        return f"{src} -> {dst}"
    elif system_elem == "REE":
        return system_options_df.loc[
            system_options_df["codigo_ree"] == int(filters["codigo_ree"]),
            "ree",
        ].iloc[0]
    elif system_elem == "UHE":
        return system_options_df.loc[
            system_options_df["codigo_usina"] == int(filters["codigo_uhe"]),
            "usina",
        ].iloc[0]
    elif system_elem == "UTE":
        return system_options_df.loc[
            system_options_df["codigo_usina"] == int(filters["codigo_ute"]),
            "usina",
        ].iloc[0]
    elif system_elem == "SIN":
        return ""


def __make_operation_plot_title(
    variable: str, filters: dict, studies: pd.DataFrame
) -> str:
    aggregation = filters["agregacao"]
    operation_options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["operacao"]), orient="split")
            for opt in studies["options"]
        ],
        ignore_index=True,
    )
    system_elem = operation_options_df.loc[
        operation_options_df["nome_longo_agregacao"] == aggregation,
        "nome_curto_agregacao",
    ].iloc[0]
    if system_elem == "SIN":
        return variable + " - " + f"{aggregation}"
    system_elem_for_options = "SBM" if system_elem == "SBP" else system_elem
    system_options_df = pd.concat(
        [
            pd.read_json(StringIO(opt[system_elem_for_options]), orient="split")
            for opt in studies["system"]
        ],
        ignore_index=True,
    )
    elem_name = __get_system_element_name(
        system_options_df, system_elem, filters
    )

    title = variable + " - " + f"{aggregation} {elem_name}"

    return title


def __make_scenario_plot_title(
    variable: str, filters: dict, studies: pd.DataFrame
) -> str:
    aggregation = filters["agregacao"]
    step = filters["etapa"]
    iteration = filters["iteracao"] if "iteracao" in filters else None
    iteration_str = f" - Iteração {iteration}" if iteration else ""
    scenario_options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["cenarios"]), orient="split")
            for opt in studies["options"]
        ],
        ignore_index=True,
    )
    system_elem = scenario_options_df.loc[
        scenario_options_df["nome_longo_agregacao"] == aggregation,
        "nome_curto_agregacao",
    ].iloc[0]

    if system_elem == "SIN":
        return (
            variable
            + " - "
            + f"{step}"
            + " - "
            + f"{aggregation}"
            + iteration_str
        )
    system_elem_for_options = "SBM" if system_elem == "SBP" else system_elem
    system_options_df = pd.concat(
        [
            pd.read_json(StringIO(opt[system_elem_for_options]), orient="split")
            for opt in studies["system"]
        ],
        ignore_index=True,
    )
    elem_name = __get_system_element_name(
        system_options_df, system_elem, filters
    )

    title = (
        variable
        + " - "
        + f"{step}"
        + " - "
        + f"{aggregation} {elem_name}"
        + iteration_str
    )

    return title


def __background_area_visibility(estudos: list) -> str:
    return "legendonly" if len(estudos) > 2 else None


def __make_operation_plot_legend_name(
    estudo: str, variable: str, filters: dict, studies: pd.DataFrame
) -> str:
    return (
        estudo + " - " + __make_operation_plot_title(variable, filters, studies)
    )
