import streamlit as st
import json
from utils.params_extraction import get_path_params
from utils.llm_helper import get_llm_response
from vcelldb.vcell_api import query_vcell_models

st.set_page_config(page_title="💬 VCell Chatbot", layout="centered")

# Header
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("misc/gsoc.png", width=60)  

with col2:
    st.markdown(
        "<h1 style='text-align: center; margin-bottom: 0;'>🤖 VCell BioModel Chatbot Demo</h1>"
        "<p style='text-align: center; font-size: 18px;'>Built for Google Summer of Code 2025</p>",
        unsafe_allow_html=True
    )

with col3:
    st.image("misc/NRNB.png", width=200) 

st.markdown("---")

# Session Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat History
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask something about VCell models..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Step 1: Feature extraction
    with st.spinner("🔍 Extracting features..."):
        extracted_params = get_path_params(prompt)

    if "error" in extracted_params:
        error_msg = f"Error extracting features: {extracted_params['error']}"
        st.chat_message("assistant").markdown(error_msg)
        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
    else:
        # Show extracted params
        with st.expander("🧠 Extracted Query Parameters", expanded=False):
            st.json(extracted_params)

        # Step 2: Query VCell
        with st.spinner("📡 Querying VCell models..."):
            api_data = query_vcell_models(extracted_params)

        if "error" in api_data:
            error_msg = f"Error querying VCell API: {api_data['error']}"
            st.chat_message("assistant").markdown(error_msg)
            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        else:
            # Show API data (collapsible)
            with st.expander("📦 VCell API Response", expanded=False):
                st.json(api_data)

            # Step 3: LLM Summary
            with st.spinner("🤖 Generating response..."):
                llm_summary_prompt = f"""
You are a VCell BioModel assistant helping users understand biological models.

User question:
\"{prompt}\"

VCell API response:
{json.dumps(api_data, indent=2)}

Generate a helpful, detailled human-readable summary of the results. Explain the model, the simulations and the applications.
"""
                llm_response = get_llm_response(llm_summary_prompt)

            st.chat_message("assistant").markdown(llm_response)
            st.session_state.chat_history.append({"role": "assistant", "content": llm_response})
