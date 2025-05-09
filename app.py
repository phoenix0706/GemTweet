import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os


# Step 1: Choose Provider
provider = st.sidebar.selectbox("🤖 Enter API Key",  "Gemini")


api_key = st.sidebar.text_input("🔑 Gemini API Key", type="password")

# Step 4: Proceed if keys and file are present
if api_key :

    os.environ["GOOGLE_API_KEY"] = api_key
    llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    # google_api_key=GOOGLE_API_KEY,
    temperature=0.9,
    convert_system_message_to_human=True,
)


# Load Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not GOOGLE_API_KEY:
    st.error("Enter your GOOGLE_API_KEY .")
    st.stop()

st.title("💡 Gem Tweet ") 
st.caption("Generate Tweets using Gemini @ Powered by Gemini 2.0 Flash (LangChain + Streamlit)")

# Input Description
description = st.text_area("What is your idea or message for the tweet?", height=120)

# Dropdowns
user_options = {}


# First Row: Trending Topics, Tone, Tweet Length
row1 = st.columns(3)
user_options["trending"] = row1[0].selectbox("Trending Topics", [
    "AI & Tech", "Politics", "Entertainment", "Sports", "Finance & Stocks",
    "Climate Change", "Space & Science"
])
user_options["tone"] = row1[1].selectbox("Tone", [
    "Informative", "Humorous", "Sarcastic", "Inspirational", "Professional", "Casual"
])
user_options["length"] = row1[2].selectbox("Tweet Length", [
    "Short (under 100 chars)", "Medium (100-200 chars)", "Long (200-280 chars)"
])

# Second Row: Purpose, Hashtag Usage
row2 = st.columns(2)
user_options["purpose"] = row2[0].selectbox("Purpose", [
    "Controversial", "Humorous", "Aggressive", "Generic", "Persuasive", "Thought-Provoking"
])

user_options["hashtags"] = row2[1].selectbox("Hashtag Usage", [
    "No Hashtags", "Trending Hashtags", "Custom Hashtags", "Industry-Specific Hashtags"
])

formatted_options = "\n".join([f"{key}: {value}" for key, value in user_options.items()])

# Prompt Template
prompt = ChatPromptTemplate.from_template("""
You are a professional tweet writer for top-performing AI and Tech Twitter accounts.

Task:
Write **exactly 3 engaging tweets** based on the following idea:
- {description}

Style Guide (apply strictly):
{formatted_options}

Format & Rules (MUST FOLLOW):
- Return ONLY the 3 tweets.  No intros, summaries, or extra text.
- Separate tweets using this exact delimiter: `###`
- Use a scroll-stopping hook: question, emoji, or bold statement.
- Keep the tone tweet-native — not a blog, essay, or explanation.
- Match the user's selected tone, length, purpose, hashtags, and trending topic.
- Avoid repetition or filler. Each tweet should stand alone.""")


# Generate
if st.button("Generate Tweets 🚀"):
    if not description.strip():
        st.warning("Please describe your tweet idea.")
    else:
        with st.spinner("Crafting tweets..."):
            formatted_options = "\n".join([f"{k}: {v}" for k, v in user_options.items()])
            chain = prompt | llm | StrOutputParser()
            result = chain.invoke({
                "description": description.strip(),
                "formatted_options": formatted_options
            })
            tweets = [t.strip() for t in result.split("###") if t.strip()]
            for i, tweet in enumerate(tweets, 1):
                st.text_area(f"Tweet {i}", tweet, height=80)
