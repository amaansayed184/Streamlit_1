import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
st.set_page_config(layout="wide",page_title='Startup Analysis')

df= pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

def load_overall_analysis():
    st.title('overall Analysis')
    coln1,coln2,coln3,coln4=st.columns(4)
    with coln1:
        total=round(df['amount'].sum())
        st.metric('Total',str(total)+'CR')
    with coln2:
        max_amount = round(df['amount'].max())
        st.metric('Max', str(max_amount) + 'CR')
    with coln3:
        mean_amount = round(df.groupby('startup')['amount'].sum().mean())
        st.metric('AVG', str(mean_amount) + 'CR')
    with coln4:
        startup_count = df['startup'].nunique()
        st.metric('Total Funded Startups', str(startup_count))
    st.header("MoM graph")
    select_option=st.selectbox('Select type',['total','count'])
    if select_option=='total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    elif select_option=='count':
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()


    temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig7, ax7 = plt.subplots()
    ax7.plot(temp_df['x-axis'], temp_df['amount'])
    st.pyplot(fig7)
def load_investor_details(investor):
    st.title(investor)
    data=df[df['investors'].str.contains(investor)].head()
    big_df = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False)
    st.subheader('Most Recent Invesments')
    st.dataframe(data)
    coln1,coln2=st.columns(2)
    with coln1:
        st.subheader('Biggest Invesments')
        fig, ax=plt.subplots()
        ax.bar(big_df.index,big_df.values)
        st.pyplot(fig)
    with coln2:
       verical_series= df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
       # st.subheader('Biggest Invesments')
       fig1, ax1 = plt.subplots()
       ax1.pie(verical_series,labels=verical_series.index,autopct='%0.01f%%')
       st.pyplot(fig1)
    coln3,coln4,coln5=st.columns(3)
    with coln3:
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        # st.subheader('Biggest Invesments')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct='%0.01f%%')
        st.pyplot(fig2)
    with coln4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        # st.subheader('Biggest Invesments')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct='%0.01f%%')
        st.pyplot(fig3)

    with coln5:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
        year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        # st.subheader('Biggest Invesments')

        fig6, ax6 = plt.subplots()
        ax6.plot(year_series.index,year_series.values)
        ax6.set_title('investments by year')
        ax6.set_xlabel('Year')
        ax6.set_ylabel('total investment amount')
        ax6.grid(True)
        st.pyplot(fig6)
st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select one',['overall Analysis','Startup','investor'])

if option =='overall Analysis':
    load_overall_analysis()

elif option =='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup details')
    st.title('Startup Analysis')

else:
    select_investor =st.sidebar.selectbox('Select',sorted(df['investors'].str.split(',').sum()))
    st.title('investor Analysis')
    btn2 = st.sidebar.button('Find investor details')
    if btn2:
        load_investor_details(select_investor)

