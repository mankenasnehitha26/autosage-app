import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

st.set_page_config(
    page_title="AutoSage - AI Vehicle Expert",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), 
                url("https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&q=80&w=1600");
    background-size: cover;
    background-attachment: fixed;
}
/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #ff4b4b;
}

/* Sidebar title */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600;
}

/* Radio buttons */
[data-testid="stSidebar"] .stRadio label {
    color: white !important;
    font-size: 16px;
    padding: 8px 12px;
    border-radius: 10px;
    transition: 0.3s ease;
}

/* Hover effect */
[data-testid="stSidebar"] .stRadio label:hover {
    background-color: rgba(255, 75, 75, 0.2);
}

/* Selected option highlight */
[data-testid="stSidebar"] .stRadio input:checked + div {
    background-color: #ff4b4b !important;
    border-radius: 10px;
}
/* Remove white top header */
header[data-testid="stHeader"] {
    background-color: #0d0d0d !important;
}

/* Remove default Streamlit toolbar background */
div[data-testid="stToolbar"] {
    background-color: #0d0d0d !important;
}

/* Make header icons visible */
header[data-testid="stHeader"] button {
    color: white !important;
}

/* Remove white menu area */
section[data-testid="stSidebar"] + div {
    background-color: transparent !important;
}


/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #ff4b4b;
}
/* Make all main content text pure white */
/* Main content text (summary + paragraphs) */
.main .block-container {
    color: #f2f2f2 !important;   /* Soft white for readability */
    font-size: 17px;
    line-height: 1.8;
}

/* Bullet point text */
ul li {
    color: #e6e6e6 !important;   /* Slight grey for clean contrast */
    font-size: 16px;
}

/* Paragraph text */
p {
    color: #f2f2f2 !important;
}


/* Main Title */
.hero-title {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    color: white;
}

/* Numbered Section Headings (1., 2., 3., etc.) */
h2 {
    color: #00bfff !important;   /* Classic Neon Blue */
    font-weight: 700;
    text-shadow: 0 0 8px rgba(0,191,255,0.4);
}

h3, h4 {
    color: #f2f2f2 !important;
    font-weight: 600;
}

/* Bullet Points - Clean & Visible */
ul {
    list-style-type: disc;
    padding-left: 25px;
}

ul li {
    color: #e6e6e6 !important;
    margin-bottom: 6px;
}


/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    color: white;
    border-radius: 30px;
    font-weight: bold;
    border: none;
    padding: 10px 25px;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0px 5px 20px rgba(255, 75, 75, 0.5);
}
            /* Futuristic Running Animation (Top Right Man Icon) */
div[data-testid="stStatusWidget"] svg {
    fill: #00ffe0 !important;          /* Neon cyan color */
    filter: drop-shadow(0 0 8px #00ffe0);
    animation: futuristicPulse 1.5s infinite ease-in-out;
}

/* Glow Pulse Animation */
@keyframes futuristicPulse {
    0% {
        filter: drop-shadow(0 0 4px #00ffe0);
        transform: scale(1);
    }
    50% {
        filter: drop-shadow(0 0 15px #00ffe0);
        transform: scale(1.1);
    }
    100% {
        filter: drop-shadow(0 0 4px #00ffe0);
        transform: scale(1);
    }
}


</style>
""", unsafe_allow_html=True)


# Load API Key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Page Config


# --- UI Header ---
st.markdown('<div class="hero-title">🚗 AutoSage: Your AI Vehicle Expert</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


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