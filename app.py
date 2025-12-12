
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data (replace with your actual filtering logic as needed)
@st.cache_data
def load_data():
	df = pd.read_csv('urbanmart_sales.csv', parse_dates=['date'])
	return df

df = load_data()
df_filtered = df.copy()  # Replace with actual filtering logic if needed

# Revenue by Category
if 'product_category' in df_filtered.columns:
	rev_by_cat = df_filtered.groupby('product_category')['line_revenue'].sum().reset_index().sort_values('line_revenue', ascending=False)
	st.subheader("Revenue by Category")
	fig_cat = px.bar(rev_by_cat, x='product_category', y='line_revenue', labels={'line_revenue':'Revenue', 'product_category':'Category'}, title='Revenue by Product Category')
	st.plotly_chart(fig_cat, use_container_width=True)

# Revenue by Store
if 'store_location' in df_filtered.columns:
	rev_by_store = df_filtered.groupby('store_location')['line_revenue'].sum().reset_index().sort_values('line_revenue', ascending=False)
	st.subheader("Revenue by Store")
	fig_store = px.bar(rev_by_store, x='store_location', y='line_revenue', labels={'line_revenue':'Revenue', 'store_location':'Store Location'}, title='Revenue by Store')
	st.plotly_chart(fig_store, use_container_width=True)

# Daily Trend
if 'date' in df_filtered.columns:
	daily = df_filtered.groupby(df_filtered['date'].dt.date)['line_revenue'].sum().reset_index()
	daily.columns = ['date', 'revenue']
	st.subheader("Daily Revenue Trend")
	fig_daily = px.line(daily, x='date', y='revenue', title='Daily Revenue')
	st.plotly_chart(fig_daily, use_container_width=True)

# Top Products & Top Customers
cols = st.columns(2)
with cols[0]:
	st.subheader("Top 5 Products by Revenue")
	if 'product_name' in df_filtered.columns:
		top_products = df_filtered.groupby('product_name')['line_revenue'].sum().sort_values(ascending=False).head(5).reset_index()
		st.table(top_products)
	elif 'product_id' in df_filtered.columns:
		top_products = df_filtered.groupby('product_id')['line_revenue'].sum().sort_values(ascending=False).head(5).reset_index()
		st.table(top_products)
	else:
		st.write("No product column found.")

with cols[1]:
	st.subheader("Top 5 Customers by Revenue")
	if 'customer_id' in df_filtered.columns:
		top_customers = df_filtered.groupby('customer_id')['line_revenue'].sum().sort_values(ascending=False).head(5).reset_index()
		st.table(top_customers)
	else:
		st.write("No customer_id column found.")

st.markdown("---")

# Raw data sample
st.subheader("Sample of Filtered Raw Data")
if not df_filtered.empty:
	st.dataframe(df_filtered.head(20))
else:
	st.write("No data available for the selected filters.")

# Reflection questions (show to students)
st.sidebar.markdown("---")
st.sidebar.header("Reflection Questions")
st.sidebar.markdown(
	"1. Which store location generates the highest revenue overall?\n"
	"2. Does online or in-store channel generate more revenue in your filtered view?\n"
	"3. Which 3 product categories contribute the most revenue?\n"
	"4. What additional filter/feature would you add to make this dashboard more useful for management?"
)