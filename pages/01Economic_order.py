import streamlit as st

st.set_page_config(page_title="Economic order quantity (EOQ)", layout="wide")

st.markdown(body="# General Parameters")


product_cost = st.number_input(label="Product cost", min_value=0, value=50)

holding_value = st.number_input(label="Holding cost", min_value=0.001, max_value=1.000, value= 0.05, step=0.01)

order_cost = st.number_input(label="Ordering cost", min_value=0, value=500)

anual_expected_demand = st.number_input(label="Anual expected demand", min_value=1, value=5000)

calculate_btn = st.button(label="Calculate")

if calculate_btn:

    eoq_value = ((2*anual_expected_demand*order_cost)/(product_cost*holding_value))**0.5

    st.session_state["eoq_value"] = eoq_value

    st.text(f"The Best value to order is {round(eoq_value,ndigits=0)}")