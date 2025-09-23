import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random

st.set_page_config(
    page_title="Geographic Analysis",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Analyse Géographique")
st.markdown("---")

# Generate geographic data
@st.cache_data
def generate_geo_data():
    countries = [
        {"country": "Canada", "code": "CAN", "lat": 56.1304, "lon": -106.3468},
        {"country": "United States", "code": "USA", "lat": 37.0902, "lon": -95.7129},
        {"country": "France", "code": "FRA", "lat": 46.2276, "lon": 2.2137},
        {"country": "Germany", "code": "DEU", "lat": 51.1657, "lon": 10.4515},
        {"country": "United Kingdom", "code": "GBR", "lat": 55.3781, "lon": -3.4360},
        {"country": "Japan", "code": "JPN", "lat": 36.2048, "lon": 138.2529},
        {"country": "Australia", "code": "AUS", "lat": -25.2744, "lon": 133.7751},
        {"country": "Brazil", "code": "BRA", "lat": -14.2350, "lon": -51.9253},
        {"country": "India", "code": "IND", "lat": 20.5937, "lon": 78.9629},
        {"country": "China", "code": "CHN", "lat": 35.8617, "lon": 104.1954}
    ]

    data = []
    for country in countries:
        visitors = random.randint(100, 5000)
        revenue = visitors * random.uniform(10, 100)
        conversion_rate = random.uniform(1, 8)

        data.append({
            **country,
            "visitors": visitors,
            "revenue": round(revenue, 2),
            "conversion_rate": round(conversion_rate, 2),
            "avg_session_duration": random.randint(120, 600)
        })

    return pd.DataFrame(data)

df_geo = generate_geo_data()

# Canadian provinces data
@st.cache_data
def generate_canada_data():
    provinces = [
        {"province": "Ontario", "code": "ON", "visitors": random.randint(1000, 3000)},
        {"province": "Quebec", "code": "QC", "visitors": random.randint(800, 2500)},
        {"province": "British Columbia", "code": "BC", "visitors": random.randint(600, 2000)},
        {"province": "Alberta", "code": "AB", "visitors": random.randint(500, 1800)},
        {"province": "Manitoba", "code": "MB", "visitors": random.randint(200, 800)},
        {"province": "Saskatchewan", "code": "SK", "visitors": random.randint(150, 600)},
        {"province": "Nova Scotia", "code": "NS", "visitors": random.randint(200, 700)},
        {"province": "New Brunswick", "code": "NB", "visitors": random.randint(150, 500)},
        {"province": "Newfoundland and Labrador", "code": "NL", "visitors": random.randint(100, 400)},
        {"province": "Prince Edward Island", "code": "PE", "visitors": random.randint(50, 200)}
    ]
    return pd.DataFrame(provinces)

df_canada = generate_canada_data()

# Sidebar
st.sidebar.header("Filtres Géographiques")
metric_choice = st.sidebar.selectbox(
    "Métrique à visualiser",
    ["visitors", "revenue", "conversion_rate"]
)

view_type = st.sidebar.radio(
    "Vue",
    ["Mondiale", "Canada"]
)

# Key metrics
total_visitors = df_geo['visitors'].sum()
total_revenue = df_geo['revenue'].sum()
avg_conversion = df_geo['conversion_rate'].mean()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Visiteurs Totaux", f"{total_visitors:,}")
with col2:
    st.metric("Revenus Totaux", f"${total_revenue:,.2f}")
with col3:
    st.metric("Conversion Moyenne", f"{avg_conversion:.1f}%")

st.markdown("---")

if view_type == "Mondiale":
    # World map
    st.subheader("🌍 Distribution Mondiale")

    metric_labels = {
        "visitors": "Visiteurs",
        "revenue": "Revenus ($)",
        "conversion_rate": "Taux de Conversion (%)"
    }

    fig_world = px.choropleth(
        df_geo,
        locations="code",
        color=metric_choice,
        hover_name="country",
        hover_data={
            "visitors": ":,",
            "revenue": ":$,.2f",
            "conversion_rate": ":.1f%"
        },
        color_continuous_scale="Blues",
        title=f"Distribution par {metric_labels[metric_choice]}"
    )

    fig_world.update_layout(
        height=500,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )

    st.plotly_chart(fig_world, use_container_width=True)

    # Top countries table
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top Pays par Visiteurs")
        top_visitors = df_geo.nlargest(5, 'visitors')[['country', 'visitors', 'revenue']]
        st.dataframe(top_visitors, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("💰 Top Pays par Revenus")
        top_revenue = df_geo.nlargest(5, 'revenue')[['country', 'revenue', 'conversion_rate']]
        st.dataframe(top_revenue, use_container_width=True, hide_index=True)

else:
    # Canada focus
    st.subheader("🍁 Analyse du Canada")

    col1, col2 = st.columns(2)

    with col1:
        # Bar chart of Canadian provinces
        fig_canada_bar = px.bar(
            df_canada.sort_values('visitors', ascending=True),
            x='visitors',
            y='province',
            orientation='h',
            title="Visiteurs par Province",
            color='visitors',
            color_continuous_scale='Blues'
        )
        fig_canada_bar.update_layout(height=500)
        st.plotly_chart(fig_canada_bar, use_container_width=True)

    with col2:
        # Pie chart
        fig_canada_pie = px.pie(
            df_canada,
            values='visitors',
            names='province',
            title="Répartition des Visiteurs Canadiens"
        )
        fig_canada_pie.update_layout(height=500)
        st.plotly_chart(fig_canada_pie, use_container_width=True)

# Geographic performance
st.subheader("📊 Performance par Région")

col1, col2 = st.columns(2)

with col1:
    # Scatter plot: visitors vs revenue
    fig_scatter = px.scatter(
        df_geo,
        x='visitors',
        y='revenue',
        size='conversion_rate',
        color='conversion_rate',
        hover_name='country',
        title="Visiteurs vs Revenus (taille = taux de conversion)",
        color_continuous_scale='Viridis'
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    # Conversion rate comparison
    fig_conversion = px.bar(
        df_geo.sort_values('conversion_rate', ascending=False),
        x='country',
        y='conversion_rate',
        title="Taux de Conversion par Pays",
        color='conversion_rate',
        color_continuous_scale='RdYlBu_r'
    )
    fig_conversion.update_xaxis(tickangle=45)
    fig_conversion.update_layout(height=400)
    st.plotly_chart(fig_conversion, use_container_width=True)