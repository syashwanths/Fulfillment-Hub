# Fulfillment Hub

A simple Streamlit-based fulfillment operations dashboard designed to help an e-commerce business monitor orders, inventory, warehouse operations, courier dispatch, and operational exceptions in one place.

## Problem

The existing fulfillment process relies on spreadsheets and shared folders, making it difficult to:

- Track order status at a glance
- Identify priority orders
- Detect inventory shortages
- Prevent wrong product or variant shipments
- Monitor courier pickups
- Track unresolved operational issues

## Solution

Fulfillment Hub provides a centralized operations dashboard with:

- Order tracking and filtering
- Priority order visibility
- Inventory and stock availability monitoring
- Secondary warehouse transfer identification
- Picking and packing verification
- Courier pickup and delivery monitoring
- Courier cost and delivery comparison
- Operational exception tracking
- Dashboard-level operational KPIs

## Tech Stack

- Python
- Streamlit
- Pandas
- CSV-based sample data

## Project Structure

```text
FulfillmentHub/
├── app.py
├── data/
│   ├── orders.csv
│   ├── products.csv
│   ├── inventory.csv
│   ├── couriers.csv
│   └── issues.csv
├── pages/
│   ├── orders.py
│   ├── inventory.py
│   ├── picking_packing.py
│   ├── dispatch_delivery.py
│   └── exceptions.py
└── utils/
    └── style.py
```

## How to Run Locally
1. Clone the repository
git clone https://github.com/YOUR-USERNAME/fulfillment-hub.git
cd fulfillment-hub

2. Install dependencies
pip install streamlit pandas

3. Run the application
streamlit run app.py

The application will open in your browser.

Sample Data

The project uses sample fulfillment data created specifically for demonstration purposes. No real customer, store, courier, or business data is used.


### Important

Replace:

```text
YOUR-USERNAME
```
with your actual GitHub username only in the README clone URL.

**Copy Rights @**
**Yashwanth S**
