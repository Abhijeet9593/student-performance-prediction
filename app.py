import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load the model
def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

st.title("🎓 Student Performance Predictor")
st.write("Enter the details below to predict if a student will pass.")

# Create input fields based on your model's features
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["No", "Yes"])
    age = st.number_input("Age", min_value=10, max_value=100, value=20)
    study_hours = st.number_input("Study Hours per Week", min_value=0, max_value=168, value=10)
    attendance = st.slider("Attendance Rate (%)", 0, 100, 85)

with col2:
    parent_edu = st.selectbox("Parent Education Level", [0, 1, 2, 3])
    internet = st.selectbox("Internet Access", ["No", "Yes"])
    extracurricular = st.selectbox("Extracurricular Activities", ["No", "Yes"])
    prev_score = st.number_input("Previous Score", min_value=0, max_value=100, value=75)
    final_score = st.number_input("Current Midterm/Final Score", min_value=0, max_value=100, value=75)

# Mapping selections to numerical data
input_data = pd.DataFrame({
    'gender': [1 if gender == "Yes" else 0],
    'age': [age],
    'study_hours_per_week': [study_hours],
    'attendance_rate': [attendance],
    'parent_education': [parent_edu],
    'internet_access': [1 if internet == "Yes" else 0],
    'extracurricular': [1 if extracurricular == "Yes" else 0],
    'previous_score': [prev_score],
    'final_score': [final_score]
})

# Prediction logic
if st.button("Predict Outcome"):
    prediction = model.predict(input_data)
    
    if prediction[0] == "Yes":
        st.success("🎉 Prediction: The student is likely to SUCCEED.")
    else:
        st.error("⚠️ Prediction: The student is at risk of FAILING.")
