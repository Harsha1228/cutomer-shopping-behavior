import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# PAGE CONFIG

st.set_page_config(
page_title="Customer Shopping Behavior Dashboard",
layout="wide"
)

# AUTO REFRESH EVERY 30 SECONDS

st_autorefresh(
interval=30000,
key="customer_dashboard_refresh"
)

# DATABASE CONNECTION

@st.cache_data(ttl=30)
def load_data():
    engine = create_engine(
        "postgresql://postgres:{DB_PASSWORD}@localhost:5432/customer_behavior"
    )

    query = """
    SELECT *
    FROM customer
    """

    df = pd.read_sql(query, engine)

    return df


df = load_data()

# TITLE

st.title("Customer Shopping Behavior Dashboard")

st.sidebar.success(
f"Last Updated: {datetime.now().strftime('%H:%M:%S')}"
)

# SIDEBAR FILTERS

st.sidebar.header("Filters")

gender_filter = st.sidebar.selectbox(
"Select Gender",
["All"] + list(df["gender"].dropna().unique())
)

category_filter = st.sidebar.selectbox(
"Select Category",
["All"] + list(df["category"].dropna().unique())
)

if gender_filter != "All":
    df = df[df["gender"] == gender_filter]

if category_filter != "All":
    df = df[df["category"] == category_filter]

# KPI CARDS

total_customers = len(df)
total_sales = df["purchase_amount"].sum()
avg_purchase = df["purchase_amount"].mean()

col1, col2, col3 = st.columns(3)

col1.metric(
"Total Customers",
total_customers
)

col2.metric(
"Total Sales",
f"${total_sales:,.0f}"
)

col3.metric(
"Average Purchase",
f"${avg_purchase:.2f}"
)

# DATASET PREVIEW

st.subheader("Dataset Preview")

st.dataframe(df.head())

# SUMMARY STATISTICS

st.subheader("Summary Statistics")

st.write(df.describe())

# GENDER DISTRIBUTION

st.subheader("Gender Distribution")

fig = px.pie(
df,
names="gender",
title="Gender Distribution"
)

st.plotly_chart(
fig,
use_container_width=True
)

# AGE DISTRIBUTION

st.subheader("Age Distribution")

fig = px.histogram(
df,
x="age",
nbins=20,
title="Age Distribution"
)

st.plotly_chart(
fig,
use_container_width=True
)

# PURCHASE AMOUNT DISTRIBUTION

st.subheader("Purchase Amount Distribution")

fig = px.histogram(
df,
x="purchase_amount",
nbins=25,
title="Purchase Amount Distribution"
)

st.plotly_chart(
fig,
use_container_width=True
)

# REVIEW RATING DISTRIBUTION

if "review_rating" in df.columns:
    st.subheader("Review Rating Distribution")

fig = px.histogram(
    df,
    x="review_rating",
    nbins=10,
    title="Review Rating Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# PREVIOUS PURCHASES DISTRIBUTION

if "previous_purchases" in df.columns:
    st.subheader("Previous Purchases Distribution")

fig = px.histogram(
    df,
    x="previous_purchases",
    nbins=20,
    title="Previous Purchases Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# SALES BY CATEGORY

st.subheader("Sales by Category")

category_sales = (
df.groupby("category")["purchase_amount"]
.sum()
.reset_index()
)

fig = px.bar(
category_sales,
x="category",
y="purchase_amount",
title="Sales by Category"
)

st.plotly_chart(
fig,
use_container_width=True
)

# SALES BY LOCATION

st.subheader("Sales by Location")

location_sales = (
df.groupby("location")["purchase_amount"]
.sum()
.reset_index()
)

fig = px.bar(
location_sales,
x="location",
y="purchase_amount",
title="Sales by Location"
)

st.plotly_chart(
fig,
use_container_width=True
)

# TOP 10 PURCHASED PRODUCTS

st.subheader("Top 10 Purchased Products")

product_counts = (
df["item_purchased"]
.value_counts()
.reset_index()
)

product_counts.columns = [
"item_purchased",
"count"
]

fig = px.bar(
product_counts.head(10),
x="item_purchased",
y="count",
title="Top 10 Purchased Products"
)

st.plotly_chart(
fig,
use_container_width=True
)

# PURCHASE AMOUNT BY GENDER

st.subheader("Purchase Amount by Gender")

gender_sales = (
df.groupby("gender")["purchase_amount"]
.sum()
.reset_index()
)

fig = px.bar(
gender_sales,
x="gender",
y="purchase_amount",
title="Purchase Amount by Gender"
)

st.plotly_chart(
fig,
use_container_width=True
)

# AGE VS PURCHASE AMOUNT

st.subheader("Age vs Purchase Amount")

fig = px.scatter(
df,
x="age",
y="purchase_amount",
color="gender",
title="Age vs Purchase Amount"
)

st.plotly_chart(
fig,
use_container_width=True
)
