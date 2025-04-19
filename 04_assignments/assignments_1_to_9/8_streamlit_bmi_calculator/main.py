import streamlit as st
import pandas as pd

st.title("BMI Calculator in 6 Minutes")

height = st.slider("Enter your height (in cm): ", 100, 250, 175)
weight = st.slider("Enter you weight in (in kg): ", 40, 200, 70)

bmi = weight / ((height / 100) ** 2)

st.info(f"Your BMI is {bmi:.2f}")

st.write("### BMI Categories ###")
st.write("- Underweight: BMI less than 18.5")
st.write("- Normal Weight: BMI between 18.5 and 24.9")
st.write("- Overweight: BMI between 25 and 29.9")
st.write("- Obesity: BMI 30 or greater")
