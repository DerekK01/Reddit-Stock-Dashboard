#
#		Reddit Stock Analysis Dash Webpage
#		Created by Derek Kwan
#
#	Info: Create a webpage using the Dash module
#




from pickle import TRUE
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import pandas_datareader.data as web
from datetime import date as dt
from datetime import datetime
import time
from dataAnalysis import getNumberOfMention, getTopMentionedStock, getTopMentionedStockTop10
from dash import dash_table


#Set up two static graph (The table and pie chart)
startt = int(datetime(2022, 11, 21, 0, 0, 0).strftime('%s'))
endt = int(datetime(2022, 11, 27, 11, 59, 59).strftime('%s'))
stock , mention = getTopMentionedStockTop10("http://localhost:3000/{}/query?{}" ,startt,endt)

#Dataframe for the table
dfm = pd.DataFrame([stock, mention]).T
dfm.columns = ['Stock', 'Mention']

#Pie chart setting
mentionDf = getTopMentionedStock("http://localhost:3000/{}/query?{}" ,startt,endt)
figPie = px.pie(mentionDf, values='Mentions', names='Stock', title='Stock Mentions frequency',hole=.3)
figPie.update_traces(textposition='inside')
figPie.update_layout(plot_bgcolor="#1f2630",paper_bgcolor="#252E3F",
uniformtext_minsize=12, 
uniformtext_mode='hide',
xaxis=dict(
showline=True,
showgrid=False,
showticklabels=True,
linecolor='rgb(26, 135, 237)',),yaxis=dict(
showgrid=False),
font=dict(
size=18,
color="white"
))

app = Dash(__name__)
server = app.server
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(children="Reddit Stock Sentiment Analysis"),
                html.P(
                    id="description",
                    children="Created by Derek Kwan",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Pick a stock symbol:",
                                ),
                                    #dropdown option
                                    dcc.Dropdown(id="stock_dropdown",
                                                options=[
                                                    {"label": "TSLA", "value": 'TSLA'},
                                                    {"label": "AAPL", "value": 'AAPL'},
                                                    {"label": "GOOGL", "value": 'GOOGL'},
                                                    {"label": "GME", "value": 'GME'},
                                                    {"label": "SE", "value": 'SE'},
                                                    {"label": "NVDA", "value": 'NVDA'},
                                                    {"label": "AMC", "value": 'AMC'}],
                                                multi=False,
                                                value='TSLA',
                                                style={'width': "60%"}
                                                ),
                                    
                                    #Graph display option
                                    dcc.RadioItems(id='stock_radio',
                                    options=[
                                        {'label': 'Line (close)', 'value': 'LINE'},
                                        {'label': 'CandleStick', 'value': 'CS'},
                                    ],
                                    value='LINE'
                                    ),
                                    html.Br(),

                                    #Graph date range
                                    dcc.DatePickerRange(
                                        id='stock_date_range',
                                        min_date_allowed=dt(1995, 8, 5),
                                        max_date_allowed=dt.today(),
                                        initial_visible_month=dt.today(),
                                        updatemode='bothdates',
                                        style={'color': "#7fafdf"}

                                    ),
                            ],
                        ),
                        html.Div(
                            id="heatmap-container",
                            children=[

                                #Stock price Graph
                                html.P(
                                    "Stock price with mention frequency",
                                    id="heatmap-title",
                                ),
                                dcc.Graph(id='stock_graph', figure={}),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Top 10 stock mentioned (Weekly update)"),

                        #Top 10 mention table setting
                        dash_table.DataTable(
                        id='table_id',
                        columns = [{"name": i, "id": i} for i in dfm.columns],
                        data = dfm.to_dict("rows"),
                        fixed_rows={'headers': True, 'data': 0},
                        fixed_columns={'headers': True, 'data': 0},
                        cell_selectable=False,
                        style_as_list_view = True,
                        #fill_width=False,
                        style_table={'height': '200px', 'overflowY': 'auto'},
                        style_cell={
                            'textAlign': 'center',
                            'padding': '5px',
                            'border': '1px rgb(26, 135, 237)',
                            'width': '200px'
                        },
                        style_header={
                            'backgroundColor': '#1f2630',
                            'fontWeight': 'bold',
                            'border': '1px rgb(26, 135, 237)',
                            'fontSize':20
                        },
                        style_data={
                            'backgroundColor': '#252E3F',
                            'color': 'white',
                            'fontSize':18
                        },
                        ),
                        html.Div(
                        id="graph-container2",
                        children=[

                        #Pie chart
                        html.P(id="pie-chart"),

                        dcc.Graph(figure=figPie),
                    ],
                ),
                    ],
                ),
            ],
        ),
    ],
)




# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    #Usage:
    #Output(component_id='output_container', component_property='children'),
    Output(component_id='stock_graph', component_property='figure'),
    Input(component_id='stock_dropdown', component_property='value'),
    Input(component_id='stock_radio', component_property='value'),
    Input(component_id='stock_date_range', component_property='start_date'),
    Input(component_id='stock_date_range', component_property='end_date')
)

def update_graph(stock_dropdown_values, radio_values,start_date,end_date):

    #Get the date ranges and the choosen stock
    container = "The stock chosen: {}".format(stock_dropdown_values)
    if start_date is None:
        sd=dt(2016,1,1)
    else:
        sd = dt.fromisoformat(start_date)
    if end_date is None:
        ed=dt.today()
    else:
        ed = dt.fromisoformat(end_date)

    #Setup stock price dataframe, values from yahoo finance
    df = web.DataReader(
        stock_dropdown_values,'yahoo',
        start=sd, end=ed
    )
    
    #Set the display option (Line graph/Candle graph)
    if radio_values == 'LINE':
        #line graph
        fig = go.Figure(data=go.Scatter(x=df.index, y=df['Close'],mode="lines",name="Stock Price"))
    else:
        #Candle graph
        fig = go.Figure(
            data=[go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name="Stock Price")])

    #Get the mentioned data using the local API (connected to mongoDB)
    stockMention = {}
    url = "http://localhost:3000/{}/query?{}" 
    if start_date is None:
        startEpoch=int(dt(2016,1,1).strftime('%s'))
    else:
        startEpoch = int(dt.fromisoformat(start_date).strftime('%s'))
    if end_date is None:
        endEpoch= int(dt.today().strftime('%s'))
    else:
        endEpoch = int(dt.fromisoformat(end_date).strftime('%s'))

    #Setup the dataframe
    #Loop through each day 
    for i in range(startEpoch,endEpoch,86400):
        startTime = i
        endTime = i + 86400
        #Get readable date format
        date = datetime.fromtimestamp(startTime).strftime("%Y-%m-%d")
        stockMention[date] =  getNumberOfMention(url,"posts",text=stock_dropdown_values,start=startTime,end=endTime)
    stockMentionDF = pd.DataFrame.from_dict(stockMention, orient='index',columns=["Mention"])
    
    #The mention line graph
    fig2 = go.Figure(data=go.Scatter(x=stockMentionDF.index, y=stockMentionDF['Mention'],mode="lines",name="Mentions",line=dict(color="#8ecae6")))


#px returns a complete figure, but add_trace (add_traces, append_trace) wants just the data.
#adding ".data[0]" to the end of the px figure to combine both graph

    #combine the mention graph with the stock price 
    mainFig = make_subplots(specs=[[{"secondary_y": True}]])
    mainFig.add_trace(fig.data[0])
    mainFig.add_trace(fig2.data[0],secondary_y=True)

    #Setting for line graph and candle graph
    mainFig.update_layout(title_text="{} Stock Price".format(stock_dropdown_values))
    if radio_values == 'LINE':
        mainFig.update_layout(plot_bgcolor="#1f2630",paper_bgcolor="#252E3F",xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(26, 135, 237)',),yaxis=dict(
        showgrid=False),
        font=dict(
        size=18,
        color="white"
        ))
    else:
        mainFig.update_layout(xaxis_rangeslider_visible=False)
        mainFig.update_layout(plot_bgcolor="#1f2630",paper_bgcolor="#252E3F",xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(26, 135, 237)',),yaxis=dict(
        showgrid=False),
        font=dict(
        size=18,
        color="white"
        ))

    #update the graph
    return mainFig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)