import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Hiring Platform Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'user_role' not in st.session_state:
    st.error("Please log in to access this page.")
elif st.session_state.user_role == 'hr':

    df = pd.read_csv(r'F:\wise-ai-thon\hiring_platform_data.csv')

    df['Date_Applied'] = pd.to_datetime(df['Date_Applied'])

    with st.sidebar:
        st.title('Dashboard Slicer')

        date_filter_type = st.selectbox('Select Time Range', ['Weekly', 'Monthly', 'Yearly'])

        if date_filter_type == 'Weekly':
            df['Week'] = df['Date_Applied'].dt.to_period('W').apply(lambda r: r.start_time)
            selected_week = st.selectbox('Select a Week', df['Week'].unique()[::-1])
            df_selected = df[df['Week'] == selected_week]
        elif date_filter_type == 'Monthly':
            df['Month'] = df['Date_Applied'].dt.to_period('M')
            selected_month = st.selectbox('Select a Month', df['Month'].unique()[::-1])
            df_selected = df[df['Month'] == selected_month]
        elif date_filter_type == 'Yearly':
            df['Year'] = df['Date_Applied'].dt.year
            selected_year = st.selectbox('Select a Year', df['Year'].unique()[::-1])
            df_selected = df[df['Year'] == selected_year]

    fig_job = px.bar(df_selected, x='Job_Title', y='Applicant_ID', title='Number of Applicants per Job Title', 
                    labels={'Applicant_ID': 'Number of Applicants'}, color='Job_Title', height=400)
    st.plotly_chart(fig_job, use_container_width=True)

    total_applicants = df_selected['Applicant_ID'].count()
    st.markdown(f"### Total Number of Applicants: **{total_applicants}**")

    fig_stage = px.pie(df_selected, names='Application_Status', title='Stage of Hiring (Application Status)', height=400)
    st.plotly_chart(fig_stage, use_container_width=True)

    fig_source = px.histogram(df_selected, x='Source', title='Source of Applicants', labels={'Source': 'Source of Applicants'}, height=400)
    st.plotly_chart(fig_source, use_container_width=True)

    offer_accepted = df_selected['Offer_Accepted'].value_counts()
    fig_offer = px.pie(values=offer_accepted, names=offer_accepted.index, title='Offer Accepted Status', height=400)
    st.plotly_chart(fig_offer, use_container_width=True)
else:
    st.error("You do not have access to this page.")
