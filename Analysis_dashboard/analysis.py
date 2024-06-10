
from dash import dcc, html, Dash, Input, Output, State, callback_context
import os

app = Dash(__name__, suppress_callback_exceptions=True)

def load_html_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error loading file: {str(e)}"

def format_filename(filename):
    return filename.split('/')[-1].replace('.html', '').replace('_', ' ').title()

lineplot_files1 = [
    "plot/box_plot_alx.html",
    "plot/box_plot_aly.html",
    "plot/box_plot_alz.html",
    "plot/box_plot_arx.html",
    "plot/box_plot_ary.html",
    "plot/box_plot_arz.html",
    "plot/box_plot_glx.html",
    "plot/box_plot_gly.html",
    "plot/box_plot_glz.html",
    "plot/box_plot_grx.html",
    "plot/box_plot_gry.html",
    "plot/box_plot_grz.html",
]

lineplot_files2 = [
    "plot/spectrogram_cycling.html",
    "plot/spectrogram_jump.html",
    "plot/spectrogram_run.html",
    "plot/spectrogram_climbing.html",
    "plot/spectrogram_walk.html",
]

lineplot_files3 = [
    "rf_rankings.png"
]

lineplot_files5 = [
    "climbing_correlation_heatmap.png",
    "cycling_correlation_heatmap.png",
    "jumping_correlation_heatmap.png",
    "run_correlation_heatmap.png",
    "walking_correlation_heatmap.png"
]
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('Sensor Data for Physical Activity Recognition Analysis Dashboard', style={'color': 'white', 'text-align': 'center'}),
            html.Div([
                html.Button('Feature Selection', id='btn-converse', n_clicks=0, style={
                    'background-color': 'hotpink', 'border': '2px solid black', 'color': 'white',
                    'border-radius': '15px', 'padding': '15px 30px', 'margin': '10px', 'font-size': '18px'}),
                html.Button('Analysis', id='btn-non-converse', n_clicks=0, style={
                    'background-color': 'yellow', 'border': '2px solid black', 'color': 'black',
                    'border-radius': '15px', 'padding': '15px 30px', 'margin': '10px', 'font-size': '18px'}),
            ], style={'textAlign': 'center', 'display': 'flex', 'justify-content': 'center', 'flex-wrap': 'wrap'})
        ], style={'flex-grow': '2', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'}),
        html.Div([
            html.Img(id='dynamic-image', src="assets/pie.png", style={"height": "300px", "width": "100%"})
        ], style={'flex-grow': '1', 'max-width': '50%'}),
    ], style={'display': 'flex', 'backgroundColor': 'black', 'align-items': 'center', 'padding': '10px'}),
    html.Div(id='content-container', children=[])
])



@app.callback(
    Output('content-container', 'children'),
    [Input('btn-converse', 'n_clicks'), Input('btn-non-converse', 'n_clicks')]
)
def toggle_layout(btn_converse, btn_non_converse):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0] if callback_context.triggered else ''
    
    if 'btn-non-converse' in changed_id:
        return html.Div([
            # Flex container for Heatmap and Spectrogram
            html.Div([
                # Heatmap section
                html.Div([
                    html.H2('Heatmap', style={'textAlign': 'center', 'backgroundColor': 'lavender'}),
                    dcc.Dropdown(
                        id='variables-dropdown5',
                        options=[{'label': format_filename(filename), 'value': filename} for filename in lineplot_files5],
                        value=lineplot_files5[0]
                    ),
                    html.Div(id='dropdown-output-container5')
                ], style={'width': '50%', 'display': 'inline-block'}),

                # Spectrogram section
                html.Div([
                    html.H2('Spectrogram', style={'textAlign': 'center', 'backgroundColor': 'lavender'}),
                    dcc.Dropdown(
                        id='variables-dropdown2',
                        options=[{'label': format_filename(filename), 'value': filename} for filename in lineplot_files2],
                        value=lineplot_files2[0]
                    ),
                    html.Div(id='dropdown-output-container2')
                ], style={'width': '50%', 'display': 'inline-block'}),
            ], style={'display': 'flex'}),

            # Box Plot section
            html.Div([
                html.H2('Box Plot', style={'textAlign': 'center', 'backgroundColor': 'lavender'}),
                dcc.Dropdown(
                    id='variables-dropdown1',
                    options=[{'label': format_filename(filename), 'value': filename} for filename in lineplot_files1],
                    value=lineplot_files1[0]
                ),
                html.Div(id='dropdown-output-container1')
            ])
        ])

    
    elif 'btn-converse' in changed_id:
        return html.Div([
            html.H2('Rankings', style={'textAlign': 'center', 'backgroundColor': 'lavender'}),
            dcc.Dropdown(
                id='variables-dropdown3',
                options=[{'label': format_filename(filename), 'value': filename} for filename in lineplot_files3],
                value=lineplot_files3[0],
                style={'width': '100%', 'padding': '10px'}  # Ensure this element's width fits as expected
            ),
            html.Div(id='dropdown-output-container3')
        ], style={'width': '100%', 'padding': '20px'})

    

@app.callback(
    Output('dropdown-output-container1', 'children'),
    Input('variables-dropdown1', 'value')
)
def render_content_1(selected_filename):
    return render_content(selected_filename)

@app.callback(
    Output('dropdown-output-container2', 'children'),
    Input('variables-dropdown2', 'value')
)
def render_content_2(selected_filename):
    return render_content(selected_filename)

@app.callback(
    Output('dropdown-output-container5', 'children'),
    Input('variables-dropdown5', 'value')
)
def update_image(selected_filename):
    if selected_filename:
        image_path = f'/assets/{selected_filename}'
        return html.Img(src=image_path,
                        style={'width': '100%', 'max-height': '500px', 'object-fit': 'contain'})
    else:
        return "Please select an image."

@app.callback(
    Output('dropdown-output-container3', 'children'),
    Input('variables-dropdown3', 'value')
)
def update_image(selected_filename):
    if selected_filename:
        image_path = f'/assets/{selected_filename}'
        return html.Img(src=image_path,
                        style={'width': '100%', 'max-height': '500px', 'object-fit': 'contain'})
    else:
        return "Please select an image."


def render_content(selected_filename):
    if selected_filename.endswith('.html'):
        with open(selected_filename, 'r') as file:
            plot_html = file.read()
        return html.Iframe(srcDoc=plot_html, style={"height": "600px", "width": "100%"})
    else:
        return "Unsupported file type."

if __name__ == '__main__':
    app.run_server(debug=True)
