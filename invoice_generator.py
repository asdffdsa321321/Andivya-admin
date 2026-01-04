import streamlit as st
import pandas as pd
from db import get_engine
from jinja2 import Template
from sqlalchemy import text

def render():
    st.header("🧾 Generate Invoice")

    engine = get_engine()

    order_id = st.number_input(
        "Order ID",
        min_value=1,
        step=1
    )

    if st.button("Generate Invoice", type="primary"):
        order_df = pd.read_sql(
            text("""
                SELECT *
                FROM orders
                WHERE id = :order_id
            """),
            engine,
            params={"order_id": order_id}
        )

        if order_df.empty:
            st.error("Order not found")
            return

        order = order_df.iloc[0].to_dict()

        items_df = pd.read_sql(
            text("""
                SELECT
                    p.title,
                    oi.quantity,
                    oi.price_paise / 100.0 AS price_inr
                FROM order_items oi
                JOIN products p ON p.id = oi.product_id
                WHERE oi.order_id = :order_id
            """),
            engine,
            params={"order_id": order_id}
        )

        items = items_df.to_dict(orient="records")

        with open("templates/invoice.html", "r") as f:
            template = Template(f.read())

        html = template.render(order=order, items=items)

        st.download_button(
            "⬇️ Download Invoice",
            data=html,
            file_name=f"invoice_{order_id}.html",
            mime="text/html"
        )
