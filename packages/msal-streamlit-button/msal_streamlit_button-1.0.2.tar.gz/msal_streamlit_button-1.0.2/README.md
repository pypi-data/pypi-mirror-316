# streamlit-custom-component

Streamlit component that allows you to do X

## Installation instructions

```sh
pip install streamlit-custom-component
```

## Usage instructions

```python
import streamlit as st

from microsoft_login_button import microsoft_login_button

value = microsoft_login_button(client_id, tenant_id,LoginText,styles )

st.write(value)
```