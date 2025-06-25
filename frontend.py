
import streamlit as st
import requests

# Streamlit Page Configuration
st.set_page_config(page_title="HealthAI Assistant", layout="wide", page_icon="🧠")

st.markdown("""
    <style>
        .main { background-color: #f4f9f9; }
        .stTabs [data-baseweb="tab"] { font-size: 18px; padding: 10px 20px; }
        .stTabs [aria-selected="true"] { background-color: #c8e6c9; color: black; font-weight: bold; border-radius: 5px; }
        .stTextInput>div>div>input { background-color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 HealthAI - Your Smart Health Assistant")

tabs = st.tabs([
    "💬 Chat Assistant",
    "🧪 Disease Predictor",
    "💊 Treatment Planner",
    "📊 Health Analytics",
])

# Base URL of your FastAPI backend
backend_url = "https://sneha0504-healthai-backend.hf.space"


# --- Chat Assistant ---
with tabs[0]:
    st.subheader("💬 Chat with HealthAI")
    st.markdown("Ask any health-related question, and our AI assistant will respond.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Type your health-related query here..."):
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            try:
                res = requests.post(f"{backend_url}/chat", json={"user_input": user_input})
                if res.status_code == 200:
                    bot_response = res.json().get("response")
                else:
                    bot_response = f"Error: {res.status_code}"
            except Exception as e:
                bot_response = f"Error: {e}"

        st.chat_message("assistant").markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

# --- Disease Predictor ---
with tabs[1]:
    st.subheader("🧪 Disease Predictor")
    st.markdown("Enter symptoms to predict the most likely disease.")

    symptoms_input = st.text_input("💡 Enter symptoms (separated by commas)")

    if st.button("Predict Disease"):
        if symptoms_input:
            with
    st.spinner("Predicting..."):
                try:
                    res = requests.post(f"{backend_url}/predict-disease", json={"symptoms": symptoms_input.split(" ,")})
                    if res.status_code == 200:
                        prediction = res.json().get("predicted_disease")
                        st.success(f"🩺 Predicted Disease: {prediction}")
                    else:
                        st.error(f"Error: {res.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter symptoms to predict the disease.")

# --- Treatment Plan Generator ---
with tabs[2]:
    st.subheader("💊 Treatment Plan Generator")
    st.markdown("Enter a disease or condition to receive a treatment plan.")

    treatment_input = st.text_input("💡 Enter diagnosis")

    if st.button("Generate Plan"):
        if treatment_input:
            with st.spinner("Generating Treatment Plan..."):
                try:
                    res = requests.post(f"{backend_url}/generate-treatment", json={"user_input": treatment_input})
                    if res.status_code == 200:
                        treatment_plan = res.json().get("treatment_plan")
                        st.success(treatment_plan)
                    else:
                        st.error(f"Error: {res.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a diagnosis.")

# --- Health Analytics Dashboard ---
with tabs[3]:
    st.subheader("📊 Health Analytics")
    st.markdown("Provide patient health data to generate analytics and insights.")

    analytics_input = st.text_area("💡 Enter patient health data")

    if st.button("Generate Analytics"):
        if analytics_input:
            with st.spinner("Analyzing..."):
                try:
                    res = requests.post(f"{backend_url}/health-analytics", json={"user_input": analytics_input})
                    if res.status_code == 200:
                        analytics = res.json().get("analytics")
                        st.success(analytics)
                    else:
                        st.error(f"Error: {res.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter patient health data.")
