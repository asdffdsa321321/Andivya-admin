import streamlit as st
import pandas as pd
from db import get_engine

def render():
    st.header("📑 Orders")

    engine = get_engine()

    # --- Load orders ---
    orders_df = pd.read_sql("""
        SELECT
            id,
            customer_name,
            status,
            amount_paise / 100.0 AS amount_inr,
            created_at
        FROM orders
        ORDER BY created_at DESC
    """, engine)

    # --- Show table ---
    st.dataframe(
        orders_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --- Select order safely ---
    order_ids = orders_df["id"].tolist()

    if not order_ids:
        st.info("No orders found.")
        return

    selected_order_id = st.selectbox(
        "Select Order ID",
        order_ids
    )

    new_status = st.selectbox(
        "Update Status",
        ["paid", "shipped", "cancelled"]
    )

    # --- Update status ---
    if st.button("Update Order Status", type="primary"):
        with engine.begin() as conn:
            conn.execute(
                """
                UPDATE orders
                SET status = :status
                WHERE id = :id
                """,
                {"status": new_status, "id": selected_order_id}
            )

        st.success(f"Order #{selected_order_id} updated to '{new_status}'")
        st.rerun()
