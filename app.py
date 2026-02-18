import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

# -----------------------------------
# Load Environment Variables
# -----------------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Missing GOOGLE_API_KEY. Please check your .env file.")
    st.stop()

# Create Gemini Client
client = genai.Client(api_key=api_key)

# -----------------------------------
# Get Available Gemini Models
# -----------------------------------
available_models = []

try:
    models = client.models.list()
    for m in models:
        if "gemini" in m.name.lower():
            available_models.append(m.name)

except Exception as e:
    st.sidebar.error(f"Error listing models: {e}")

# -----------------------------------
# Sidebar Configuration
# -----------------------------------
st.sidebar.header("⚙️ Configuration")

selected_model_name = st.sidebar.selectbox(
    "Select Model",
    available_models,
    index=0 if available_models else None
)

# -----------------------------------
# Gemini Response Function
# -----------------------------------
def get_nutritional_info(food_items, model_name):
    try:
        system_prompt = """
You are a certified nutrition expert.

Provide detailed nutritional information for the given food items.

Include:
1. Calories
2. Macronutrients (Protein, Carbohydrates, Fat)
3. Micronutrients (Vitamins & Minerals)
4. Health benefits
5. Dietary considerations (if any)

Structure the output clearly and professionally.
"""

        response = client.models.generate_content(
            model=model_name,
            contents=[
                system_prompt,
                f"Food items: {food_items}"
            ]
        )

        return response.text

    except Exception as e:
        return f"Error: {e}"

# -----------------------------------
# Streamlit UI
# -----------------------------------
st.set_page_config(
    page_title="NutriAI - Smart Nutrition Analyzer",
    layout="centered"
)

st.title("🥗 NutriAI - Smart Nutrition Analyzer")
st.write("Enter food items to get detailed nutritional analysis powered by Gemini AI.")

food_items = st.text_area(
    "Enter Food Items (separate by commas):",
    placeholder="e.g., Rice, Chicken Breast, Broccoli"
)

analyze_button = st.button("Get Nutritional Information")

# -----------------------------------
# Run Analysis
# -----------------------------------
if analyze_button:
    if not food_items:
        st.warning("Please enter at least one food item.")
    elif not selected_model_name:
        st.error("No model available for selection.")
    else:
        with st.spinner("Analyzing nutritional data..."):
            result = get_nutritional_info(food_items, selected_model_name)

        st.subheader("📊 Nutritional Report")
        st.write(result)
