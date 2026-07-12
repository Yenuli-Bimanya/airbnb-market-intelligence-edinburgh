"""
Edinburgh Airbnb Market Intelligence Dashboard
Section 08 — Interactive analytics app (Plotly Dash)

Run from project root:
    python dashboard/app.py

Then open: http://127.0.0.1:8050
"""

from __future__ import annotations

from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, dash_table, dcc, html

COLORS = {
    "primary": "#1e3a5f",
    "secondary": "#2c5282",
    "accent": "#3182ce",
    "success": "#38a169",
    "warning": "#d69e2e",
    "background": "#f0f2f6",
    "card": "#ffffff",
    "muted": "#64748b",
}
CHART_PALETTE = ["#3182ce", "#2c5282", "#4299e1", "#63b3ed", "#90cdf4"]
KPI_ACCENTS = ["#3182ce", "#38a169", "#d69e2e", "#805ad5"]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "edinburgh" / "2026-06-23"
TABLES_DIR = PROJECT_ROOT / "reports" / "tables"
SNAPSHOT_DATE = "2026-06-23"
CITY = "Edinburgh"


def load_listings() -> pd.DataFrame:
    listings_path = PROCESSED_DIR / "listings_enriched.parquet"
    if not listings_path.exists():
        raise FileNotFoundError(
            f"Missing {listings_path}. Run `python -m src.pipeline` first."
        )
    listings = pd.read_parquet(listings_path)
    listings = listings[(listings["is_valid_price"] == True) & listings["price"].notna()].copy()
    listings["price"] = listings["price"].astype(float)
    return listings


def load_report_table(filename: str) -> pd.DataFrame:
    path = TABLES_DIR / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def apply_chart_style(fig: go.Figure, height: int = 380) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=24, r=24, t=52, b=24),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8fafc",
        font=dict(family="Segoe UI, sans-serif", color=COLORS["primary"], size=12),
        title=dict(font=dict(size=15, color=COLORS["primary"])),
        colorway=CHART_PALETTE,
        xaxis=dict(gridcolor="#e2e8f0", linecolor="#cbd5e0"),
        yaxis=dict(gridcolor="#e2e8f0", linecolor="#cbd5e0"),
    )
    return fig


def make_kpi_card(title: str, value: str, subtitle: str, accent_color: str) -> dbc.Card:
    return dbc.Card(
        [
            html.Div(className="kpi-accent", style={"backgroundColor": accent_color}),
            dbc.CardBody(
                [
                    html.P(title, className="mb-1", style={"color": COLORS["muted"], "fontSize": "0.85rem"}),
                    html.H4(value, className="kpi-value mb-0"),
                    html.Small(subtitle, style={"color": COLORS["muted"]}),
                ]
            ),
        ],
        className="kpi-card h-100",
    )


def wrap_chart(graph_component) -> html.Div:
    return html.Div(graph_component, className="chart-container")


listings_df = load_listings()
model_comparison_df = load_report_table("price_model_comparison.csv")
feature_importance_df = load_report_table("price_model_feature_importance.csv")
hypothesis_df = load_report_table("hypothesis_test_summary.csv")
topic_df = load_report_table("review_topic_summary.csv")
sentiment_corr_df = load_report_table("review_sentiment_rating_correlation.csv")

def get_neighbourhood_column(df: pd.DataFrame) -> str:
    """Use cleansed neighbourhood names (raw `neighbourhood` is empty in this snapshot)."""
    if "neighbourhood_cleansed" in df.columns and df["neighbourhood_cleansed"].notna().any():
        return "neighbourhood_cleansed"
    return "neighbourhood"


NEIGHBOURHOOD_COLUMN = get_neighbourhood_column(listings_df)
neighbourhood_options = sorted(listings_df[NEIGHBOURHOOD_COLUMN].dropna().unique())
room_type_options = sorted(listings_df["room_type"].dropna().unique())

median_price = listings_df["price"].median()
mean_rating = listings_df["review_scores_rating"].mean()
mean_occupancy = listings_df["occupancy_proxy"].mean()


def build_market_figures(filtered: pd.DataFrame) -> tuple[go.Figure, go.Figure, go.Figure, go.Figure]:
    if filtered.empty:
        empty = apply_chart_style(px.scatter(title="No data for selected filters"))
        return empty, empty, empty, empty

    neighbourhood_summary = (
        filtered.groupby(NEIGHBOURHOOD_COLUMN, as_index=False)["price"]
        .median()
        .sort_values("price", ascending=False)
        .head(15)
    )
    fig_neighbourhood = apply_chart_style(
        px.bar(
            neighbourhood_summary,
            x="price",
            y=NEIGHBOURHOOD_COLUMN,
            orientation="h",
            title="Median Price by Neighbourhood (Top 15)",
            labels={"price": "Median price (£)", NEIGHBOURHOOD_COLUMN: "Neighbourhood"},
            color_discrete_sequence=[COLORS["accent"]],
        )
    )

    fig_room_type = apply_chart_style(
        px.box(
            filtered,
            x="room_type",
            y="price",
            title="Price Distribution by Room Type",
            labels={"room_type": "Room type", "price": "Price (£)"},
            color="room_type",
            color_discrete_sequence=CHART_PALETTE,
        )
    )
    fig_room_type.update_layout(xaxis_tickangle=-20, showlegend=False)

    rating_df = filtered.dropna(subset=["review_scores_rating"])
    rating_sample = rating_df.sample(n=min(1500, len(rating_df)), random_state=42)
    fig_rating = apply_chart_style(
        px.scatter(
            rating_sample,
            x="review_scores_rating",
            y="price",
            opacity=0.5,
            title="Price vs Review Score",
            labels={"review_scores_rating": "Review score", "price": "Price (£)"},
            color_discrete_sequence=[COLORS["secondary"]],
        )
    )

    fig_occupancy = apply_chart_style(
        px.bar(
            filtered.groupby("room_type", as_index=False)["occupancy_proxy"].mean(),
            x="room_type",
            y="occupancy_proxy",
            title="Mean Occupancy Proxy by Room Type",
            labels={"room_type": "Room type", "occupancy_proxy": "Occupancy proxy"},
            color_discrete_sequence=[COLORS["success"]],
        )
    )
    fig_occupancy.update_layout(xaxis_tickangle=-20)

    return fig_neighbourhood, fig_room_type, fig_rating, fig_occupancy


INITIAL_MARKET_FIGS = build_market_figures(listings_df)


def market_explorer_layout() -> html.Div:
    return html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Filters", className="section-title"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Neighbourhood", style={"fontWeight": 600}),
                                        dcc.Dropdown(
                                            id="filter-neighbourhood",
                                            options=[{"label": n, "value": n} for n in neighbourhood_options],
                                            multi=True,
                                            placeholder="All neighbourhoods",
                                        ),
                                    ],
                                    md=6,
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Room type", style={"fontWeight": 600}),
                                        dcc.Dropdown(
                                            id="filter-room-type",
                                            options=[{"label": r, "value": r} for r in room_type_options],
                                            multi=True,
                                            placeholder="All room types",
                                        ),
                                    ],
                                    md=6,
                                ),
                            ]
                        ),
                    ]
                ),
                className="content-card mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        wrap_chart(
                            dcc.Graph(
                                id="chart-price-by-neighbourhood",
                                figure=INITIAL_MARKET_FIGS[0],
                                config={"displayModeBar": False},
                            )
                        ),
                        md=6,
                    ),
                    dbc.Col(
                        wrap_chart(
                            dcc.Graph(
                                id="chart-price-by-room-type",
                                figure=INITIAL_MARKET_FIGS[1],
                                config={"displayModeBar": False},
                            )
                        ),
                        md=6,
                    ),
                ],
                className="g-3",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        wrap_chart(
                            dcc.Graph(
                                id="chart-price-vs-rating",
                                figure=INITIAL_MARKET_FIGS[2],
                                config={"displayModeBar": False},
                            )
                        ),
                        md=6,
                    ),
                    dbc.Col(
                        wrap_chart(
                            dcc.Graph(
                                id="chart-occupancy-by-room-type",
                                figure=INITIAL_MARKET_FIGS[3],
                                config={"displayModeBar": False},
                            )
                        ),
                        md=6,
                    ),
                ],
                className="g-3 mt-2",
            ),
        ]
    )


def nlp_layout() -> html.Div:
    topic_chart = html.Div()
    if not topic_df.empty:
        plot_df = topic_df.sort_values("reviews_in_sample", ascending=True)
        fig = apply_chart_style(
            px.bar(
                plot_df,
                x="reviews_in_sample",
                y="interpreted_label",
                orientation="h",
                title="Review Topics (NMF on 10k sample)",
                labels={"reviews_in_sample": "Reviews in sample", "interpreted_label": "Topic"},
                color="reviews_in_sample",
                color_continuous_scale=["#bee3f8", "#3182ce", "#1e3a5f"],
            ),
            height=420,
        )
        fig.update_layout(showlegend=False)
        topic_chart = wrap_chart(dcc.Graph(figure=fig, config={"displayModeBar": False}))

    corr_text = "Sentiment-rating correlation file not found."
    if not sentiment_corr_df.empty:
        pearson_row = sentiment_corr_df[sentiment_corr_df["metric"] == "pearson"]
        if not pearson_row.empty:
            corr_value = pearson_row.iloc[0]["correlation"]
            if pd.notna(corr_value):
                corr_text = (
                    f"Pearson correlation between listing mean text sentiment and review score: "
                    f"{corr_value:.3f} (weak-to-moderate relationship is expected)."
                )
            else:
                corr_text = (
                    "Pearson correlation could not be computed reliably on the sampled data. "
                    "This can happen when sentiment scores have low variance in the sample."
                )

    return html.Div(
        [
            dbc.Alert(
                [
                    html.Strong("NLP Insights  |  "),
                    "Outputs from notebooks/05_nlp_reviews.ipynb (TextBlob sentiment + TF-IDF/NMF topics).",
                ],
                className="alert-banner mb-4",
                style={"backgroundColor": COLORS["secondary"], "color": "#ffffff"},
            ),
            dbc.Row(
                [
                    dbc.Col(topic_chart, md=7),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Sentiment vs rating", className="section-title"),
                                    html.P(corr_text),
                                    html.Hr(),
                                    html.H6("Key insight", style={"color": COLORS["accent"]}),
                                    html.P(
                                        "Review comments and star ratings measure different signals. "
                                        "Use both together for a fuller guest satisfaction picture.",
                                        style={"color": COLORS["muted"]},
                                    ),
                                ]
                            ),
                            className="content-card insight-card h-100",
                        ),
                        md=5,
                    ),
                ],
                className="g-3",
            ),
        ]
    )


def ml_layout() -> html.Div:
    if model_comparison_df.empty:
        return dbc.Alert("ML comparison table not found. Run notebook 04 first.", color="warning")

    best_model = model_comparison_df.sort_values("test_mae").iloc[0]["model"]
    comparison_fig = apply_chart_style(
        px.bar(
            model_comparison_df,
            x="model",
            y="test_mae",
            title="Model Comparison (lower MAE is better)",
            labels={"model": "Model", "test_mae": "Test MAE"},
            text="test_mae",
            color="model",
            color_discrete_sequence=CHART_PALETTE,
        )
    )
    comparison_fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    comparison_fig.update_layout(showlegend=False)

    importance_component = html.Div()
    if not feature_importance_df.empty:
        top_features = feature_importance_df.head(12).sort_values("importance", ascending=True)
        top_features["feature"] = top_features["feature"].str.replace("numeric__", "", regex=False)
        top_features["feature"] = top_features["feature"].str.replace("categorical__", "", regex=False)
        importance_fig = apply_chart_style(
            px.bar(
                top_features,
                x="importance",
                y="feature",
                orientation="h",
                title="Top Price Drivers (Random Forest)",
                labels={"importance": "Importance", "feature": "Feature"},
                color_discrete_sequence=[COLORS["accent"]],
            ),
            height=420,
        )
        importance_component = wrap_chart(
            dcc.Graph(figure=importance_fig, config={"displayModeBar": False})
        )

    return html.Div(
        [
            dbc.Alert(
                [html.Strong("Best model  |  "), f"{best_model} (lowest test MAE)"],
                className="alert-banner mb-4",
                style={"backgroundColor": COLORS["success"], "color": "#ffffff"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        wrap_chart(
                            dcc.Graph(figure=comparison_fig, config={"displayModeBar": False})
                        ),
                        md=5,
                    ),
                    dbc.Col(importance_component, md=7),
                ],
                className="g-3",
            ),
        ]
    )


def stats_layout() -> html.Div:
    if hypothesis_df.empty:
        return dbc.Alert("Hypothesis summary table not found. Run notebook 03 first.", color="warning")

    display_df = hypothesis_df.copy()
    display_df["significant_0_05"] = display_df["significant_0_05"].map({True: "Yes", False: "No"})

    return html.Div(
        [
            html.H5("Hypothesis Test Summary (H1–H5)", className="section-title"),
            dbc.Card(
                dash_table.DataTable(
                    data=display_df.to_dict("records"),
                    columns=[{"name": col, "id": col} for col in display_df.columns],
                    page_size=10,
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "textAlign": "left",
                        "padding": "10px",
                        "fontFamily": "Segoe UI, sans-serif",
                        "border": "1px solid #e2e8f0",
                    },
                    style_header={
                        "fontWeight": "bold",
                        "backgroundColor": COLORS["primary"],
                        "color": "#ffffff",
                        "border": "1px solid #1e3a5f",
                    },
                    style_data={"backgroundColor": "#ffffff"},
                    style_data_conditional=[
                        {"if": {"row_index": "odd"}, "backgroundColor": "#f8fafc"},
                    ],
                ),
                className="content-card p-3",
            ),
        ]
    )


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Edinburgh Airbnb Market Intelligence",
    suppress_callback_exceptions=True,
)

app.layout = html.Div(
    [
        html.Div(
            [
                html.H2("Edinburgh Airbnb Market Intelligence"),
                html.P(
                    f"Inside Airbnb snapshot: {SNAPSHOT_DATE}  |  "
                    f"{len(listings_df):,} listings with valid prices  |  {CITY}"
                ),
            ],
            className="dashboard-header",
        ),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(make_kpi_card("Listings analysed", f"{len(listings_df):,}", "Valid nightly prices", KPI_ACCENTS[0]), md=3),
                        dbc.Col(make_kpi_card("Median price", f"£{median_price:,.0f}", "Per night (GBP)", KPI_ACCENTS[1]), md=3),
                        dbc.Col(make_kpi_card("Mean review score", f"{mean_rating:.2f}", "Out of 5", KPI_ACCENTS[2]), md=3),
                        dbc.Col(make_kpi_card("Mean occupancy proxy", f"{mean_occupancy:.2%}", "Calendar-based estimate", KPI_ACCENTS[3]), md=3),
                    ],
                    className="g-3 mb-4",
                ),
                dbc.Tabs(
                    [
                        dbc.Tab(label="Market Explorer", tab_id="tab-market", tab_class_name="nav-link"),
                        dbc.Tab(label="Reviews & NLP", tab_id="tab-nlp", tab_class_name="nav-link"),
                        dbc.Tab(label="ML Insights", tab_id="tab-ml", tab_class_name="nav-link"),
                        dbc.Tab(label="Statistical Tests", tab_id="tab-stats", tab_class_name="nav-link"),
                    ],
                    id="main-tabs",
                    active_tab="tab-market",
                ),
                html.Div(id="tab-content", children=market_explorer_layout()),
            ],
            fluid=True,
            className="pb-4",
        ),
    ],
    style={"backgroundColor": COLORS["background"], "minHeight": "100vh"},
)


@app.callback(Output("tab-content", "children"), Input("main-tabs", "active_tab"))
def render_tab(active_tab: str):
    if active_tab == "tab-market":
        return market_explorer_layout()
    if active_tab == "tab-nlp":
        return nlp_layout()
    if active_tab == "tab-ml":
        return ml_layout()
    if active_tab == "tab-stats":
        return stats_layout()
    return market_explorer_layout()


@app.callback(
    Output("chart-price-by-neighbourhood", "figure"),
    Output("chart-price-by-room-type", "figure"),
    Output("chart-price-vs-rating", "figure"),
    Output("chart-occupancy-by-room-type", "figure"),
    Input("filter-neighbourhood", "value"),
    Input("filter-room-type", "value"),
    Input("main-tabs", "active_tab"),
)
def update_market_charts(selected_neighbourhoods, selected_room_types, active_tab):
    if active_tab != "tab-market":
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    filtered = listings_df.copy()
    if selected_neighbourhoods:
        filtered = filtered[filtered[NEIGHBOURHOOD_COLUMN].isin(selected_neighbourhoods)]
    if selected_room_types:
        filtered = filtered[filtered["room_type"].isin(selected_room_types)]

    return build_market_figures(filtered)


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)
