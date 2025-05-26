import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Current Without Voltage Dashboard", layout="wide", page_icon="⚡")
st.title("⚡ Current Without Voltage Event Analytics Dashboard")

# --- Read data ---
df = pd.read_excel("CURRENT_WITHOUT_VOLTAGE_JAN_TO_APRIL_UPDATED_14_05_2025.xlsx")

# --- Automatic column detection ---
circle_col = next((col for col in df.columns if "CIRCLE" in col.upper()), None)
manufacturer_col = next((col for col in df.columns if "MANUFACTURER" in col.upper()), None)
sanction_col = next((col for col in df.columns if "SANCTION" in col.upper() and ("KW" in col.upper() or "KWH" in col.upper())), None)

# --- Show data preview ---
st.markdown("### Data Preview")
st.dataframe(df, use_container_width=True)

# --- Top Summary Cards ---
st.markdown("### Key Metrics")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Cases", len(df))
with c2:
    st.metric("Unique Circles", df[circle_col].nunique() if circle_col else "NA")
with c3:
    st.metric("Meter Manufacturers", df[manufacturer_col].nunique() if manufacturer_col else "NA")

st.markdown("---")

# ========== 1. Circle-wise cases generated ==========
st.markdown("## 1. Circle-wise Cases Generated")
if circle_col:
    circle_counts = df[circle_col].value_counts().reset_index()
    circle_counts.columns = ['Circle', 'Cases Generated']
    circle_counts = circle_counts.sort_values(by='Cases Generated', ascending=True)  # For horizontal bar

    fig1 = go.Figure(go.Bar(
        x=circle_counts['Cases Generated'],
        y=circle_counts['Circle'],
        orientation='h',
        marker=dict(
            color=circle_counts['Cases Generated'],
            colorscale='Viridis',
        ),
        text=circle_counts['Cases Generated'],
        textposition='auto',
        hovertemplate='Circle: %{y}<br>Cases: %{x}<extra></extra>'
    ))
    fig1.update_layout(
        title='Circle-wise Cases Generated',
        xaxis_title='Cases Generated',
        yaxis_title='Circle',
        template='plotly_white',
        height=500,
        plot_bgcolor='#f7fbff',
        font=dict(size=15, family="Montserrat")
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("CIRCLE column not found in data.")

# ========== 2. Cases generated against meter manufacturer ==========
st.markdown("## 2. Cases Generated Against Meter Manufacturer")
if manufacturer_col:
    man_counts = df[manufacturer_col].value_counts().reset_index()
    man_counts.columns = [manufacturer_col, 'count']
    fig2 = px.pie(
        man_counts,
        names=manufacturer_col,
        values='count',
        title="Cases by Meter Manufacturer",
        hole=0.45,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig2.update_traces(
        textinfo='percent+label',
        marker=dict(line=dict(color='#fff', width=2))
    )
    fig2.update_layout(
        template='seaborn',
        showlegend=True,
        height=500,
        font=dict(size=15, family="Montserrat")
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Meter Manufacturer column not found in data.")

# ========== 3. Sanction Load > 10 kWh ==========
st.markdown("## 3. Cases with Sanction Load > 10 kW")
if sanction_col:
    df[sanction_col] = pd.to_numeric(df[sanction_col], errors='coerce')
    df_gt_10 = df[df[sanction_col] > 10]
    st.write(f"**Total cases with Sanction Load > 10 kW: {len(df_gt_10)}**")

    fig3 = px.histogram(
        df_gt_10,
        x=sanction_col,
        nbins=20,
        title='Distribution of Sanction Load (>10kW)',
        color_discrete_sequence=['#2E8B57'],
        opacity=0.85
    )
    fig3.update_traces(marker_line_color='black', marker_line_width=1)
    fig3.update_layout(
        xaxis_title='Sanction Load (kW)',
        yaxis_title='Number of Cases',
        template='simple_white',
        bargap=0.2,
        height=500,
        font=dict(size=15, family="Montserrat")
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("Sanction Load column not found in data.")

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#6c757d; font-size:16px;'>Made by Esyasoft</div>",
    unsafe_allow_html=True
)
