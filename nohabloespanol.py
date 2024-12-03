import streamlit as st
import openai
import json
import pandas as pd
import random

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
Given a Spanish text, split it into words and provide:
- Word in Spanish
- IPA transcription
- English translation
- Thai translation
- Part of speech (e.g., noun, verb, adjective)
Return the data as a JSON array of objects, one object per word, formatted like this:
[
    {"word": "hola", "IPA": "ˈo.la", "english_translation": "hello", "thai_translation": "สวัสดี", "part_of_speech": "interjection"}
]
"""

# Funny loading memes
loading_meme = [
    "Loading… because irregular verbs need therapy.💆‍♀️",
    "Wait… we’re still arguing with el agua 💧, which is feminine but insists it’s not.🏳️‍⚧️✨",
    "One second… ☝️ trying to explain why burro doesn’t mean butter.🧈",
    "Processing… 🤔 just like you’re processing that esposa can mean ‘wife’ or ‘handcuffs.⛓️’",
    "Wait a moment… ✋ we’re deciding if the subjunctive is really necessary. (Spoiler: it is.)🫢",
    "Loading… ⚙️ translating ¡Caramba! because honestly, even we’re not sure what it means.😯",
    "Please wait… 🚶‍♀️looking for someone who truly understands por and para.🔍",
    "Hold on… 🧘‍♀️ debating whether ll sounds like ‘y,’ ‘j,’ or nothing today.🤷‍♀️"
]

# Submit button
if st.button("✦ Analizar Texto ✦"):
    if not user_api_key:
        st.error("Uh oh where is your API key? Enter it and try again!")
    elif not user_input.strip():
        st.error("Please Enter some Spanish text to analyze.🧏‍♀️")
    else:
        # Build OpenAI chat messages
        results = []
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]

        with st.spinner(random.choice(loading_meme)):  # Add funny loading message
            try:
                # Send request to OpenAI API
                response = client.chat.completions.create(
                    model = "gpt-4o-mini",
                    messages = messages, 
                    temperature = 0.6
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
        csv = df.to_csv(index = False, encoding = 'utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label = "🪄 Download (CSV)",
            data = csv,
            file_name = "spanish_text_analysis.csv",
            mime = 'text/csv'
        )

