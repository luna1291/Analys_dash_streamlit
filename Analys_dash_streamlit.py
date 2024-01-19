import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Analysis", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# загрузка файла или выбор файла по умолчанию
fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    st.write(fl.name)
    df = pd.read_excel(fl.read())
    st.write("filename:", fl.name)
else:
    df = pd.read_excel('./data/tech_analysis.xlsx')


   
# выбор даты 
col1, col2 = st.columns((2))
df["date_df"] = pd.to_datetime(df["date_df"].sort_values(ascending=False))
 
startDate = pd.to_datetime(df["date_df"]).max()
endDate = pd.to_datetime(df["date_df"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["date_df"] >= date1) & (df["date_df"] <= date2)].copy()


#график с барами и показателем ema
st.header("EURRUB")
fig = go.Figure(data=[go.Candlestick(x=df['datetime_df'],
                open=df['open'], high=df['high'],
                low=df['low'], close=df['close'],
                )
                     ])

fig.update_layout(xaxis_rangeslider_visible=True)

fig2 = go.Figure(go.Scatter(
    x = df['datetime_df'],
    y = df['ema']
))

fig2.update_xaxes(
    rangeslider_visible=True,
    tickformatstops = [
        dict(dtickrange=[None, 1000], value="datetime_df")
    ]
)

fig3 = go.Figure(data = fig.data + fig2.data)
fig3.update_layout(height = 280, showlegend = False, margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig3, use_container_width=True)


# выбор показателей
st.sidebar.header("Choose your filter: ",)

indicators_df = st.sidebar.multiselect("Indicators", df.iloc[:, 10:].columns)
if not indicators_df:
    df1 = pd.concat([df.iloc[:, 1], df.iloc[:, 4:10]], axis=1)
else:
    df1 = pd.concat([df.iloc[:, 1], df.iloc[:, 4:10], df[indicators_df]], axis=1)

chart_data = pd.DataFrame(
    df)

 #графики по фильтрам
fig6 = px.line(df1, x=df1.datetime_df, y=df1[indicators_df].columns,
            #   hover_data={"datetime_df": "|%B %d, %Y"},
              title='Filter chart',
              )
fig6.update_xaxes(visible=False)
fig6.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="right",
    x=1
), height = 180, margin=dict(l=0, r=0, t=0, b=0))

st.plotly_chart(fig6,  use_container_width=True)


# тренды объема
st.text('Volume')
fig7 = go.Figure()

fig7.add_trace(go.Bar(
    x=df1['datetime_df'],
    y=df1.volume,
))

fig7.add_trace(go.Scatter(
    x=df1.datetime_df,
    y=df1[indicators_df].columns,
))

fig7.update_layout(hovermode="x unified", height = 130, showlegend = False, margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig7,  use_container_width=True)


# таблица данных
st.dataframe(df1, use_container_width=True)


# python -m streamlit run Analys_dash_streamlit.py
