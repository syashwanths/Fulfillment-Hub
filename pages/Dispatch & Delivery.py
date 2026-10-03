import streamlit as st
import pandas as pd
from utils.styles import apply_styles

st.set_page_config(
    page_title="Dispatch & Delivery",
    page_icon="🚚",
    layout="wide"
)

apply_styles()

# Load data
orders = pd.read_csv("data/orders.csv")
couriers = pd.read_csv("data/couriers.csv")

# -----------------------------
# Header
# -----------------------------
st.title("🚚 Dispatch & Delivery")
st.caption("Monitor packed orders, courier pickup and delivery")
st.divider()

# -----------------------------
# Dispatch Metrics
# -----------------------------
dispatch_orders = orders[
    orders["status"].isin(["Packing", "Staged"])
]

staged_orders = orders[
    orders["status"] == "Staged"
]

shipped_orders = orders[
    orders["status"] == "Shipped"
]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📦 Ready for Dispatch",
        len(dispatch_orders)
    )

with col2:
    st.metric(
        "🚚 Awaiting Pickup",
        len(staged_orders)
    )

with col3:
    st.metric(
        "📤 Shipped Orders",
        len(shipped_orders)
    )

st.divider()

# -----------------------------
# Dispatch Queue
# -----------------------------
st.subheader("📦 Dispatch Queue")
st.caption("Orders that are packed or waiting for courier pickup.")

if len(dispatch_orders) > 0:

    dispatch_display = dispatch_orders.copy()

    dispatch_display["Pickup Status"] = dispatch_display.apply(
        lambda row:
        "🟡 Awaiting Pickup"
        if row["status"] == "Staged"
        else "🔵 Packing",
        axis=1
    )

    st.dataframe(
        dispatch_display[
            [
                "order_id",
                "customer",
                "status",
                "priority",
                "courier",
                "ship_deadline",
                "Pickup Status",
                "address",
                "pincode"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:
    st.success("No orders are currently waiting for dispatch.")

st.divider()

# -----------------------------
# Courier Pickup Schedule
# -----------------------------
st.subheader("🚚 Courier Pickup Schedule")
st.caption("Compare courier cost, pickup time and estimated delivery.")

courier_display = couriers.copy()

courier_display["Pickup Window"] = courier_display["pickup_time"].apply(
    lambda x: f"Pickup by {x}"
)

st.dataframe(
    courier_display[
        [
            "courier_id",
            "courier_name",
            "cost_per_order",
            "pickup_time",
            "estimated_delivery"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

# -----------------------------
# Courier Comparison
# -----------------------------
st.subheader("⚖️ Courier Comparison")

selected_courier = st.selectbox(
    "Select Courier",
    couriers["courier_name"].tolist()
)

selected_courier_data = couriers[
    couriers["courier_name"] == selected_courier
].iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Cost / Order",
        f"₹{selected_courier_data['cost_per_order']}"
    )

with col2:
    st.metric(
        "Pickup Time",
        selected_courier_data["pickup_time"]
    )

with col3:
    st.metric(
        "Estimated Delivery",
        selected_courier_data["estimated_delivery"]
    )

st.divider()

# -----------------------------
# Delivery Status
# -----------------------------
st.subheader("📍 Delivery Status")
st.caption("Track orders that have already left the warehouse.")

delivery_summary = orders[
    orders["status"].isin(["Shipped", "Delivered"])
]

if len(delivery_summary) > 0:

    st.dataframe(
        delivery_summary[
            [
                "order_id",
                "customer",
                "status",
                "priority",
                "courier",
                "ship_deadline",
                "pincode"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No shipped or delivered orders yet.")