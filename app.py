import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import config

df = pd.read_csv('gapminderDataFiveYear.csv')

app = dash.Dash()


# https://dash.plot.ly/dash-core-components/dropdown
# We need to construct a dictionary of dropdown values for the years
year_options = []
for year in df['year'].unique():
    year_options.append({'label':str(year),'value':year})

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(id='year-picker',options=year_options,value=df['year'].min())
    dcc.Graph(id='scatterplot',
                            figure= {'data':[
                                    go.Scatter(
                                        x=random_x,
                                        y=random_y,
                                        mode='markers',
                                        marker={
                                                'size':12,
                                                'color':'rgb(51,204,153)',
                                                'symbol':'pentagon',
                                                'line':{'width':2}


                                        }

                                    )],
                                    'layout': go.Layout(title='My Scatterplot',
                                                        xaxis={'title':'Some X title'})

                            }




)
])

@app.callback(Output('graph', 'figure'),
              [Input('year-picker', 'value')])
def update_figure(selected_year):
    filtered_df = df[df['year'] == selected_year]
    traces = []
    for continent_name in filtered_df['continent'].unique():
        df_by_continent = filtered_df[filtered_df['continent'] == continent_name]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={'size': 15},
            name=continent_name
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy'},
            hovermode='closest'
        )
    }
if __name__ == '__main__':
    app.run_server(host=config.host,port=config.porte,threaded=config.threaded,dev_tools_hot_reload=config.dev_tools_hot_reload,dev_tools_hot_reload_interval=config.dev_tools_hot_reload_interval, dev_tools_hot_reload_max_retry=config.dev_tools_hot_reload_max_retry)