import streamlit as st

st.title("🤖 RetailPulse AI Assistant")

question = st.text_input("Ask a business question")

if question:

    st.success("Question Received")

    if "sales" in question.lower():
        st.write("Sales are performing well with strong revenue growth.")

    elif "customer" in question.lower():
        st.write("Customer segmentation helps identify loyal and at-risk customers.")

    elif "forecast" in question.lower():
        st.write("Demand forecasting predicts future sales trends.")

    else:
        st.write("AI Assistant is ready to answer business questions.")

        