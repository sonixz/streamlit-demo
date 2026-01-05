import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Dashboard Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Dashboard Streamlit Demo")
st.markdown("---")

# Sidebar
st.sidebar.header("Paramètres")
date_range = st.sidebar.date_input(
    "Période d'analyse",
    value=[datetime.now() - timedelta(days=30), datetime.now()],
    max_value=datetime.now()
)

metric_type = st.sidebar.selectbox(
    "Type de métrique",
    ["Ventes", "Utilisateurs", "Revenus", "Conversions"]
)

# Generate sample data
@st.cache_data
def generate_sample_data(days=30):
    dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq='D')
    data = []

    for date in dates:
        data.append({
            'date': date,
            'ventes': random.randint(50, 200),
            'utilisateurs': random.randint(100, 500),
            'revenus': round(random.uniform(1000, 5000), 2),
            'conversions': round(random.uniform(2, 8), 2)
        })

    return pd.DataFrame(data)

df = generate_sample_data()

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = df['ventes'].sum()
    st.metric(
        label="Ventes Totales",
        value=f"{total_sales:,}",
        delta=f"+{random.randint(5, 15)}%"
    )

with col2:
    avg_users = df['utilisateurs'].mean()
    st.metric(
        label="Utilisateurs Moyens",
        value=f"{avg_users:.0f}",
        delta=f"+{random.randint(2, 10)}%"
    )

with col3:
    total_revenue = df['revenus'].sum()
    st.metric(
        label="Revenus Totaux",
        value=f"${total_revenue:,.2f}",
        delta=f"+{random.randint(8, 20)}%"
    )

with col4:
    avg_conversion = df['conversions'].mean()
    st.metric(
        label="Taux Conversion Moyen",
        value=f"{avg_conversion:.1f}%",
        delta=f"+{random.uniform(0.1, 0.5):.1f}%"
    )

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Évolution des Ventes")
    fig_sales = px.line(
        df,
        x='date',
        y='ventes',
        title="Ventes par jour",
        color_discrete_sequence=['#1f77b4']
    )
    fig_sales.update_layout(height=400)
    st.plotly_chart(fig_sales, use_container_width=True)

with col2:
    st.subheader("👥 Distribution des Utilisateurs")
    fig_users = px.bar(
        df.tail(7),
        x='date',
        y='utilisateurs',
        title="Utilisateurs - 7 derniers jours",
        color_discrete_sequence=['#ff7f0e']
    )
    fig_users.update_layout(height=400)
    st.plotly_chart(fig_users, use_container_width=True)

# Revenue analysis
st.subheader("💰 Analyse des Revenus")
col1, col2 = st.columns([2, 1])

with col1:
    fig_revenue = go.Figure()
    fig_revenue.add_trace(go.Scatter(
        x=df['date'],
        y=df['revenus'],
        mode='lines+markers',
        name='Revenus',
        line=dict(color='#2ca02c', width=3),
        marker=dict(size=6)
    ))

    fig_revenue.add_trace(go.Scatter(
        x=df['date'],
        y=df['revenus'].rolling(window=7).mean(),
        mode='lines',
        name='Moyenne mobile (7j)',
        line=dict(color='#d62728', width=2, dash='dash')
    ))

    fig_revenue.update_layout(
        title="Revenus quotidiens avec tendance",
        xaxis_title="Date",
        yaxis_title="Revenus ($)",
        height=400
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

with col2:
    st.subheader("🎯 Objectifs")

    # Progress bars for goals
    sales_goal = 2000
    revenue_goal = 80000

    sales_progress = min(total_sales / sales_goal, 1.0)
    revenue_progress = min(total_revenue / revenue_goal, 1.0)

    st.markdown("**Objectif Ventes**")
    st.progress(sales_progress)
    st.write(f"{total_sales:,} / {sales_goal:,} ({sales_progress:.1%})")

    st.markdown("**Objectif Revenus**")
    st.progress(revenue_progress)
    st.write(f"${total_revenue:,.0f} / ${revenue_goal:,} ({revenue_progress:.1%})")

# Data table
st.markdown("---")
st.subheader("📋 Données Détaillées")

# Filters for the table
col1, col2, col3 = st.columns(3)
with col1:
    min_sales = st.number_input("Ventes minimum", min_value=0, value=0)
with col2:
    min_users = st.number_input("Utilisateurs minimum", min_value=0, value=0)
with col3:
    sort_by = st.selectbox("Trier par", ["date", "ventes", "utilisateurs", "revenus"])

# Apply filters
filtered_df = df[
    (df['ventes'] >= min_sales) &
    (df['utilisateurs'] >= min_users)
].sort_values(by=sort_by, ascending=False)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
        "ventes": st.column_config.NumberColumn("Ventes", format="%d"),
        "utilisateurs": st.column_config.NumberColumn("Utilisateurs", format="%d"),
        "revenus": st.column_config.NumberColumn("Revenus", format="$%.2f"),
        "conversions": st.column_config.NumberColumn("Conversions", format="%.1f%%")
    }
)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        🚀 Dashboard créé avec Streamlit |
        📊 Données générées aléatoirement pour la démo |
        ☁️ Hébergé sur Azure Web App
    </div>
    """,
    unsafe_allow_html=True
)