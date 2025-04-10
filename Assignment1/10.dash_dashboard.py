import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# ---- Load Benchmark Results ----
def load_benchmark_results():
    df = pd.read_csv("benchmark_results.csv")
    if "Time (Seconds)" in df.columns:
        df.rename(columns={"Time (Seconds)": "Execution Time"}, inplace=True)
    elif "Read Time" in df.columns:
        df.rename(columns={"Read Time": "Execution Time"}, inplace=True)
    return df

# ---- Initialize Dash App ----
app = dash.Dash(__name__)
app.title = "Benchmarking Comparison Dashboard"

# ---- Layout ----
app.layout = html.Div([
    html.H1("Benchmarking Performance Dashboard with Ploty", style={
        "textAlign": "center", 
        "fontSize": "30px", 
        "fontFamily": "Arial Black",  
        "fontWeight": "bold",
        "color": "darkred"
    }),

    # Hidden tab selector to trigger callback on startup
    dcc.Tabs(id="tabs", value="benchmark", children=[
        dcc.Tab(label="Benchmarking Results", value="benchmark"),
    ], style={"display": "none"}),  # Hidden as it's not needed

    html.Div([
        dcc.Graph(id="read-chart", style={"width": "48%", "display": "inline-block"}),
        dcc.Graph(id="write-chart", style={"width": "48%", "display": "inline-block"})
    ], style={"backgroundColor": "rgba(0,0,0,0)", "padding": "20px"}),  

    html.Footer("📌 Data sourced from benchmarking_results.csv", 
                style={"textAlign": "center", "marginTop": "20px", "fontSize": "14px", "color": "darkred"})
], style={"backgroundColor": "rgba(0,0,0,0)"})  

# ---- Callback for Both Charts ----
@app.callback(
    [Output("read-chart", "figure"),
     Output("write-chart", "figure")],
    [Input("tabs", "value")]
)
def update_charts(_):
    df = load_benchmark_results()

    # Read Speed Chart
    df_read = df[df["Operation"] == "Read"]
    fig_read = px.bar(
        df_read, x="Dataset", y="Execution Time", color="Library",
        title="CSV vs. Parquet Read Speed",
        text_auto=".2f",
        barmode="group",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"],
        template="plotly_dark"  # ✅ DARK THEME APPLIED
    )

    fig_read.update_layout(
        title_font=dict(size=20, color="white", family="Arial"),
        xaxis=dict(title="Dataset Size", title_font=dict(size=16, color="gold", family="Arial")),
        yaxis=dict(title="Execution Time (Seconds)", title_font=dict(size=16, color="white", family="Verdana")),
        font=dict(size=14, color="white", family="Arial"),
        bargap=0.2,
        plot_bgcolor="#121212", 
        paper_bgcolor="#121212" 
    )

    # Write Speed Chart
    df_write = df[df["Operation"] == "Write"]
    fig_write = px.bar(
        df_write, x="Dataset", y="Execution Time", color="Library",
        title="CSV vs. Parquet Write Speed",
        text_auto=".2f",
        barmode="group",
        color_discrete_sequence=["#d62728", "#2ca02c"],
        template="plotly_dark"  
    )

    fig_write.update_layout(
        title_font=dict(size=20, color="white", family="Arial"),
        xaxis=dict(title="Dataset Size", title_font=dict(size=16, color="gold", family="Arial")),
        yaxis=dict(title="Execution Time (Seconds)", title_font=dict(size=16, color="white", family="Verdana")),
        font=dict(size=14, color="white", family="Arial"),
        bargap=0.2,
        plot_bgcolor="rgba(0,0,0,0)",  
        paper_bgcolor="#121212"  
    )

    return fig_read, fig_write

# ---- Run the Dash App ----
if __name__ == "__main__":
    app.run_server(debug=True)
