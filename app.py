import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

def local_css():
    st.markdown("""
    <style>
        /* Main background and font */
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                        url("https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&q=80&w=1600");
            background-size: cover;
            color: white;
        }
        
        /* Modernize the sidebar */
        [data-testid="stSidebar"] {
            background-color: rgba(20, 20, 20, 0.9);
            border-right: 1px solid #ff4b4b;
        }

        /* Styling buttons to look 'automotive' */
        div.stButton > button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 20px;
            border: none;
            width: 100%;
            transition: all 0.3s ease;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        div.stButton > button:hover {
            background-color: #ff3333;
            transform: scale(1.05);
            box-shadow: 0px 4px 15px rgba(255, 75, 75, 0.4);
        }

        /* Metric cards styling */
        [data-testid="stMetricValue"] {
            color: #ff4b4b;
            font-family: 'Orbitron', sans-serif;
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Load API Key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Page Config
st.set_page_config(page_title="AutoSage - AI Vehicle Expert", page_icon="🏎️")

# --- UI Header ---
st.title("🏎️ AutoSage: Your AI Vehicle Expert")
st.markdown("---")

# --- Sidebar Navigation ---
scenario = st.sidebar.radio("Go to:", ["Vehicle Comparison", "Maintenance Alerts", "Eco-Friendly Search"])

# --- AI Logic Function ---
def ask_autosage(prompt, context):
    try:
        system_instruction = f"You are AutoSage, an automotive expert. Context: {context}."
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=f"{system_instruction}\n\nUser Question: {prompt}"
        )
        return response.text
    except Exception as e:
        # This will print the detailed JSON error to your Streamlit screen
        return f"🚨 API Error: {str(e)}"

# --- Scenario 1: Comparison ---
if scenario == "Vehicle Comparison":
    st.header("🏍️ Motorcycle & Car Comparison")
    col1, col2 = st.columns(2)
    with col1: v1 = st.text_input("Vehicle 1", "Yamaha R1")
    with col2: v2 = st.text_input("Vehicle 2", "BMW S1000RR")
    
    if st.button("Compare Specs"):
        query = f"Compare {v1} and {v2} in detail including price and performance."
        with st.spinner("Analyzing..."):
            result = ask_autosage(query, "Sarah is buying a new vehicle and needs a comparison.")
            st.markdown(result)

# --- Scenario 2: Maintenance ---
elif scenario == "Maintenance Alerts":
    st.header("🔧 Proactive Maintenance Tips")
    v_model = st.text_input("What do you drive?", "Tesla Model 3")
    season = st.selectbox("Current Season", ["Winter", "Summer", "Rainy"])
    
    if st.button("Get Maintenance Alert"):
        query = f"Provide seasonal maintenance tips for a {v_model} during {season}."
        with st.spinner("Checking health..."):
            result = ask_autosage(query, "Proactive vehicle health check alert.")
            st.info(result)

# --- Scenario 3: Eco-Friendly ---
elif scenario == "Eco-Friendly Search":
    st.header("🌿 Green Vehicle Discovery")
    budget = st.slider("Budget ($)", 20000, 150000, 50000)
    
    if st.button("Find Eco Options"):
        query = f"Suggest the best electric or hybrid cars for a budget of ${budget}."
        with st.spinner("Searching green tech..."):
            result = ask_autosage(query, "Emma is looking for sustainable vehicle options.")
            st.success(result)