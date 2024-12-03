import streamlit as st
import openai
import json
import pandas as pd
import random
import re

# Title and description
st.title("🎀 Tu Spanish Text Analyser 🇪🇸 🖋️")
st.markdown("""
This app analyzes Spanish text, breaking it into individual words and providing: \n
✶ IPA transcription \n
✶ English and Thai translations \n
✶ Part of Speech (POS) information \n
""")

# Sidebar for API key
user_api_key = st.sidebar.text_input("🔒 Enter your OpenAI API key below ↓ ", type="password")

# Input text area
user_input = st.text_area("Enter your Spanish text ✍️:", "Escribe algo aquí!", height=200)

client = openai.OpenAI(api_key = user_api_key)
# Prompt definition
prompt = """You are a linguist specializing in Spanish. 
Given a single Spanish word or a Spanish text, split it into words (if it's a text) or process it directly (if it's a single word). Provide:
- Word in Spanish
- IPA transcription
- English translation
- Thai translation
- Part of speech (e.g., noun, verb, adjective)
Return the data as a JSON array of objects, even if there's only one word. For example:
[
    {"word": "días", "IPA": "ˈdi.as", "english_translation": "days", "thai_translation": "วัน", "part_of_speech": "noun"}
]
"""

# Funny loading memes
loading_meme = [
    "Loading… because irregular verbs need therapy. 💆‍♀️",
    "Wait… we’re still arguing with el agua 💧, which is feminine but insists it’s not. 🏳️‍⚧️✨",
    "One second… ☝️ trying to explain why burro doesn’t mean butter. 🧈",
    "Processing… 🤔 just like you’re processing that esposa can mean ‘wife’ or ‘handcuffs. ⛓️’",
    "Wait a moment… ✋ we’re deciding if the subjunctive is really necessary. (Spoiler: it is.) 🫢",
    "Loading… ⚙️ translating ¡Caramba! because honestly, even we’re not sure what it means. 😯",
    "Please wait… 🚶‍♀️looking for someone who truly understands por and para. 🔍",
    "Hold on… 🧘‍♀️ debating whether ll sounds like ‘y,’ ‘j,’ or nothing today. 🤷‍♀️"
]

# Load Spanish words
def load_spanish_words():
    words = set()
    try:
        with open("./data/spanish_words.txt", "r") as file:
            for line in file:
                word = line.strip() 
                if word:
                    words.add(word)
    except FileNotFoundError:
        print("File not found")
    return words

# Function to clean input text
def clean_text(text):
    # Remove digits and special characters, but keep non-Latin characters like Thai, Japanese, Korean, Chinese, and Arabic
    cleaned_text = re.sub(r'[^a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s\u0E00-\u0E7F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u0600-\u06FF\uAC00-\uD7AF]', '', text)
    return cleaned_text

# Function to check if input contains non-Latin characters
def contains_non_latin(text):
    non_latin_pattern = re.compile('[^\x00-\x7F]+')
    return bool(non_latin_pattern.search(text))

# Function to validate if text is Spanish
def is_valid_spanish(text, spanish_words):
    if contains_non_latin(text):
        return False, "Non-Latin characters detected"
    words = clean_text(text).split()
    invalid_words = [word for word in words if word.lower() not in spanish_words]
    if invalid_words:
        return False, invalid_words
    return True, []
spanish_words = load_spanish_words()

# Submit button
if st.button("✦ Analizar Texto ✦"):
    if not user_api_key:
        st.error("Uh-oh where is your API key? Enter it and try again!")
    elif not user_input.strip():
        st.error("Please Enter some Spanish text to analyze.🧏‍♀️")
    else:
        # Clean and validate the input
        cleaned_input = clean_text(user_input)
        is_valid, invalid_words = is_valid_spanish(cleaned_input, spanish_words)
        if not is_valid:
            if invalid_words == "Non-Latin characters detected":
                st.error("⚠️ Uh-oh It seems like your text contains non-Spanish words or invalid characters.😕 Please try again.")
            else:
                st.error(f"⚠️ Uh-oh It seems like your text contains non-Spanish words or invalid characters.: {', '.join(invalid_words)}.")
        else:
            # Proceed with OpenAI API call as usual
            results = []
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": cleaned_input}
            ]
            
            with st.spinner(random.choice(loading_meme)):  # Add funny loading message
                try:
                    # Send request to OpenAI API
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        temperature=0.6
                    )
                    chat_response = response.choices[0].message.content
                    esp_data = json.loads(chat_response)

                    for item in esp_data:
                        results.append({
                            "Word": item.get("word", "N/A"),
                            "IPA": item.get("IPA", "N/A"),
                            "English Translation": item.get("english_translation", "N/A"),
                            "Thai Translation": item.get("thai_translation", "N/A"),
                            "Part of Speech": item.get("part_of_speech", "N/A")
                        })

                except Exception as e:
                    st.error(f"An error occurred while processing your text: {str(e)}")
                    results.append({
                        "Word": "Error",
                        "IPA": "N/A",
                        "English Translation": "N/A",
                        "Thai Translation": "N/A",
                        "Part of Speech": str(e)
                    })

            # Create a DataFrame
            df = pd.DataFrame(results)

            # Display the DataFrame
            st.subheader(" ⭑ Aquí es tu Spanish Analysed Table 💁‍♀️")
            st.dataframe(df)

            # Allow download as CSV
            csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button(
                label="🪄 Download (CSV)",
                data=csv,
                file_name="spanish_text_analysis.csv",
                mime='text/csv'
            )
