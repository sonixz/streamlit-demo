import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Analytics Avancées")
st.markdown("---")

# Generate more detailed analytics data
@st.cache_data
def generate_analytics_data():
    dates = pd.date_range(start=datetime.now() - timedelta(days=90), end=datetime.now(), freq='H')
    data = []

    for date in dates:
        hour = date.hour
        # Simulate different patterns based on hour of day
        base_traffic = 100 + (50 * np.sin(hour * np.pi / 12))  # Daily pattern
        traffic = max(10, int(base_traffic + random.gauss(0, 20)))

        data.append({
            'datetime': date,
            'date': date.date(),
            'hour': hour,
            'traffic': traffic,
            'bounce_rate': max(0.1, min(0.9, 0.4 + random.gauss(0, 0.1))),
            'page_views': traffic * random.randint(2, 5),
            'session_duration': max(30, 180 + random.gauss(0, 60))
        })

    return pd.DataFrame(data)

df_analytics = generate_analytics_data()

# Sidebar filters
st.sidebar.header("Filtres Analytics")
period = st.sidebar.selectbox(
    "Période",
    ["7 derniers jours", "30 derniers jours", "90 derniers jours"]
)

period_map = {
    "7 derniers jours": 7,
    "30 derniers jours": 30,
    "90 derniers jours": 90
}

filtered_df = df_analytics[
    df_analytics['datetime'] >= (datetime.now() - timedelta(days=period_map[period]))
]

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_traffic = filtered_df['traffic'].sum()
    st.metric(
        "Trafic Total",
        f"{total_traffic:,}",
        delta=f"+{random.randint(5, 25)}%"
    )

with col2:
    avg_bounce = filtered_df['bounce_rate'].mean()
    st.metric(
        "Taux de Rebond",
        f"{avg_bounce:.1%}",
        delta=f"{random.uniform(-0.05, 0.05):+.1%}"
    )

with col3:
    total_pageviews = filtered_df['page_views'].sum()
    st.metric(
        "Pages Vues",
        f"{total_pageviews:,}",
        delta=f"+{random.randint(10, 30)}%"
    )

with col4:
    avg_session = filtered_df['session_duration'].mean()
    st.metric(
        "Durée Session Moy.",
        f"{avg_session:.0f}s",
        delta=f"+{random.randint(5, 15)}s"
    )

# Traffic patterns
st.subheader("🌊 Patterns de Trafic")

col1, col2 = st.columns(2)

with col1:
    # Hourly traffic pattern
    hourly_traffic = filtered_df.groupby('hour')['traffic'].mean().reset_index()
    fig_hourly = px.line(
        hourly_traffic,
        x='hour',
        y='traffic',
        title="Trafic Moyen par Heure",
        markers=True
    )
    fig_hourly.update_layout(
        xaxis_title="Heure de la journée",
        yaxis_title="Trafic moyen",
        height=400
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

with col2:
    # Daily traffic
    daily_traffic = filtered_df.groupby('date')['traffic'].sum().reset_index()
    fig_daily = px.bar(
        daily_traffic.tail(14),
        x='date',
        y='traffic',
        title="Trafic Quotidien (14 derniers jours)"
    )
    fig_daily.update_layout(height=400)
    st.plotly_chart(fig_daily, use_container_width=True)

# Heatmap
st.subheader("🔥 Heatmap du Trafic")

# Create heatmap data
heatmap_data = filtered_df.pivot_table(
    values='traffic',
    index=filtered_df['datetime'].dt.hour,
    columns=filtered_df['datetime'].dt.day_name(),
    aggfunc='mean'
)

# Reorder columns to start with Monday
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heatmap_data = heatmap_data.reindex(columns=[col for col in day_order if col in heatmap_data.columns])

fig_heatmap = px.imshow(
    heatmap_data,
    title="Trafic par Heure et Jour de la Semaine",
    aspect="auto",
    color_continuous_scale="Blues"
)
fig_heatmap.update_layout(
    xaxis_title="Jour de la Semaine",
    yaxis_title="Heure de la Journée",
    height=500
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Performance metrics
st.subheader("⚡ Métriques de Performance")

col1, col2 = st.columns(2)

with col1:
    # Bounce rate over time
    daily_bounce = filtered_df.groupby('date')['bounce_rate'].mean().reset_index()
    fig_bounce = px.line(
        daily_bounce,
        x='date',
        y='bounce_rate',
        title="Évolution du Taux de Rebond",
        color_discrete_sequence=['#e74c3c']
    )
    fig_bounce.update_yaxis(tickformat='.1%')
    fig_bounce.update_layout(height=400)
    st.plotly_chart(fig_bounce, use_container_width=True)

with col2:
    # Session duration
    daily_session = filtered_df.groupby('date')['session_duration'].mean().reset_index()
    fig_session = px.area(
        daily_session,
        x='date',
        y='session_duration',
        title="Durée Moyenne des Sessions",
        color_discrete_sequence=['#2ecc71']
    )
    fig_session.update_layout(
        yaxis_title="Durée (secondes)",
        height=400
    )
    st.plotly_chart(fig_session, use_container_width=True)