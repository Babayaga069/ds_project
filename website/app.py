import dash
from dash import Dash, html, dcc

# for multiple pages
app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1("Main page Data Sciene Project"),
    
    # Navigation menu
    html.Div([
        dcc.Link(f"{page['name']} | ", href=page["relative_path"])
        for page in dash.page_registry.values()
    ], style={'padding': '10px', 'backgroundColor': '#f0f0f0'}),
    
    html.Hr(),
    
    # Showing page Content
    dash.page_container
    ]   
    )

if __name__ == '__main__':
    app.run(debug=True)