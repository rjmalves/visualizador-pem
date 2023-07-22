import math
import geopandas
from src.utils import constants
import networkx as nx
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict


def __load_submercado_shape(
    arq: str = "./src/assets/submercados.geojson", simplify_tol: float = 0.1
) -> geopandas.GeoDataFrame:
    shape_gdf = geopandas.read_file(arq)
    shape_gdf["geometry"] = shape_gdf["geometry"].simplify(
        tolerance=simplify_tol
    )
    return shape_gdf


def __generate_submercado_graph(
    submercado_data_df: pd.DataFrame, intercambio_data_df: pd.DataFrame
) -> nx.Graph:
    nos = constants.NOS_SUBMERCADOS_NEWAVE
    attrs = submercado_data_df.columns.tolist()
    for _, line in submercado_data_df.iterrows():
        for a in attrs:
            nos[line["nome"]][a] = line[a]
    arestas = constants.ARESTAS_INTERCAMBIOS_NEWAVE
    int_data = np.abs(intercambio_data_df["valor"].to_numpy())
    max_int = np.max(int_data)
    max_width = 4.5
    min_width = 1.0
    for _, line in intercambio_data_df.iterrows():
        arestas[(line["source"], line["target"])] = {
            **arestas[(line["source"], line["target"])],
            "label": line["label"],
            "INT": line["valor"],
            "width": np.abs(line["valor"]) / max_int * max_width + min_width,
            "color": "rgb(255,250,220)",
        }

    # espessura varia conforme valor absoluto
    # cor varia conforme valor relativo ao limite do intercâmbio

    submercado_graph = nx.from_pandas_edgelist(
        constants.INTERCAMBIOS_SUBMERCADOS_NEWAVE,
        edge_attr=True,
        create_using=nx.DiGraph,
    )
    nx.set_node_attributes(submercado_graph, nos)
    nx.set_edge_attributes(submercado_graph, arestas)
    return submercado_graph


def __add_edge(
    start,
    end,
    lengthFrac=1,
    arrowPos=None,
    arrowLength=0.025,
    arrowAngle=30,
    dotSize=20,
):
    x0, y0 = start["pos"]
    x1, y1 = end["pos"]

    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    dotSizeConversion = 0.0565 / 20
    convertedDotDiameter = dotSize * dotSizeConversion
    lengthFracReduction = convertedDotDiameter / length
    lengthFrac = lengthFrac - lengthFracReduction

    skipX = (x1 - x0) * (1 - lengthFrac)
    skipY = (y1 - y0) * (1 - lengthFrac)
    x0 = x0 + skipX / 2
    x1 = x1 - skipX / 2
    y0 = y0 + skipY / 2
    y1 = y1 - skipY / 2

    edge_x = []
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y = []
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

    if not arrowPos == None:
        pointx = x1
        pointy = y1

        eta = (
            math.degrees(math.atan((x1 - x0) / (y1 - y0)))
            if y1 != y0
            else 90.0
        )

        if arrowPos == "middle" or arrowPos == "mid":
            pointx = x0 + (x1 - x0) / 2
            pointy = y0 + (y1 - y0) / 2

        signx = (x1 - x0) / abs(x1 - x0) if x1 != x0 else +1
        signy = (y1 - y0) / abs(y1 - y0) if y1 != y0 else +1

        dx = arrowLength * math.sin(math.radians(eta + arrowAngle))
        dy = arrowLength * math.cos(math.radians(eta + arrowAngle))
        edge_x.append(pointx)
        edge_x.append(pointx - signx**2 * signy * dx)
        edge_x.append(None)
        edge_y.append(pointy)
        edge_y.append(pointy - signx**2 * signy * dy)
        edge_y.append(None)

        dx = arrowLength * math.sin(math.radians(eta - arrowAngle))
        dy = arrowLength * math.cos(math.radians(eta - arrowAngle))
        edge_x.append(pointx)
        edge_x.append(pointx - signx**2 * signy * dx)
        edge_x.append(None)
        edge_y.append(pointy)
        edge_y.append(pointy - signx**2 * signy * dy)
        edge_y.append(None)

    return edge_x, edge_y


def __create_graph_traces_for_plot(
    G: nx.Graph,
    node_attrs: List[str] = ["EARPF", "GHID", "GTER", "CMO"],
    edge_attrs: List[str] = ["INT"],
) -> list[go.Trace]:
    def make_node_text_info(label, node) -> str:
        text = f"<br><b>{label}</b></br>"
        for a in node_attrs:
            text += (
                f"{a}:".ljust(7)
                + f"{node[a]:.2f} {constants.VARIABLE_UNITS[a]}".rjust(15)
                + "<br>"
            )
        return text

    def make_edge_text_info(edge) -> str:
        text = f"<br><b>{edge['label']}</b></br>"
        text += (
            f"{np.abs(edge['INT']):.2f} {constants.VARIABLE_UNITS['INT']}".rjust(
                15
            )
            + "<br>"
        )
        return text

    def make_edge(start, end, edge):
        if edge["INT"] <= 0:
            start, end = end, start
        edge_x, edge_y = __add_edge(
            start, end, lengthFrac=0.7, arrowPos="end", arrowLength=0.75
        )
        return go.Scattergeo(
            lon=edge_x,
            lat=edge_y,
            mode="lines+text",
            line={"width": edge["width"], "color": edge["color"]},
            showlegend=False,
        )

    def generate_rectangle_frame(center, sizes) -> List[List[float]]:
        left_x = center[0] - sizes[0] / 2
        right_x = center[0] + sizes[0] / 2
        lower_y = center[1] - sizes[1] / 2
        upper_y = center[1] + sizes[1] / 2

        return [left_x, left_x, right_x, right_x, left_x], [
            lower_y,
            upper_y,
            upper_y,
            lower_y,
            lower_y,
        ]

    edge_traces = []

    for edge in G.edges():
        start = G.nodes[edge[0]]
        end = G.nodes[edge[1]]
        edge_trace = make_edge(start, end, G.edges[edge])
        text_x, text_y = G.edges[edge]["textposition"]
        frame_x, frame_y = generate_rectangle_frame(
            G.edges[edge]["textposition"], G.edges[edge]["textframe"]
        )
        rectangle_trace = go.Scattergeo(
            lon=frame_x,
            lat=frame_y,
            mode="lines",
            fill="toself",
            line={
                "color": "black",
            },
            fillcolor="rgba(230, 215, 181, 1.0)",
            showlegend=False,
        )
        text_trace = go.Scattergeo(
            lon=[text_x],
            lat=[text_y],
            mode="text",
            text=make_edge_text_info(G.edges[edge]),
            showlegend=False,
        )
        edge_traces += [edge_trace, rectangle_trace, text_trace]

    node_traces = []
    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        text_x, text_y = G.nodes[node]["textposition"]
        frame_x, frame_y = generate_rectangle_frame(
            G.nodes[node]["textposition"], G.nodes[node]["textframe"]
        )
        node_trace = go.Scattergeo(
            lon=[x],
            lat=[y],
            mode="markers",
            hovertemplate=None,
            marker=dict(
                color=G.nodes[node]["color"],
                size=G.nodes[node]["size"],
                line=dict(width=2, color="DarkSlateGrey"),
            ),
            showlegend=False,
        )
        if not G.nodes[node]["fict"]:
            rectangle_trace = go.Scattergeo(
                lon=frame_x,
                lat=frame_y,
                mode="lines",
                fill="toself",
                line={
                    "color": "black",
                },
                fillcolor="white",
                showlegend=False,
            )

            text_trace = go.Scattergeo(
                lon=[text_x],
                lat=[text_y],
                mode="text",
                text=make_node_text_info(node, G.nodes[node]),
                showlegend=False,
            )
            node_traces += [node_trace, rectangle_trace, text_trace]
        else:
            node_traces += [node_trace]
    return edge_traces + node_traces


def view_SBM_EST(
    data_df: dict,
) -> go.Figure:
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if not all(["SBM" in data_df, "INT" in data_df]):
        return fig
    if any([data_df["SBM"] is None, data_df["INT"] is None]):
        return fig
    submercado_data_df = pd.read_json(data_df["SBM"], orient="split")
    intercambio_data_df = pd.read_json(data_df["INT"], orient="split")
    submercado_graph = __generate_submercado_graph(
        submercado_data_df, intercambio_data_df
    )
    gdf = __load_submercado_shape()
    fig = px.choropleth(
        submercado_data_df.loc[submercado_data_df.index.isin([1, 2, 3, 4])],
        geojson=gdf["geometry"],
        locations=gdf.index,
        color="EARPF",
        color_continuous_scale="Blues",
        range_color=[0.0, 100.0],
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.add_traces(__create_graph_traces_for_plot(submercado_graph))
    fig.update_traces(hovertemplate=None, hoverinfo="skip")
    fig.update_layout(
        coloraxis_showscale=False, margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return fig
