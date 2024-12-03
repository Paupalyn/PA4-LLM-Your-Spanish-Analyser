import streamlit as st
import openai
import pandas as pd
import json
import random

# Title and description
st.title("🎀 Tu Spanish Text Analyser 🇪🇸 🖋️")
st.markdown("""
This app analyzes Spanish text, breaking it into individual words and providing:
- IPA transcription
- English and Thai translations
- Part of Speech (POS) information
""")

# Sidebar for API key
user_api_key = st.sidebar.text_input("Enter your OpenAI API key 🔐", type="password")

# Input text area
user_input = st.text_area("Enter Spanish text ✍️:", "Escribe algo aquí.", height=200)

# Prompt for OpenAI
processing_prompt = """
You are a linguist specializing in Spanish. Given a Spanish text, split it into words and provide:
- Word in Spanish
- IPA transcription
- English translation
- Thai translation
- Part of speech (e.g., noun, verb, adjective)

Return the data as a JSON array of objects like this:
[
    {"word": "hola", "IPA": "ˈo.la", "english_translation": "hello", "thai_translation": "สวัสดี", "part_of_speech": "interjection"}
].
"""

# Funny loading memes
loading_meme = [
    "Loading… because irregular verbs need therapy.",
    "Wait… we’re still arguing with el agua, which is feminine but insists it’s not.",
    "One second… trying to explain why burro doesn’t mean butter.",
    "Processing… just like you’re processing that esposa can mean ‘wife’ or ‘handcuffs.’",
    "Wait a moment… we’re deciding if the subjunctive is really necessary. (Spoiler: it is.)",
    "Loading… translating ¡Caramba! because honestly, even we’re not sure what it means.",
    "Please wait… looking for someone who truly understands por and para.",
    "Hold on… debating whether ll sounds like ‘y,’ ‘j,’ or nothing today."
]

# Function to process text with OpenAI API
def process_text(user_api_key, text):
    try:
        openai.api_key = user_api_key
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": processing_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.6
        )
        st.write("API Response Raw:", response) 
        return response
    except openai.error.OpenAIError as api_error:
        st.error(f"OpenAI API error: {api_error}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

# Submit button
if st.button("Analizar Texto"):
    if not user_api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not user_input.strip():
        st.error("Please enter some text to analyze.")
    else:
        with st.spinner(random.choice(loading_meme)):
            response = process_text(user_api_key, user_input)
            if response:
                if "choices" in response and len(response["choices"]) > 0:
                    api_content = response["choices"][0]["message"]["content"]
                    if api_content.strip():
                        try:
                            esp_list = json.loads(api_content)
                            # Create a DataFrame
                            df = pd.DataFrame(esp_list)

                            # Display the DataFrame
                            st.markdown("### Spanish Analysed Table 💁‍♀️")
                            st.dataframe(df)

                            # Allow CSV download
                            csv = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
                            st.download_button(
                                label="Download Results as CSV",
                                data=csv,
                                file_name="spanish_text_analysis.csv",
                                mime="text/csv",
                            )
                        except json.JSONDecodeError:
                            st.error("Failed to parse the API response as JSON. Please check the prompt or input.")
                    else:
                        st.error("Received an empty response from the API.")
                else:
                    st.error("No valid response received from the OpenAI API.")
            else:
                st.error("Failed to process your request. Please check your input or API key.")
