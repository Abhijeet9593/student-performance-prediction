import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Student Success AI",
    page_icon="🎓",
    layout="wide"
)

# Professional Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        background-color: #2e59a8;
        color: white;
        height: 3em;
        border-radius: 8px;
    }
    .result-card {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        font-size: 22px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Load the model securely
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as file:
        return pickle.load(file)

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")

# Sidebar - Instructions
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=100)
    st.title("About the Tool")
    st.info("""
    This AI model analyzes student demographics, study habits, and previous grades to predict final academic success.
    
    **Features used:**
    - Attendance Rate
    - Study Hours
    - Previous Performance
    """)

# Header
st.markdown("<h1 style='text-align: center;'>🎓 Student Performance Analytics</h1>", unsafe_allow_html=True)
st.divider()

# Input Form
with st.form("prediction_form"):
    st.subheader("📝 Student Details")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        gender = st.selectbox("Gender", ["No", "Yes"])
        age = st.number_input("Age", 10, 50, 20)
        parent_edu = st.selectbox("Parent Education Level", [0, 1, 2, 3])

    with c2:
        attendance = st.slider("Attendance Rate (%)", 0, 100, 85)
        study_hours = st.number_input("Weekly Study Hours", 0, 168, 15)
        internet = st.selectbox("Internet Access", ["No", "Yes"])

    with c3:
        extracurricular = st.selectbox("Extracurriculars", ["No", "Yes"])
        prev_score = st.number_input("Previous Score", 0, 100, 70)
        final_score_input = st.number_input("Current Score", 0, 100, 75)

    submit = st.form_submit_button("Run AI Prediction")

# Processing Prediction
if submit:
    # Ensure all inputs are converted to the correct numeric format for the model 
    data = {
        'gender': [1 if gender == "Yes" else 0],
        'age': [float(age)],
        'study_hours_per_week': [float(study_hours)],
        'attendance_rate': [float(attendance)],
        'parent_education': [float(parent_edu)],
        'internet_access': [1 if internet == "Yes" else 0],
        'extracurricular': [1 if extracurricular == "Yes" else 0],
        'previous_score': [float(prev_score)],
        'final_score': [float(final_score_input)]
    }
    
    input_df = pd.DataFrame(data)
    
    # Make Prediction
    prediction = model.predict(input_df)
    
    st.markdown("---")
    if prediction[0] == "Yes":
        st.balloons()
        st.markdown("""<div class='result-card' style='background-color: #e1f5fe; color: #01579b;'>
                    ✅ <b>Prediction: SUCCESS</b><br>The student is likely to pass the academic term.</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class='result-card' style='background-color: #ffebee; color: #b71c1c;'>
                    ❌ <b>Prediction: AT RISK</b><br>Additional academic support is recommended.</div>""", unsafe_allow_html=True)
