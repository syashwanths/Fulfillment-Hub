import streamlit as st
import pandas as pd
from utils.styles import apply_styles

st.set_page_config(page_title="Exceptions", page_icon="⚠️", layout="wide")
apply_styles()

# Load issues
issues = pd.read_csv("data/issues.csv")

st.title("⚠️ Exceptions")
st.caption("Track and resolve operational problems")

st.divider()

# Summary
open_issues = issues[issues["status"] != "Resolved"]

col1, col2 = st.columns(2)

with col1:
    status_filter = st.selectbox(
        "Filter by Issue Status",
        ["All"] + sorted(issues["status"].unique().tolist())
    )

with col2:
    priority_filter = st.selectbox(
        "Filter by Priority",
        ["All"] + sorted(issues["priority"].unique().tolist())
    )

filtered_issues = issues.copy()

if status_filter != "All":
    filtered_issues = filtered_issues[
        filtered_issues["status"] == status_filter
    ]

if priority_filter != "All":
    filtered_issues = filtered_issues[
        filtered_issues["priority"] == priority_filter
    ]

high_priority = open_issues[
    open_issues["priority"] == "High"
]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Issues", len(issues))

with col2:
    st.metric("Open Issues", len(open_issues))

with col3:
    st.metric("High Priority", len(high_priority))

st.divider()

st.subheader("Operational Issues")

if len(filtered_issues) > 0:
    st.dataframe(
        filtered_issues[
            [
                "issue_id",
                "order_id",
                "issue_type",
                "priority",
                "assigned_to",
                "status",
                "created_time",
                "notes"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("No open operational issues.")