import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai



load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro', generation_config={"temperature": 1})

def generate_response(age, income, saving_goal):

    prompt = f"""
    You are the Aqua: One the best Financial Planning AI. in the world. You create a plan's for the user to make successfull money strategies to invest which helps to achieve there goal in saving money.
    user: Age of the user is  {age} and having amount with {income} and there saving goal is {saving_goal}. 
    
    Best AI generate the best result.
    """
    response = model.generate_content(prompt, stream=True)
    
    
    for chunk in response:
        yield chunk.text

def main():
    st.title("💰 Financial Planning Assistant")
    st.write("Welcome to the Financial Planning Assistant! Please provide some information about your finances and age.")

    age = st.number_input("👴 Age (years)", min_value=18, max_value=100, value=25)

    income = st.number_input("💵 Monthly Income ($)", min_value=0, step=1000, value=5000)

    default_saving_goal = income * 2

    saving_goal = st.number_input("💰 Saving Goal ($)", min_value=0, step=1000, value=default_saving_goal)

    if st.button("Generate Plan"):
        if saving_goal <= income:
            st.error("Your saving goal must be greater than your monthly income.")
        else:
            response = generate_response(age, income, saving_goal)
            st.success("Generating Financial Plan... 📈")
            st.write_stream(response)

if __name__ == "__main__":
    main()