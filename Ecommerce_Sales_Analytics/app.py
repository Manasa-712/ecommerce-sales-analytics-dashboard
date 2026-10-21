import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv("ecommerce_sales_analytics_5000.csv")
df['order_date'] = pd.to_datetime(df['order_date'])
st.subheader("🔎 Filter Sales by Region")    #filter sales by Region

selected_region = st.selectbox(
    "Select Region",
    ["All Regions"] + sorted(df["region"].unique().tolist()),
    key="region_filter"
)

st.subheader("🛍️ Filter by Product Category") #filter sales by Product Category

selected_category = st.selectbox(
    "Select Category",
    ["All Categories"] + sorted(df["product_category"].unique().tolist())
)

if selected_category != "All Categories":
    df = df[df["product_category"] == selected_category]


if selected_region != "All Regions":
    df = df[df["region"] == selected_region]
st.title("📊 E-Commerce Sales Analytics")
st.caption("Track revenue, orders, customers, and sales performance.")

st.write("Welcome to the E-Commerce Sales Analytics Dashboard")

total_revenue = df['revenue'].sum()
total_orders = df['order_id'].nunique()
total_customers = df['customer_id'].nunique()
avg_rating = df['customer_rating'].mean()


st.subheader("📈 Business Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="background:#30245B;padding:20px;border-radius:12px;border-top:4px solid #A78BFA;">
        <p style="color:#C4B5FD;margin:0;">Total Revenue</p>
        <h2 style="color:white;margin:8px 0 0;">₹{:,.2f}</h2>
    </div>
    """.format(total_revenue), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:#17365C;padding:20px;border-radius:12px;border-top:4px solid #60A5FA;">
        <p style="color:#93C5FD;margin:0;">Total Orders</p>
        <h2 style="color:white;margin:8px 0 0;">{:,}</h2>
    </div>
    """.format(total_orders), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background:#12463E;padding:20px;border-radius:12px;border-top:4px solid #34D399;">
        <p style="color:#6EE7B7;margin:0;">Total Customers</p>
        <h2 style="color:white;margin:8px 0 0;">{:,}</h2>
    </div>
    """.format(total_customers), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="background:#59371B;padding:20px;border-radius:12px;border-top:4px solid #FBBF24;">
        <p style="color:#FCD34D;margin:0;">Average Rating</p>
        <h2 style="color:white;margin:8px 0 0;">{:.2f}</h2>
    </div>
    """.format(avg_rating), unsafe_allow_html=True)
st.write("")
st.subheader("📈 Monthly Revenue Trend")
monthly_revenue = df.groupby(
df['order_date'].dt.to_period('M')
)['revenue'].sum()
monthly_revenue.index = monthly_revenue.index.astype(str)
st.line_chart(monthly_revenue)

#st.subheader("🚚 Average Delivery Days by Region")
#delivery_time = df.groupby("region")["delivery_days"].mean()
#st.bar_chart(delivery_time)
st.subheader("🚚 Average Delivery Days by Region")

delivery_time = df.groupby("region")["delivery_days"].mean().reset_index()
delivery_time.columns = ["Region", "Average Delivery Days"]

fig = px.bar(
    delivery_time,
    x="Region",
    y="Average Delivery Days",
    color="Region",
    color_discrete_sequence=["#A791E7", "#1059B3", "#34D399", "#DEA71D"],
    template="plotly_dark"
)

fig.update_layout(
    showlegend=False,
    bargap=0.5
)
fig.update_yaxes(tickformat=".1f", rangemode="tozero")
fig.update_layout(height=400)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏆 Top 5 Orders by Revenue")
top_orders = df.nlargest(5, "revenue")

st.dataframe(top_orders[["order_id", "product_category", "region", "revenue"]])

st.subheader("💡 Business Insights")

best_category = df.groupby("product_category")["revenue"].sum().idxmax()

if selected_region == "All Regions":
    best_region = df.groupby("region")["revenue"].sum().idxmax()
else:
    best_region = selected_region


region_revenue = df.groupby("region")["revenue"].sum()
st.write(region_revenue.sort_values(ascending=False))
st.write("Top Revenue Category:", best_category)
st.write("Top Revenue Region:", best_region)


st.subheader("📥 Download Filtered Data")

csv_data = df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)