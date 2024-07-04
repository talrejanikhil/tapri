from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


# Function to calculate sales projections
def calculate_projections(startup_expenses, monthly_fixed_expenses, monthly_operational_costs, monthly_sales, months):
    total_expenses = np.zeros(months)
    total_sales = np.zeros(months)
    cumulative_expenses = startup_expenses
    cumulative_sales = 0

    for month in range(months):
        cumulative_expenses += (monthly_fixed_expenses + monthly_operational_costs)
        cumulative_sales += monthly_sales
        total_expenses[month] = cumulative_expenses
        total_sales[month] = cumulative_sales

    return total_expenses, total_sales


# Streamlit App
st.set_page_config(layout="wide")

st.title('Sales Projections and Break-Even Analysis (€)')

# Inputs
with st.sidebar:
    startup_expenses = st.slider('Startup Expenses (€)', 0, 200000, 100000, 1000)
    monthly_fixed_expenses = st.slider('Monthly Fixed Expenses (€)', 0, 20000, 5000, 1000)
    monthly_operational_costs = st.slider('Monthly Operational Costs (€)', 0, 20000, 5000, 1000)
    monthly_sales = st.slider('Monthly Sales (€)', 0, 50000, 20000, 1000)
    months = st.slider('Number of Months to Forecast', 1, 60, 24, 1)

# Calculate projections
total_expenses, total_sales = calculate_projections(startup_expenses, monthly_fixed_expenses, monthly_operational_costs,
                                                    monthly_sales, months)

# Find break-even point
break_even_month = next((i for i, (expense, sales) in enumerate(zip(total_expenses, total_sales)) if sales >= expense),
                        None)

# Create a DataFrame for visualization
start_date = datetime(2024, 11, 1)  # Start date set to November 2024
dates = [start_date + timedelta(days=30 * i) for i in range(months)]
date_labels = [date.strftime('%b %Y') for date in dates]

data = pd.DataFrame({
    'Date': date_labels,
    'Total Expenses': total_expenses,
    'Total Sales': total_sales
})

# Plotting
st.subheader('Sales Projections Over Time')
fig, ax = plt.subplots(figsize=(12, 6))  # Adjust the figure size for better fit
ax.plot(data['Date'], data['Total Expenses'], label='Total Expenses', color='#FF6F61', linewidth=2)
ax.plot(data['Date'], data['Total Sales'], label='Total Sales', color='#6FA1FF', linewidth=2)

if break_even_month is not None:
    break_even_date = date_labels[break_even_month]
    ax.axvline(x=break_even_date, color='blue', linestyle='--', label='Break-Even Point')
    st.text(f'Break-Even Point: {break_even_date}')

ax.set_xlabel('Date')
ax.set_ylabel('Amount (€)')
ax.legend()
plt.xticks(rotation=90)
plt.tight_layout()

st.pyplot(fig)
