import os
import streamlit.components.v1 as components



parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "build")
_component_func = components.declare_component("microsoft_login_button", path=build_dir)


def microsoft_login_button(client_id:str, tenant_id:str,LoginText="Login with Microsoft",styles = None ):

    component_value = _component_func(clientId=client_id, tenantId=tenant_id, styles = styles ,LoginText= LoginText)

  
    return component_value