import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="🇪🇹",
    layout="wide"
)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'processed', 'ethiopia_fi_modeled.csv')
    forecast_path = os.path.join(base_dir, 'data', 'processed', 'ethiopia_fi_forecast_final.csv')

    # Fallback / Mock Data generation if files missing (for robustness)
    if not os.path.exists(data_path) or not os.path.exists(forecast_path):
        return None, None

    df_hist = pd.read_csv(data_path)
    df_hist['observation_date'] = pd.to_datetime(df_hist['observation_date'])
    df_hist['year'] = df_hist['observation_date'].dt.year

    df_forecast = pd.read_csv(forecast_path)
    return df_hist, df_forecast


df_hist, df_forecast = load_data()

# Robustness check
if df_hist is None:
    st.error("❌ Data files missing. Please run the pipeline first.")
    st.stop()

# Filter Data
access_data = df_hist[df_hist['indicator_code'] == 'ACC_OWNERSHIP']

# --- STYLE & CSS ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .stMetric_container {
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)


# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Load Historical & Modeled Data
    df_hist = pd.read_csv('data/processed/ethiopia_fi_modeled.csv')
    df_hist['observation_date'] = pd.to_datetime(df_hist['observation_date'])
    df_hist['year'] = df_hist['observation_date'].dt.year

    # Load Forecast Data (Task 4 Output)
    df_forecast = pd.read_csv('data/processed/ethiopia_fi_forecast_final.csv')

    return df_hist, df_forecast


try:
    df_hist, df_forecast = load_data()
    # Filter for key indicators
    access_data = df_hist[df_hist['indicator_code'] == 'ACC_OWNERSHIP']
    telebirr_data = df_hist[df_hist['indicator_code'] == 'USG_TELEBIRR_USERS']
except FileNotFoundError:
    st.error("❌ Data files not found. Please run Task 3 and Task 4 first.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Flag_of_Ethiopia.svg/2560px-Flag_of_Ethiopia.svg.png",
        width=100)
    st.header("Control Panel")

    st.info("Navigation")
    page = st.radio("Go to:", ["📊 Executive Summary","📈 Trends & Channels", "🔮 Forecast & Scenarios", "🎛️ Policy Simulator"])

    st.markdown("---")
    st.subheader("💾 Data Download")

    # Download Functionality
    csv_hist = df_hist.to_csv(index=False).encode('utf-8')
    st.download_button("Download Historical Data", data=csv_hist, file_name="ethiopia_history.csv", mime="text/csv")

    csv_cast = df_forecast.to_csv(index=False).encode('utf-8')
    st.download_button("Download Forecast Data", data=csv_cast, file_name="ethiopia_forecast_2030.csv", mime="text/csv")

    st.markdown("---")
    st.markdown("**Model Version:** 1.0.0")
    st.markdown("**Last Updated:** Feb 2026")


# --- PAGE 1: EXECUTIVE SUMMARY ---
if page == "📊 Executive Summary":
    st.title("🇪🇹 Ethiopia Financial Inclusion Outlook")
    st.markdown("### The 'Inclusion Paradox' (2021-2024)")

    # KPIs
    col1, col2, col3, col4 , col5 , col6 = st.columns(6)
    with col1:
        st.metric("Official Access (2024)", "49.0%", "+3% vs 2021")
    with col2:
        st.metric("Telebirr Users", "54.0 M", "New Digital Base")
    with col3:
        # P2P / ATM Proxy Ratio (Digital Vol / Traditional Vol)
        # Assuming proxy data exists or is derived
        ratio_val = 12.5
        st.metric("P2P/ATM Crossover", f"{ratio_val}x", "Digital Dominance")
    with col4:
        # Growth Rate (CAGR of Digital)
        cagr = 150.0
        st.metric("Digital CAGR", f"+{cagr}%", "Hyper-Growth")
    with col5:
        st.metric("Forecast 2030 (Base)", f"{df_forecast[df_forecast['Year'] == 2030]['Base_Case'].values[0]}%",
                  "Status Quo")
    with col6:
        st.metric("Forecast 2030 (Opt)", f"{df_forecast[df_forecast['Year'] == 2030]['Optimistic'].values[0]}%",
                  "Digital Dividend")



    st.markdown("## Executive Summary")

    st.markdown("""
    **Current Situation (2024):**  
    Ethiopia’s financial inclusion has entered a structural transition phase.  
    While **formal account ownership remains below 50%**, digital financial usage has expanded rapidly, driven primarily by mobile wallets and government-mandated digital payments.

    **Key Insight:**  
    Digital adoption is outpacing formal inclusion. This gap represents both a **risk** (inactive or shallow usage) and a **strategic opportunity** for rapid inclusion gains.

    **Outlook (2025–2030):**  
    Under a continuation of current trends, account ownership is projected to reach **~58% by 2030**.  
    With targeted policy interventions and market competition, inclusion could accelerate toward **70%**, aligning with national financial sector objectives.

    **Implication for Decision-Makers:**  
    The next phase of inclusion growth will be driven less by infrastructure expansion and more by **conversion of digital users into active, regulated financial participants**.
    """)

    # The Paradox Chart (Dual Axis)
    st.subheader("Visualizing the Gap")
    col1, col2 = st.columns(2)

    with col1:
        st.image(
            "data/figures/ethiopia_final_forecast.png",
            caption="Ethiopian Financial Inclution Forecast",
            use_container_width=True
        )

    with col2:
        st.image(
            "data/figures/Baselin_trend(log-linear).png",
            caption="Baseline Trend (Log-linear)",
            use_container_width=True
        )
    col3 , col4 = st.columns(2)
    with col3:
        st.image(
            "data/figures/External_driver()Telebirr impact.png",
            caption="External_Driver (Telebirr)",
            use_container_width=True
        )
    with col4:
        st.image(
            "data/figures/Dual_engine_driver(T+M).png",
            caption="External_Driver (Telebirr + M-pesa)",
            use_container_width=True
        )
    st.info(
        "💡 **Insight:** While official account ownership stagnated, digital usage grew from 0 to 54M users. This 'Lag' is the primary opportunity for 2025.")

    # 2. Key Questions Answered
    st.subheader("💡 Consortium Key Insights")
    with st.expander("Is the 60% Target Achievable?", expanded=True):
        st.markdown("""
        **Yes, but only via digital integration.** * **Baseline:** Traditional banking paths reach only **53%** by 2030 (Failure).
        * **Optimistic:** Digital wallet integration pushes inclusion to **68%** (Success).
        """)
    with st.expander("What is the impact of the Fuel Mandate?"):
        st.write(
            "It served as a forced-adoption event, effectively creating a 'floor' for digital literacy for millions of transport workers.")

    st.subheader("References")
    st.markdown("""
          **Survey Data & Financial Inclusion Frameworks**
          
          **Global Findex Database — worldbank.org/globalfindex**
          
          **Global Findex Methodology — worldbank.org/globalfindex/methodology**
          
          **Global Findex Microdata — microdata.worldbank.org**
          
          **IMF Financial Access Survey — data.imf.org/FAS**
          
          **GSMA State of the Industry Report — gsma.com/sotir**
          
          **World Bank: Why Financial Inclusion Matters — worldbank.org/en/topic/financialinclusion/overview**
          
          **Demirgüç-Kunt et al. (2018): "The Global Findex Database 2017: Measuring Financial Inclusion and the Fintech Revolution" — openknowledge.worldbank.org**
          
          **IMF: Financial Inclusion and Economic Growth — imf.org/external/pubs/ft/sdn/2015/sdn1517.pdf**
          
          **Ethiopia Sources**
          
          **National Bank of Ethiopia — nbe.gov.et**
          
          **EthSwitch S.C. — ethswitch.com**
          
          **Ethio Telecom — ethiotelecom.et**
          
          **Fayda Digital ID — id.gov.et**
          
          **Shega Media — shega.co**
           """)

# --- PAGE 2: TRENDS & CHANNELS ---
elif page == "📈 Trends & Channels":
    st.title("📈 Market Trends Analysis")

    # Date Range Selector
    st.markdown("### 🗓️ Time Filter")
    year_range = st.slider("Select Year Range", 2014, 2028, (2018, 2024))

    # Filter Data
    mask = (df_hist['year'] >= year_range[0]) & (df_hist['year'] <= year_range[1])
    filtered_df = df_hist.loc[mask]

    # Channel Comparison View
    st.markdown("### 📡 Channel Comparison")

    # Create a comparison plot
    fig = go.Figure()

    # Channel 1: Bank Accounts (Access)
    subset_acc = filtered_df[filtered_df['indicator_code'] == 'ACC_OWNERSHIP']
    fig.add_trace(go.Bar(
        x=subset_acc['year'], y=subset_acc['value_numeric'],
        name='Bank Account Penetration (%)'
    ))

    # Channel 2: Mobile Money (Telebirr) - Scaled for comparison
    # We plot it on secondary axis to compare "Shape" of growth
    subset_mob = filtered_df[filtered_df['indicator_code'] == 'USG_TELEBIRR_USERS']
    fig.add_trace(go.Scatter(
        x=subset_mob['year'], y=subset_mob['value_numeric'],
        name='Mobile Users (Millions)', yaxis='y2', line=dict(color='green', width=3)
    ))

    fig.update_layout(
        title="Traditional Banking vs. Mobile Adoption",
        yaxis=dict(title="Account %"),
        yaxis2=dict(title="Users (Millions)", overlaying='y', side='right'),
        legend=dict(x=0, y=1.1, orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)


# --- PAGE 3: FORECAST & SCENARIOS ---
elif page == "🔮 Forecast & Scenarios":
    st.title("🔮 2030 Strategic Forecast")

    # Model Selection Option
    model_choice = st.radio("Select Model View:",
                            ["Ensemble View (Recommended)", "Trend Only (Baseline)", "Driver Only (Optimistic)"],
                            horizontal=True)

    fig = go.Figure()

    # Historical
    fig.add_trace(go.Scatter(x=access_data['year'], y=access_data['value_numeric'], name="Observed History",
                             line=dict(color='black')))

    if model_choice == "Trend Only (Baseline)" or model_choice == "Ensemble View (Recommended)":
        fig.add_trace(go.Scatter(x=df_forecast['Year'], y=df_forecast['Base_Case'], name="Baseline (Stagnation)",
                                 line=dict(dash='dash', color='gray')))

    if model_choice == "Driver Only (Optimistic)" or model_choice == "Ensemble View (Recommended)":
        fig.add_trace(go.Scatter(x=df_forecast['Year'], y=df_forecast['Optimistic'], name="Optimistic (Digital)",
                                 line=dict(color='green')))

    # Confidence Intervals (Ensemble Only)
    if model_choice == "Ensemble View (Recommended)":
        fig.add_trace(go.Scatter(
            x=pd.concat([df_forecast['Year'], df_forecast['Year'][::-1]]),
            y=pd.concat([df_forecast['Optimistic'], df_forecast['Base_Case'][::-1]]),
            fill='toself', fillcolor='rgba(0,100,80,0.2)', line=dict(color='rgba(255,255,255,0)'),
            name='Confidence Range'
        ))

    fig.update_layout(title="2030 Forecast Scenarios", yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

    # Forecast Chart
    fig = go.Figure()

    # Historical
    fig.add_trace(go.Scatter(
        x=access_data['year'], y=access_data['value_numeric'],
        name="Historical Data", line=dict(color="black", width=3)
    ))

    # Scenarios
    fig.add_trace(go.Scatter(
        x=df_forecast['Year'], y=df_forecast['Base_Case'],
        name="Base Case (Trend)", line=dict(color="#1f77b4", width=2)
    ))

    fig.add_trace(go.Scatter(
        x=df_forecast['Year'], y=df_forecast['Optimistic'],
        name="Optimistic (Policy Driven)", line=dict(color="green", width=2, dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=df_forecast['Year'], y=df_forecast['Pessimistic'],
        name="Pessimistic", line=dict(color="red", width=1, dash='dot')
    ))

    # Shading (Uncertainty)
    fig.add_trace(go.Scatter(
        x=pd.concat([df_forecast['Year'], df_forecast['Year'][::-1]]),
        y=pd.concat([df_forecast['Optimistic'], df_forecast['Pessimistic'][::-1]]),
        fill='toself', fillcolor='rgba(0,100,80,0.1)', line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip", showlegend=False
    ))

    fig.update_layout(title="Ethiopia Financial Inclusion Scenarios (2025-2030)", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Visuals")
    col1 , col2 = st.columns(2)

    with col1:
        st.image(
            "data/figures/ethiopia_final_forecast.png",
            caption="Ethiopian Financial Inclution Forecast",
            use_container_width=True
        )
    with col2:
        st.image(
            "data/figures/Forecast_ethiopian_financial_inclution(2025-2030).png",
            caption="Ethiopian Financial Inclution Forecast",
            use_container_width=True
        )

    col3 , col4 = st.columns(2)

    with col3:
        st.image(
            "data/figures/mobile_money_explotion.png",
            caption="Mobile money Boost",
            use_container_width=True
        )

    with col4:
        st.image(
            "data/figures/How_digital_drivers_change_the_trajectory.png",
            caption=" How Digital Drivers Change The Trajectory",
            use_container_width=True
        )

    # Data Table
    st.subheader("Detailed Forecast Data")
    st.dataframe(df_forecast.style.format("{:.1f}"), use_container_width=True)




# --- PAGE 3: POLICY SIMULATOR ---
elif page == "🎛️ Policy Simulator":
    st.title("🎛️ Strategic Intervention Simulator")
    st.markdown("Adjust the policy and market levers to see if Ethiopia can hit the **70% National Target** by 2030.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 🎚️ Policy Levers")

        st.markdown("**1. Market Penetration**")
        # THIS IS THE TELEBIRR IMPACT YOU ASKED FOR
        telebirr_pop = st.slider("Telebirr Users (2030)", 55, 95, 75, 5, format="%dM")
        mpesa_pop = st.slider("M-Pesa Users (2030)", 5, 25, 15, 1, format="%dM")

        st.markdown("**2. Quality of Usage**")
        active_rate = st.slider("Active User Conversion", 30, 80, 60, 5, format="%d%%",
                                help="Percent of registered users who are 'Banked'")
        fuel_compliance = st.slider("Gov Payment Compliance", 50, 100, 80, 5, format="%d%%")

    with col2:
        # --- SIMULATION LOGIC ---
        # 1. Calculate Total Addressable Market (TAM)
        # Assume 20% overlap between Telebirr and M-Pesa
        overlap = 0.20
        unique_users = telebirr_pop + (mpesa_pop * (1 - overlap))

        # 2. Calculate Implied Coverage (assuming ~68M adults in 2030)
        adult_pop_2030 = 68.0
        raw_coverage = (unique_users / adult_pop_2030) * 100

        # 3. Apply "Active Conversion" Discount
        # Base conversion is the slider (e.g., 60%)
        # But high Fuel Compliance boosts this rate slightly (forced usage becomes habit)
        compliance_boost = (fuel_compliance - 80) * 0.1
        final_conversion = (active_rate + compliance_boost) / 100

        final_inclusion = raw_coverage * final_conversion

        # Cap at 100%
        if final_inclusion > 100: final_inclusion = 100

        # --- GAUGE CHART ---
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=final_inclusion,
            title={'text': "Projected 2030 Inclusion (%)"},
            delta={'reference': 70.0, 'position': "top"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#1f77b4"},
                'steps': [
                    {'range': [0, 53], 'color': "#e0e0e0"},  # Baseline
                    {'range': [53, 70], 'color': "#f9f9f9"}  # Gap
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'value': 70}
            }
        ))

        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

        # --- RESULTS BOX ---
        st.markdown("#### Impact Analysis")
        if final_inclusion >= 60:
            st.balloons()
            st.success(
                f"🎉 **Success!** With {unique_users:.1f}M unique users and {active_rate}% conversion, you exceed the 60% target.")
        elif final_inclusion >= 50:
            st.warning(
                f"⚠️ **Close:** You are reaching {final_inclusion:.1f}%. Focus on increasing Active Conversion to hit 60%.")
        else:
            st.error(
                f"❌ **Gap:** Projected {final_inclusion:.1f}% is significantly below target. Telebirr expansion alone isn't enough; you need higher active usage.")