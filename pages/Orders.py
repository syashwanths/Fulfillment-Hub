import streamlit as st
import pandas as pd
from utils.styles import apply_styles

st.set_page_config(page_title="Orders", page_icon="📋", layout="wide")
apply_styles()

# Load orders
orders = pd.read_csv("data/orders.csv")

st.title("📋 Orders")
st.caption("View and monitor all fulfillment orders")

st.divider()

# Filters
col1, col2 = st.columns(2)

with col1:
    status_filter = st.selectbox(
        "Filter by Status",
        ["All"] + sorted(orders["status"].unique().tolist())
    )

with col2:
    priority_filter = st.selectbox(
        "Filter by Priority",
        ["All"] + sorted(orders["priority"].unique().tolist())
    )

# Apply filters
filtered_orders = orders.copy()

if status_filter != "All":
    filtered_orders = filtered_orders[
        filtered_orders["status"] == status_filter
    ]

if priority_filter != "All":
    filtered_orders = filtered_orders[
        filtered_orders["priority"] == priority_filter
    ]
priority_count = len(
    filtered_orders[
        filtered_orders["priority"].isin(["High", "Priority"])
    ]
)

processing_count = len(
    filtered_orders[
        filtered_orders["status"].isin(
            ["New", "Processing", "Picking", "Packing"]
        )
    ]
)

dispatch_count = len(
    filtered_orders[
        filtered_orders["status"].isin(
            ["Staged"]
        )
    ]
)

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric("🔴 Priority Orders", priority_count)

with metric2:
    st.metric("📦 In Fulfillment", processing_count)

with metric3:
    st.metric("🚚 Ready for Dispatch", dispatch_count)

st.subheader("Order Status Summary")

status_counts = filtered_orders["status"].value_counts()

summary_cols = st.columns(len(status_counts))

for col, (status, count) in zip(summary_cols, status_counts.items()):
    with col:
        st.metric(status, count)

st.subheader(f"Orders ({len(filtered_orders)})")

display_orders = filtered_orders.copy()

display_orders["Attention"] = display_orders.apply(
    lambda row:
        "🔴 Priority"
        if row["priority"] in ["High", "Priority"]
        else "🟡 In Fulfillment"
        if row["status"] in ["New", "Processing", "Picking", "Packing"]
        else "🟢 On Track",
    axis=1
)

st.dataframe(
    display_orders[
        ["order_id", "customer", "product", "variant", "quantity",
         "priority", "order_time", "ship_deadline", "status",
         "courier", "Attention"]
    ],
    use_container_width=True,
    hide_index=True
)