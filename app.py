import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & NOC Branding
st.set_page_config(page_title="NOC Digital Fact Book", layout="wide")
noc_red = "#CC092F"
noc_gray = "#888B8D"

st.title("🏛️ Northern Oklahoma College: Digital Fact Book")
st.markdown("### Strategic Enrollment & Demographic Dashboard")

# 2. Sidebar for User Controls (CLO 5, 7)
st.sidebar.header("Dashboard Filters")
df = pd.read_csv('Combined_NOC_3YR_Data.csv')

# Year Filter
available_years = sorted(df['yr_cde'].unique())
selected_year = st.sidebar.selectbox("Select Academic Year", available_years)

# Filter Data based on selection
df_filtered = df[df['yr_cde'] == selected_year].copy()

# 3. Data Preparation (Race/Ethnicity Logic)
df_filtered['Demographic'] = df_filtered.apply(
    lambda x: 'Hispanic/Latino' if x['ethnic_rpt_desc'] == 'Hispanic/Latino' else x['race1'],
    axis=1
).fillna('Unknown/Unreported')

# 4. The 6-Panel Layout (using Streamlit Columns)
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

# Chart 1: Overall (Top Left)
with col1:
    st.subheader("Overall Demographics")
    fig1 = px.pie(df_filtered, names='Demographic', color_discrete_sequence=[noc_red, noc_gray, "#333333"])
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Tonkawa
with col2:
    st.subheader("Tonkawa (TONK)")
    df_tonk = df_filtered[df_filtered['loc_cde'] == 'TONK']
    st.bar_chart(df_tonk['Demographic'].value_counts())
# Chart 3: Enid
with col3:
    st.subheader("Enid (ENID)")
    df_enid = df_filtered[df_filtered['loc_cde'] == 'ENID']
    st.bar_chart(df_enid['Demographic'].value_counts())
#Chart 4: Stillwater
with col4:
    st.subheader("Stillwater (STIL)")
    df_stil = df_filtered[df_filtered['loc_cde'] == 'STIL']
    st.bar_chart(df_stil['Demographic'].value_counts())

# Chart 5: Digital Campus (ONLI + VRTAL)
with col5:
    st.subheader("Digital Campus (ONLI/VRTAL)")
    df_digital = df_filtered[df_filtered['loc_cde'].isin(['ONLI', 'VRTAL'])]
    fig5 = px.bar(df_digital['Demographic'].value_counts(), color_discrete_sequence=[noc_red])
    st.plotly_chart(fig5, use_container_width=True)
#Chart 6: Credit Hours by Race
with col6:
    st.subheader("Credit Hours by Race")
    df_credit = df_filtered.groupby('Demographic')['credit_hrs'].sum().reset_index()
    fig6 = px.bar(
        df_credit,
        x='Demographic',
        y='credit_hrs',
        color='Demographic',
        color_discrete_sequence=[noc_red, noc_gray, "#333333"],
        title=""
    )
    st.plotly_chart(fig6, use_container_width=True)

# 5. Data Download Feature
st.sidebar.markdown("---")
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download Filtered Data", data=csv, file_name=f"NOC_Data_{selected_year}.csv")
