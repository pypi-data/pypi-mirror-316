import streamlit as st
from microsoft_login_button import microsoft_login_button

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/example.py`

st.subheader("Component with constant args")

component_value = microsoft_login_button()
