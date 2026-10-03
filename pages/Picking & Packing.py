import streamlit as st
import pandas as pd
from utils.styles import apply_styles

st.set_page_config(page_title="Picking & Packing", page_icon="📦", layout="wide")
apply_styles()

# Load data
orders = pd.read_csv("data/orders.csv")
inventory = pd.read_csv("data/inventory.csv")

products = pd.read_csv("data/products.csv")

inventory_check = inventory.merge(
    products[["product_id", "product_name", "variant", "reorder_level"]],
    on=["product_id", "product_name", "variant"],
    how="left"
)

inventory_check["available_stock"] = (
    inventory_check["main_warehouse"]
    - inventory_check["reserved_stock"]
)

st.title("📦 Picking & Packing")
st.caption("Prepare orders accurately before dispatch")

st.divider()

# Orders currently requiring warehouse action
warehouse_orders = orders[
    orders["status"].isin(["New", "Processing", "Picking", "Packing"])
]

col1, col2 = st.columns(2)

with col1:
    st.metric("Orders Requiring Action", len(warehouse_orders))

with col2:
    st.metric(
        "Priority Orders",
        len(
            warehouse_orders[
                warehouse_orders["priority"].isin(["High", "Priority"])
            ]
        )
    )

st.divider()

st.subheader("🛒 Orders to Pick")
st.caption("Check warehouse availability before starting the picking process.")

pick_display = warehouse_orders.copy()

def check_stock(row):
    match = inventory_check[
        (inventory_check["product_name"] == row["product"]) &
        (inventory_check["variant"] == row["variant"])
    ]

    if len(match) == 0:
        return "⚠️ Product Not Found"

    available = match.iloc[0]["available_stock"]

    if available >= row["quantity"]:
        return "🟢 Available"

    if available <= 0:
        return "🔴 Transfer Required"

    return "🟡 Insufficient Stock"


pick_display["Stock Status"] = pick_display.apply(
    check_stock,
    axis=1
)

st.dataframe(
    pick_display[
        [
            "order_id",
            "product",
            "variant",
            "quantity",
            "priority",
            "status",
            "ship_deadline",
            "Stock Status"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("✅ Packing Verification")

order_list = warehouse_orders["order_id"].tolist()

if len(order_list) > 0:

    selected_order = st.selectbox(
        "Select Order to Verify",
        order_list
    )

    selected_data = warehouse_orders[
        warehouse_orders["order_id"] == selected_order
    ].iloc[0]

    stock_match = inventory_check[
    (inventory_check["product_name"] == selected_data["product"]) &
    (inventory_check["variant"] == selected_data["variant"])
]

if len(stock_match) > 0:
    available_stock = stock_match.iloc[0]["available_stock"]

    if available_stock >= selected_data["quantity"]:
        stock_status = "🟢 Available"
    elif available_stock <= 0:
        stock_status = "🔴 Transfer Required"
    else:
        stock_status = "🟡 Insufficient Stock"
else:
    available_stock = 0
    stock_status = "⚠️ Product Not Found"

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.write("**Product**")
    st.write(selected_data["product"])

with col2:
    st.write("**Variant**")
    st.write(selected_data["variant"])

with col3:
    st.write("**Quantity**")
    st.write(selected_data["quantity"])

with col4:
    st.write("**Available Stock**")
    st.write(available_stock)

with col5:
    st.write("**Stock Status**")
    st.write(stock_status)

verified = st.checkbox(
"I have verified the product, variant and quantity."
)

if verified:
    st.success("✅ Order verified and ready for packing.")
else:
    st.warning("⚠️ Verification required before packing.")

st.divider()

st.subheader("📋 Packing Checklist")

check_product = st.checkbox("Product matches the order")
check_variant = st.checkbox("Variant matches the order")
check_quantity = st.checkbox("Quantity matches the order")
check_label = st.checkbox("Shipping label matches the order")

if all([check_product, check_variant, check_quantity, check_label]):
    st.success("✅ All packing checks completed. Order is ready for dispatch.")
else:
    completed = sum(
        [check_product, check_variant, check_quantity, check_label]
    )
    st.info(f"Packing checks completed: {completed}/4")