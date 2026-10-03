import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fulfillment Hub",
    page_icon="📦",
    layout="wide"
)

# -----------------------------
# Professional Dashboard Styling
# -----------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #eef3f8;
    }

    .main {
        background: #eef3f8;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #172033;
    	border-right: 1px solid #24334a;
    }

    [data-testid="stSidebar"] * {
        color: #e8eef7;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff;
    }

    /* Main headings */
    h1 {
        color: #172033;
        font-weight: 700;
    }

    h2, h3 {
        color: #263449;
        font-weight: 650;
    }

    /* KPI cards */
    [data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #dfe7f0;
    border-left: 5px solid #4f8cff;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(23, 32, 51, 0.07);
    min-height: 105px;
   }

    [data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 500;
    }

    [data-testid="stMetricValue"] {
        color: #172033;
        font-weight: 750;
	font-size: 28px;
    }

    /* Data tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #dfe7f0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 3px 12px rgba(23, 32, 51, 0.04);
    }

    /* Info / warning / success boxes */
    .stAlert {
        border-radius: 12px;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        border-radius: 8px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Dividers */
    hr {
        border-color: #dbe4ee;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Dashboard Header
# -----------------------------


# -----------------------------
# Dashboard Header
# -----------------------------

st.markdown("""
<div style="
background: linear-gradient(135deg, #dcecff 0%, #f7fbff 55%, #d8e8f7 100%);
border: 1px solid #d7e4f0;
border-radius: 16px;
padding: 30px 35px;
margin-bottom: 25px;
box-shadow: 0 6px 20px rgba(23,32,51,0.08);
">

<div style="
color: #2563c7;
font-size: 13px;
font-weight: 700;
letter-spacing: 1px;
margin-bottom: 8px;
">
OPERATIONS CONTROL CENTER
</div>

<div style="
color: #172033;
font-size: 36px;
font-weight: 750;
margin-bottom: 8px;
">
📦 Fulfillment Hub
</div>

<div style="
color: #52637a;
font-size: 15px;
line-height: 1.5;
">
Monitor orders, inventory, dispatch and operational exceptions in one place.
</div>

<div style="
display: inline-block;
margin-top: 16px;
background: #ffffff;
border: 1px solid #d8e3ef;
border-radius: 20px;
padding: 7px 13px;
color: #2563c7;
font-size: 12px;
font-weight: 600;
">
● System Online
</div>

</div>
""", unsafe_allow_html=True)


# -----------------------------
# Load data
# -----------------------------

orders = pd.read_csv("data/orders.csv")
products = pd.read_csv("data/products.csv")
inventory = pd.read_csv("data/inventory.csv")
couriers = pd.read_csv("data/couriers.csv")
issues = pd.read_csv("data/issues.csv")


# -----------------------------
# Dashboard calculations
# -----------------------------

total_orders = len(orders)

priority_orders = len(
    orders[orders["priority"].isin(["High", "Priority"])]
)

delayed_orders = len(
    issues[issues["issue_type"] == "Order Delay"]
)

# Inventory alert calculation
inventory_check = inventory.merge(
    products[["product_id", "reorder_level"]],
    on="product_id",
    how="left"
)

inventory_check["available_stock"] = (
    inventory_check["main_warehouse"]
    - inventory_check["reserved_stock"]
)

inventory_alerts = inventory_check[
    inventory_check["available_stock"] < inventory_check["reorder_level"]
]

stock_alerts = len(inventory_alerts)

open_issues = len(
    issues[issues["status"] != "Resolved"]
)
# Courier pickup risk
staged_orders = orders[
    orders["status"] == "Staged"
]

pending_pickups = len(staged_orders)

priority_staged = len(
    staged_orders[
        staged_orders["priority"].isin(["High", "Priority"])
    ]
)

# Inventory alert calculation
inventory_check = inventory.merge(
    products[["product_id", "reorder_level"]],
    on="product_id",
    how="left"
)

inventory_check["available_stock"] = (
    inventory_check["main_warehouse"]
    - inventory_check["reserved_stock"]
)

inventory_alerts = inventory_check[
    inventory_check["available_stock"] < inventory_check["reorder_level"]
]


# -----------------------------
# Dashboard
# -----------------------------

st.divider()

st.subheader("📊 Today's Fulfillment Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📦 Total Orders",
        total_orders
    )

with col2:
    st.metric(
        "🔴 Priority Orders",
        priority_orders
    )

with col3:
    st.metric(
        "⚠️ Delayed Orders",
        delayed_orders
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("📉 Stock Alerts", stock_alerts)

with col5:
    st.metric("⚠️ Open Issues", open_issues)

with col6:
    st.metric("🚚 Pending Pickups", pending_pickups)


st.divider()

st.markdown("""
<div style="
background: #f8fbff;
border: 1px solid #d8e6f5;
border-left: 5px solid #4f8cff;
border-radius: 12px;
padding: 14px 18px;
margin: 8px 0 22px 0;
color: #52637a;
font-size: 14px;
">
<b style="color: #263449;">Operational Overview</b><br>
Use this dashboard to identify priority orders, fulfillment delays,
inventory risks and unresolved operational issues.
</div>
""", unsafe_allow_html=True)

st.subheader("Fulfillment Pipeline")

status_order = [
    "New",
    "Processing",
    "Picking",
    "Packing",
    "Staged",
    "Shipped",
    "Delivered"
]

pipeline_cols = st.columns(len(status_order))

for col, status in zip(pipeline_cols, status_order):
    count = len(orders[orders["status"] == status])

    with col:
        st.metric(label = status, value = count)

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("⚠️ Needs Attention")

    st.caption(
        "Priority orders and active delays requiring attention."
    )

    attention_orders = orders[
        (orders["priority"].isin(["High", "Priority"])) |
        (orders["order_id"].isin(
            issues[issues["issue_type"] == "Order Delay"]["order_id"]
        ))
    ]

    st.dataframe(
        attention_orders[
            [
                "order_id",
                "priority",
                "ship_deadline",
                "status"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


with col2:

    st.subheader("📦 Inventory Alerts")

    st.caption(
        "Products below their reorder level."
    )

    if len(inventory_alerts) > 0:

        st.dataframe(
            inventory_alerts[
                [
                    "product_id",
                    "product_name",
                    "variant",
                    "available_stock",
                    "reorder_level"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success("No inventory alerts.")

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("🚚 Upcoming Courier Pickups")

    st.caption(
        "Packed orders waiting for courier pickup."
    )

    pickup_orders = orders[
        orders["status"].isin(["Staged", "Packing"])
    ]

    st.dataframe(
        pickup_orders[
            [
                "order_id",
                "status",
                "courier",
                "ship_deadline"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


with col2:

    st.subheader("⚠️ Open Operational Issues")

    st.caption(
        "Issues that still require action."
    )

    open_issue_data = issues[
        issues["status"] != "Resolved"
    ]

    if len(open_issue_data) > 0:

        st.dataframe(
            open_issue_data[
                [
                    "issue_id",
                    "order_id",
                    "issue_type",
                    "priority",
                    "status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success("No open operational issues.")

st.divider()

st.subheader("📦 Inventory Health")

healthy_count = len(
    inventory_check[
        inventory_check["available_stock"] >= inventory_check["reorder_level"]
    ]
)

low_stock_count = len(
    inventory_check[
        (inventory_check["available_stock"] < inventory_check["reorder_level"]) &
        (inventory_check["available_stock"] > 0)
    ]
)

transfer_count = len(
    inventory_check[
        (inventory_check["available_stock"] <= 0) &
        (inventory_check["secondary_warehouse"] > 0)
    ]
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🟢 Healthy", healthy_count)

with col2:
    st.metric("🟡 Low Stock", low_stock_count)

with col3:
    st.metric("🔴 Transfer Required", transfer_count)

st.divider()

inventory_health = inventory_check[
    [
        "product_id",
        "product_name",
        "variant",
        "available_stock",
        "reorder_level"
    ]
].copy()

inventory_health["Status"] = inventory_health.apply(
    lambda row:
        "🔴 Transfer Required"
        if row["available_stock"] <= 0
        else "🟡 Low Stock"
        if row["available_stock"] < row["reorder_level"]
        else "🟢 Healthy",
    axis=1
)

st.dataframe(
    inventory_health,
    use_container_width=True,
    hide_index=True
)

st.caption(
    f"Last inventory data check: {inventory['last_stock_check'].max()}"
)