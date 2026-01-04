import streamlit as st
from product_uploader import render as product_page
from orders_dashboard import render as orders_page
from invoice_generator import render as invoice_page

st.set_page_config(
    page_title="Andivya Admin",
    layout="wide"
)

st.sidebar.title("Admin")

page = st.sidebar.radio(
    "Navigate",
    [
        "Upload Products",  # ✅ FIRST = default
        "Orders",
        "Invoices",
    ],
    index=0  # ✅ ensures Product Uploader loads first
)

if page == "Upload Products":
    product_page()
elif page == "Orders":
    orders_page()
elif page == "Invoices":
    invoice_page()
