import pandas as pd
import numpy as np 
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st


df=pd.read_csv("data/fatalities_isr_pse_conflict_2000_to_2023.csv")


st.set_page_config(
    page_title="Conflict Fatalities Dashboard",
    page_icon="⚡",
    layout="wide"   
)

st.markdown(
    """
    <style>
    
    body {
        background-color: #f5f5f5;
    }

   
    .css-1d391kg h1 {
        color: #1f77b4;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
        <h1 style="
        font-size:32px;  /* حجم الخط أصغر */
        color:#1f77b4;
        text-align:center;
        font-family: 'Arial', sans-serif;
    ">
        Conflict Fatalities Dashboard ⚡
    </h1>

    /* sidebar */
    .css-1d391kg .css-18e3th9 {
        background-color: #e6f0ff;
        padding: 20px;
        border-radius: 10px;
    }

    /* نصوص داخل الصفحة */
    .stMarkdown p {
        font-size: 16px;
        color: #333333;
    }

    /* table */
    .stDataFrame div.row-widget.stRadio > label {
        color: #1f77b4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- عنوان رئيسي ----
st.title("Conflict Fatalities Dashboard ⚡")

# ---- وصف صغير ----


st.sidebar.header("FILTERS")
years = sorted(df['year_of_event'].dropna().unique())
years_options = ["All"] + [str(y) for y in years]  
selected_years = st.sidebar.multiselect(
    "Select The Year",
    options=years_options,
    default=["All"]
)
event_month=st.sidebar.multiselect("Select The Month",sorted(df["month_name"].unique()),default=sorted(df["month_name"].unique()))
even_day=st.sidebar.multiselect("Select The Day",sorted(df["day_name"].unique()),default=sorted(df["day_name"].unique()))
if "All" in selected_years:
    filtered_df = df.copy()  
else:
    filtered_df = df[df['year_of_event'].astype(str).isin(selected_years)]


filtered_df = filtered_df[
    (filtered_df['month_name'].isin(event_month)) &
    (filtered_df['day_name'].isin(even_day))
]


# ---- KPIs ----
total_events = filtered_df.shape[0]
total_deaths = filtered_df['date_of_death'].notna().sum()  # لو date_of_death موجود → يعتبر وفاة
most_common_injury = filtered_df['type_of_injury'].mode()[0] if not filtered_df.empty else "N/A"
most_common_weapon = filtered_df['ammunition'].mode()[0] if not filtered_df.empty else "N/A"

# عرضهم في 4 أعمدة
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Events", total_events)
col2.metric("Total Deaths", total_deaths)
col3.metric("Most Common Injury", most_common_injury)
col4.metric("Most Common Weapon", most_common_weapon)

col1, col2, =st.columns(2)

with col1:
    gender_count = filtered_df['gender'].value_counts().reset_index()
    gender_count.columns = ['Gender', 'Count']
    fig_gender = px.pie(
        gender_count, 
        names='Gender', 
        values='Count',
        title="Gender Distribution",
        hole=0.4
    )
    fig_gender.update_layout(height=340, width=300)
    st.plotly_chart(fig_gender, use_container_width=True)
    
    month_name = filtered_df['month_name'].value_counts().reset_index()
    month_name.columns = ['Month', 'fatalities']
    # Create bar chart
    fig = px.bar(
        month_name,
        x='Month',
        y='fatalities',
        color='Month',
        text='fatalities',
        title="Fatalities by Type of Injury"
    )
    
    st.plotly_chart(fig,use_container_width=True)
    

with col2 :
    injury_counts = filtered_df['type_of_injury'].value_counts().reset_index()
    injury_counts.columns = ['type_of_injury', 'fatalities']
    # Create bar chart
    fig = px.bar(
        injury_counts,
        x='type_of_injury',
        y='fatalities',
        color='type_of_injury',
        text='fatalities',
        title="Fatalities by Type of Injury"
    )
    st.plotly_chart(fig,use_container_width=True)


    year_of_event = filtered_df['year_of_event'].value_counts().reset_index()
    year_of_event.columns = ['year', 'fatalities']

    # نرتب السنين علشان الرسمة تطلع مظبوطة
    year_of_event = year_of_event.sort_values('year')

    # Create line chart
    fig = px.line(
        year_of_event,
        x='year',
        y='fatalities',
        text='fatalities',
        markers=True,  # يضيف نقط على الخط
        title="Fatalities by Year of Event"
    )

    fig.update_traces(textposition="top center")

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Fatalities",
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)
    
##ahmed