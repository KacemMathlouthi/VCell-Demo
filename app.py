import streamlit as st
import json
from PIL import Image
from utils.params_extraction import get_path_params
from utils.llm_helper import get_llm_response
from vcelldb.vcell_api import query_vcell_models
from vcelldb.diagram import get_diagram_urls, get_bmkeys

favicon = Image.open("misc/favi.ico")
st.set_page_config(
    page_title="VCell Chatbot Demo", page_icon=favicon, layout="centered"
)

# Header
col1, col2, col3 = st.columns([1, 5, 1])

with col1:
    st.image("misc/gsoc.png", width=60)

with col2:
    st.markdown(
        """
        <h1 style='text-align: center; margin-bottom: 0;'>🤖 VCell BioModel Chatbot Demo</h1>
        <p style='text-align: center; font-size: 18px;'>Demo Built for Google Summer of Code 2025</p>
        <p style='text-align: center; margin-top: 0.5em; font-size: 16px;'>
            <a href='https://www.linkedin.com/in/kacem-mathlouthi/' target='_blank' style='text-decoration: none; margin-right: 20px;'>
                <img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg' alt='LinkedIn' width='22' style='vertical-align: middle; margin-right: 6px;'/>
                LinkedIn
            </a>
            <a href='https://github.com/KacemMathlouthi/VCell-Demo' target='_blank' style='text-decoration: none; margin-right: 20px;'>
                <img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg' alt='GitHub' width='22' style='vertical-align: middle; margin-right: 6px;'/>
                GitHub
            </a>
            <a href='mailto:kacem.mathlouthi@insat.ucar.tn' style='text-decoration: none;'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/7/7e/Gmail_icon_%282020%29.svg' alt='Gmail' width='22' style='vertical-align: middle; margin-right: 6px;'/>
                Email
            </a>
        </p>
        """,
        unsafe_allow_html=True,
    )


with col3:
    st.image("misc/NRNB.png", width=300)

st.markdown("""
    <div style="text-align: center; margin-top: 30px; color: #444;">
        <p style="font-size: 18px;">💡 Try one of these example prompts:</p>
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-top: 20px;">
            <div style="border: 1px solid #ccc; border-radius: 8px; padding: 10px 16px; background-color: #f8f9fa; font-size: 15px;">
                List a VCell biomodels authored by the user ion
            </div>
            <div style="border: 1px solid #ccc; border-radius: 8px; padding: 10px 16px; background-color: #f8f9fa; font-size: 15px;">
                Find a VCell biomodel with the id 201844485
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar Configuration
st.sidebar.title("LLM Provider Settings")
llm_provider = st.sidebar.selectbox("Select LLM Provider", ["Groq (Cloud)", "Ollama (Local)"])

if llm_provider == "Groq (Cloud)":
    groq_model = st.sidebar.selectbox(
        "Choose Groq Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "meta-llama/llama-4-maverick-17b-128e-instruct", "meta-llama/llama-4-scout-17b-16e-instruct"]
    )
    groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
    if groq_api_key:
        st.session_state["llm_settings"] = {"provider": "groq", "api_key": groq_api_key, "model": groq_model}
else:
    st.sidebar.markdown("""
    Make sure Ollama is installed and running.
    You can pull a model by running the following command in your terminal:
    ```bash
    ollama pull llama3
    ```
    Replace `llama3` with your desired model name (like `mistral`, `qwen`, etc.).                 
    Then you have to start the model by running the following command:
    ```bash
    ollama run llama3
    ```
    """)
    ollama_model = st.sidebar.text_input("Enter Local Ollama Model Name (e.g., llama3, mistral, etc.)")
    if ollama_model:
        st.session_state["llm_settings"] = {"provider": "ollama", "model": ollama_model}

# Save Button
if st.sidebar.button("Save Settings"):
    st.success("✅ LLM settings saved!")


# Session Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat History
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask something about VCell biomodels..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Step 1: Feature extraction
    with st.spinner("🔍 Extracting features..."):
        extracted_params = get_path_params(prompt)

    if "error" in extracted_params:
        error_msg = f"Error extracting features: {extracted_params['error']}"
        st.chat_message("assistant").markdown(error_msg)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": error_msg}
        )
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
            st.session_state.chat_history.append(
                {"role": "assistant", "content": error_msg}
            )
        else:
            # Show API data
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
            st.session_state.chat_history.append(
                {"role": "assistant", "content": llm_response}
            )

            # STEP 4: Show Diagrams
            diagram_urls = get_diagram_urls(api_data)

            if diagram_urls:
                st.markdown("**Model Diagram(s):**")
                for url in diagram_urls:
                    try:
                        st.image(url, use_container_width=True)
                    except:
                        st.markdown(f"[View Diagram]({url})")

            # STEP 5: Show SBML and VCML Download Links
            bmkeys = get_bmkeys(api_data)

            if bmkeys:
                st.markdown("### 📥 Download BioModel Files")

                for bmkey in bmkeys:
                    st.markdown(
                        f"""
                        **BioModel ID:** `{bmkey}`  
                        🔹 [Download SBML](https://vcell.cam.uchc.edu/api/v0/biomodel/{bmkey}/biomodel.sbml)  
                        🔹 [Download VCML](https://vcell.cam.uchc.edu/api/v0/biomodel/{bmkey}/biomodel.vcml)
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.warning("⚠️ No BioModel keys found in the API response.")
