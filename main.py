import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

career_paths = {
    "STEM": ["science", "math", "coding", "physics", "robotics", "engineering"],
    "Arts": ["painting", "music", "theatre", "writing", "drawing"],
    "Sports": ["cricket", "football", "running", "gym", "sports", "badminton"],
    "Commerce": ["business", "finance", "marketing", "economics", "accounts"],
    "Humanities": ["history", "sociology", "psychology", "philosophy"],
    "Design": ["fashion", "design", "graphics", "ux", "illustration"]
}

def needs_more_info(text):
    return len(text.split()) < 6 or not any(kw in text.lower() for kws in career_paths.values() for kw in kws)

st.title("🎓 Smart Career Path Recommender")
user_input = st.text_area("Tell us about your hobbies, interests, and scores:")

if st.button("🎯 Get Recommendation"):
    if not user_input.strip():
        st.warning("Please enter something.")
    elif needs_more_info(user_input):
        st.info("Can you tell us more about your favourite subjects, hobbies, or marks?")
    else:
        prompt = f"""
        A student says: "{user_input}"
        Choose the most fitting career path from these:
        STEM, Arts, Sports, Commerce, Humanities, Design.

        Give a short explanation for each career path that might suit the student, and highlight the top one clearly.
        """
        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1-0528-qwen3-8b:free",
                messages=[{"role": "user", "content": prompt}]
            )
            st.success("Recommended Career Paths:")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {e}")
st.markdown("___")
st.markdown("Made by Rohan with 💖  \n📧 rohanrvc45@gmail.com")
