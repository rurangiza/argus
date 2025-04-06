import streamlit as st

pg = st.navigation([
    st.Page("qa.py", title="Q&A"),
  ],
)

pg.run()