import streamlit as st
import pandas as pd
import numpy as np

# Sample Data for Evaluation
data = {
    'Startup': ['Fintech A', 'Fintech B', 'Fintech C'],
    'ARR (Annual Recurring Revenue)': [500000, 1200000, 800000],
    'CAC (Customer Acquisition Cost)': [100, 250, 150],
    'LTV (Lifetime Value)': [1000, 1500, 1200],
    'Churn Rate (%)': [5, 3, 7],
    'Team Score (1-10)': [8, 9, 7],
    'Market Opportunity (1-10)': [9, 8, 8],
    'Burn Rate ($)': [30000, 50000, 40000],
}

# Create DataFrame
df = pd.DataFrame(data)

# Default weights
weights = {
    'ARR (Annual Recurring Revenue)': 0.3,
    'CAC (Customer Acquisition Cost)': 0.1,
    'LTV (Lifetime Value)': 0.2,
    'Churn Rate (%)': -0.2,
    'Team Score (1-10)': 0.2,
    'Market Opportunity (1-10)': 0.1,
}

# Streamlit Configuration
st.set_page_config(page_title="Startup Evaluation v2", layout="wide", page_icon="🚀")

# Title and Sidebar
st.title("🚀 Startup Evaluation Dashboard")
st.sidebar.header("Adjust Weights & Edit Data")

# Sidebar: Adjust Weights
st.sidebar.subheader("Adjust Weights")
for key in weights.keys():
    weights[key] = st.sidebar.slider(f"Weight: {key}", -1.0, 1.0, weights[key], 0.1)

# Sidebar: Edit or Add New Startup
st.sidebar.subheader("Edit or Add New Startup")
new_startup_name = st.sidebar.text_input("Startup Name")
new_arr = st.sidebar.number_input("ARR (Annual Recurring Revenue)", min_value=0, step=1000)
new_cac = st.sidebar.number_input("CAC (Customer Acquisition Cost)", min_value=0, step=1)
new_ltv = st.sidebar.number_input("LTV (Lifetime Value)", min_value=0, step=10)
new_churn_rate = st.sidebar.number_input("Churn Rate (%)", min_value=0, max_value=100, step=1)
new_team_score = st.sidebar.slider("Team Score (1-10)", min_value=1, max_value=10, step=1)
new_market_opportunity = st.sidebar.slider("Market Opportunity (1-10)", min_value=1, max_value=10, step=1)
new_burn_rate = st.sidebar.number_input("Burn Rate ($)", min_value=0, step=1000)

# Add/Edit Startup Button
if st.sidebar.button("Add or Edit Startup"):
    if new_startup_name.strip():
        if new_startup_name in df['Startup'].values:
            df.loc[df['Startup'] == new_startup_name, :] = [
                new_startup_name, new_arr, new_cac, new_ltv, new_churn_rate,
                new_team_score, new_market_opportunity, new_burn_rate
            ]
            st.sidebar.success(f"Updated startup: {new_startup_name}")
        else:
            new_row = {
                'Startup': new_startup_name,
                'ARR (Annual Recurring Revenue)': new_arr,
                'CAC (Customer Acquisition Cost)': new_cac,
                'LTV (Lifetime Value)': new_ltv,
                'Churn Rate (%)': new_churn_rate,
                'Team Score (1-10)': new_team_score,
                'Market Opportunity (1-10)': new_market_opportunity,
                'Burn Rate ($)': new_burn_rate,
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            st.sidebar.success(f"Added new startup: {new_startup_name}")
    else:
        st.sidebar.error("Startup name cannot be empty!")

# Normalize Data
df_normalized = df.copy()
for col in weights.keys():
    if weights[col] > 0:
        df_normalized[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    else:
        df_normalized[col] = (df[col].max() - df[col]) / (df[col].max() - df[col].min())

# Calculate Scores
df['Score'] = sum(weights[col] * df_normalized[col] for col in weights.keys())
df['Score'] = df['Score'].round(2)  # Keep only 2 decimals
df = df.sort_values('Score', ascending=False)

# Display Scores
st.subheader("🏆 Startup Scores")
st.dataframe(df[['Startup', 'Score']])

# Bar Chart for Scores
st.subheader("Scores Overview")
st.bar_chart(df.set_index('Startup')['Score'])

# Scenario Planning Section
st.subheader("📈 Scenario Planning")
selected_startup = st.selectbox("Select a Startup", df['Startup'])
growth_rate = st.slider("Revenue Growth Rate (%)", -50, 200, 20)

# Calculate ARR Scenarios
startup_data = df[df['Startup'] == selected_startup].iloc[0]
initial_revenue = startup_data['ARR (Annual Recurring Revenue)']
scenario_revenues = {
    "Year 1": initial_revenue,
    "Year 2": initial_revenue * (1 + growth_rate / 100),
    "Year 3": initial_revenue * ((1 + growth_rate / 100) ** 2),
    "Year 4": initial_revenue * ((1 + growth_rate / 100) ** 3),
}
scenario_df = pd.DataFrame(list(scenario_revenues.items()), columns=["Year", "Revenue"])

# Display Scenario Chart with Y-axis labeled
st.line_chart(scenario_df.set_index("Year"), height=400, use_container_width=True)
st.caption(f"Projected ARR ($) for {selected_startup}")

# Interpretation Section
if st.button("What Does the Score Mean?"):
    st.write("""
    ### Score Interpretation:
    - **High Score**: Indicates strong KPIs aligned with benchmarks and weights.
    - **Investment Decision**: Higher scores reflect startups that are likely better investments.
    - Use qualitative insights to supplement scores for final decisions.
    """)

# Questionnaire for KPIs
st.subheader("📝 Scoring Assistance")
st.write("""
### Team Score:
1. Evaluate team cohesion and leadership effectiveness (1-10).
2. Rate team experience and ability to execute projects (1-10).

### Market Opportunity:
1. Assess the market's size and growth potential (1-10).
2. Analyze the competitive landscape and market accessibility (1-10).
""")

# Footer
st.write("🚀 **Explore and evaluate startups dynamically with this enhanced dashboard!**")
