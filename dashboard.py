# Installations Guide
# pip install dash
# pip install pandas

# imports
import pandas as pd
import dash
from dash import dcc, html, Output, Input
import plotly.express as px

# Dash Intialization
app = dash.Dash(__name__)
app.title = 'Canadian Immigration'

# Getting Data Ready
df = pd.read_csv('canadian_immigration_data.csv')

# Styles
halfPage = {'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}

# Layout
app.layout = html.Div(children=[
    dcc.Markdown('''
    ```yaml
        Project By: Jayant Katia
    ```
    ''', style={'fontSize':'large'}),
    dcc.Markdown('''
        # Canadian Immigration
        Analyze the trends and hidden patterns of Immigrants from all over the world to Canada.

        1. Analyze Country-wise trends (Line Chart), displays Top 5 countries by default, toggle the ```Show All``` button to display all countries. 
        2. Analyze Continent-Year trends (Pie Charts), displays pie charts by Regions, Development category.
        3. Analyze Immigrants by Continent (Bar Charts)
    '''),
    
    html.H2(children='Country-wise Analysis'),
    dcc.Dropdown(id='select_continent_country_line', value='Asia', multi=False,
                options=pd.Series(df['Continent'].unique()).map(lambda country: {"label": country, "value": country}),
                style=halfPage),
    dcc.Checklist(id='checkbox_country_line', options=[
                    {'label': 'Show All', 'value': 'all'},
                ], style=halfPage),
    html.Div(id='output_country_line', children=[]),
    dcc.Graph(id='country_line', figure={}),

    html.H2(children='Continent-Year Analysis'),
    dcc.Dropdown(id='select_year_country_types_pie', value='Total', multi=False,
                options=df.columns[4:].map(lambda yr: {"label": yr, "value": yr}),
                style=halfPage),
    dcc.Dropdown(id='select_continent_continent_pie', value='Asia', multi=False,
                options=pd.Series(df['Continent'].unique()).map(lambda country: {"label": country, "value": country}),
                style=halfPage),
    html.Div(id='output_country_types_pie', children=[], style=halfPage),
    html.Div(id='output_continent_pie', children=[], style=halfPage),
    dcc.Graph(id='country_types_pie', figure={}, style=halfPage),
    dcc.Graph(id='continent_pie', figure={}, style=halfPage),

    
    html.H2(children='Immigrants by Continent'),
    dcc.Dropdown(id='select_year_continents_bar', value='Total', multi=False,
                options=df.columns[4:].map(lambda yr: {"label": yr, "value": yr}),
                style=halfPage),
    html.Div(id='output_continents_bar', children=[]),
    dcc.Graph(id='continents_bar', figure={})
])


# Callbacks
@app.callback(
    [Output(component_id='output_continents_bar', component_property='children'),
     Output(component_id='continents_bar', component_property='figure')],
    [Input(component_id='select_year_continents_bar', component_property='value')]
)
def update_continents_bar(year_selected):
    container = "The year chosen by user is: {}".format(year_selected)
    dff = df.copy()
    dff = dff.groupby('Continent')[year_selected].sum().rename('Immigrants').reset_index()    
    fig = px.bar(dff, x='Continent', y='Immigrants', labels={'Immigrants': 'Total number of Immigrants'}, color='Continent')
    return container, fig


@app.callback(
    [Output(component_id='output_country_types_pie', component_property='children'),
     Output(component_id='output_continent_pie', component_property='children'),
     Output(component_id='country_types_pie', component_property='figure'),
     Output(component_id='continent_pie', component_property='figure')],
    [Input(component_id='select_year_country_types_pie', component_property='value'),
     Input(component_id='select_continent_continent_pie', component_property='value'),
    ]
)
def update_pies(year_selected, continent_selected):
    container_year = "The year chosen by user is: {}".format(year_selected)
    container_continent = "The continent chosen by user is: {}".format(continent_selected)

    dff = df.copy()
    dff = dff[dff['Continent']==continent_selected]
    
    devDff = dff.groupby('DevName')[year_selected].sum().rename('Immigrants').reset_index()
    devPie = px.pie(devDff, values='Immigrants', names='DevName', title='Development')

    contPie = px.pie(dff, values=year_selected, names='Region', title='Regions')


    return container_year, container_continent, devPie, contPie

@app.callback(
    [Output(component_id='output_country_line', component_property='children'),
     Output(component_id='country_line', component_property='figure')],
     [Input(component_id='select_continent_country_line', component_property='value'),
     Input(component_id='checkbox_country_line', component_property='value')]
)
def update_line_chart(continent_selected, checkbox_value):
    container_continent = "The continent chosen by user is: {}".format(continent_selected)

    dff = df.copy()
    dff = dff[dff['Continent']==continent_selected]
    if not checkbox_value:
        dff=dff.nlargest(5, 'Total')
    dff = dff[['Country'] + list(dff.columns[4:-1])].set_index('Country')
    line_chart = px.line(dff.T, color='Country', markers=True)
    return container_continent, line_chart


# Run Server
if __name__ == '__main__':
    app.run_server()