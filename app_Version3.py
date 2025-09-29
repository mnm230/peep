import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Expenses Calculator", layout="wide")

st.title("💰 Expenses Calculator")

st.sidebar.header("Your Financial Inputs")

annual_income_gbp = st.sidebar.number_input("Annual Income (GBP)", value=28000, min_value=0)
savings_usd = st.sidebar.number_input("Current Savings (USD)", value=10000, min_value=0)
october_spending_usd = st.sidebar.number_input("October Spending (USD)", value=45000, min_value=0)
exchange_rate = st.sidebar.number_input("GBP to USD Exchange Rate", value=1.34, min_value=0.0)
future_monthly_spending = st.sidebar.number_input("Future Monthly Spending (USD)", value=3000, min_value=0)
additional_income = st.sidebar.number_input("Additional Monthly Income (USD)", value=0, min_value=0)

monthly_income_usd = (annual_income_gbp / 12) * exchange_rate
total_available = monthly_income_usd + savings_usd
october_shortfall = max(0, october_spending_usd - total_available)
remaining_after_october = max(0, total_available - october_spending_usd)

total_monthly_income = monthly_income_usd + additional_income
monthly_surplus = total_monthly_income - future_monthly_spending
months_to_recover = int(np.ceil(october_shortfall / monthly_surplus)) if monthly_surplus > 0 else None
max_sustainable_spending = total_monthly_income

st.markdown(f"### Monthly Income (USD): **${monthly_income_usd:,.2f}** (+ ${additional_income:,.2f} additional)")

if october_shortfall > 0:
    st.error(f"October Shortfall: **${october_shortfall:,.2f}** – You need to find this amount from other sources.")
else:
    st.success(f"Remaining After October: **${remaining_after_october:,.2f}** – You have this much left after October expenses.")

if monthly_surplus > 0:
    st.success(f"Monthly Surplus: **${monthly_surplus:,.2f}**")
else:
    st.warning(f"Monthly Deficit: **${monthly_surplus:,.2f}**")

if months_to_recover is None:
    st.warning("Unable to recover shortfall with current income/spending. Increase income or reduce spending.")
else:
    st.info(f"Time to recover from October shortfall: **{months_to_recover} months**")

st.markdown(f"Maximum sustainable monthly spending: **${max_sustainable_spending:,.2f}**")

# Recovery Timeline Chart
months = np.arange(0, 25)
cumulative_balance = -october_shortfall + np.maximum(months, 0) * monthly_surplus

timeline_df = pd.DataFrame({
    "Month": ["Oct"] + [str(m) for m in months[1:]],
    "Cumulative Balance": cumulative_balance
})

fig = px.line(timeline_df, x="Month", y="Cumulative Balance", title="Recovery Timeline (24 Months)",
              labels={"Cumulative Balance": "USD"})
st.plotly_chart(fig, use_container_width=True)

# Income vs Spending Bar Chart
comparison_df = pd.DataFrame({
    "Category": ["Monthly Income", "Monthly Spending", "October Spending"],
    "Amount": [total_monthly_income, future_monthly_spending, october_spending_usd]
})
fig2 = px.bar(comparison_df, x="Category", y="Amount", color="Category", title="Income vs Spending Comparison")
st.plotly_chart(fig2, use_container_width=True)

# Budget Breakdown Pie Chart
pie_df = pd.DataFrame({
    "Type": ["Regular Income", "Additional Income", "Monthly Spending"],
    "Value": [monthly_income_usd, additional_income, future_monthly_spending]
})
pie_df = pie_df[pie_df["Value"] > 0]
fig3 = px.pie(pie_df, names="Type", values="Value", title="Monthly Budget Breakdown", hole=0.4)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.caption("Expenses Calculator • Built with Streamlit & Plotly • Deploy on Streamlit Cloud or HuggingFace Spaces")