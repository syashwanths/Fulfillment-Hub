import streamlit as st
import pandas as pd
from utils.styles import apply_styles

st.set_page_config(page_title="Inventory", page_icon="📦", layout="wide")
apply_styles()

# Load data
inventory = pd.read_csv("data/inventory.csv")
products = pd.read_csv("data/products.csv")

# Connect inventory with reorder levels
inventory_data = inventory.merge(
    products[["product_id", "reorder_level"]],
    on="product_id",
    how="left"
)

# Calculate available stock
inventory_data["available_stock"] = (
    inventory_data["main_warehouse"]
    - inventory_data["reserved_stock"]
)

st.title("📦 Inventory")
st.caption("Monitor warehouse stock and identify transfer requirements")

st.divider()

# Summary
low_stock = inventory_data[
    inventory_data["available_stock"] < inventory_data["reorder_level"]
]

transfer_required = inventory_data[
    (inventory_data["available_stock"] <= 0) &
    (inventory_data["secondary_warehouse"] > 0)
]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Inventory Records", len(inventory_data))

with col2:
    st.metric("Low Stock Alerts", len(low_stock))

with col3:
    st.metric("Transfer Required", len(transfer_required))

st.divider()

st.subheader("Inventory Overview")

inventory_display = inventory_data.copy()

inventory_display["Stock Status"] = inventory_display.apply(
    lambda row:
        "🔴 Transfer Required"
        if row["available_stock"] <= 0 and row["secondary_warehouse"] > 0
        else "🟡 Low Stock"
        if row["available_stock"] < row["reorder_level"]
        else "🟢 Healthy",
    axis=1
)

st.dataframe(
    inventory_display[
        ["product_id", "product_name", "variant",
         "main_warehouse", "secondary_warehouse",
         "reserved_stock", "available_stock",
         "reorder_level", "Stock Status", "last_stock_check"]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("🔄 Stock Transfer Required")

if len(transfer_required) > 0:

    transfer_required = transfer_required.copy()

    transfer_required["suggested_transfer"] = (
        transfer_required["reorder_level"]
        - transfer_required["available_stock"]
    )

    st.dataframe(
        transfer_required[
            [
                "product_id",
                "product_name",
                "variant",
                "main_warehouse",
                "secondary_warehouse",
                "reserved_stock",
                "available_stock",
                "suggested_transfer"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:
    st.success("No stock transfers are currently required.")

st.divider()

st.subheader("📋 Transfer Status")

transfer_status = st.selectbox(
    "Current Transfer Status",
    ["Pending", "In Progress", "Completed"]
)

if transfer_status == "Pending":
    st.warning("Transfer is pending.")

elif transfer_status == "In Progress":
    st.info("Transfer is currently in progress.")

else:
    st.success("Transfer completed.")