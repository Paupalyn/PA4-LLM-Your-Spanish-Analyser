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
api_key = st.sidebar.text_input("Enter your OpenAI API key 🔐", type="password")

# Input text area
user_input = st.text_area("Enter Spanish text ✍️:", "Escribe algo aquí.", height=200)

# Prompt for OpenAI
processing_prompt = """
Act as a linguist who is expert in Spanish morphology and syntax. You will receive a Spanish text, and you should break it into individual words. 
For each word, provide the following:
1. "word" - the original word in Spanish
2. "IPA" - the International Phonetic Alphabet transcription of the word
3. "english_translation" - the translation of the word into English
4. "thai_translation" - the translation of the word into Thai
5. "part_of_speech" - the part of speech (e.g., noun, verb, adjective)
Return the result as a JSON array, where each element contains these fields.
"""

# Funny loading meme
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

# Submit button
if st.button("Analizar Texto"):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not user_input.strip():
        st.error("Please enter some text to analyze.")
    else:
        with st.spinner(random.choice(loading_meme)):
            try:
                # Set OpenAI API key
                openai.api_key = api_key
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    temperature=0.6,
                    messages=[
                        {"role": "system", "content": processing_prompt},
                        {"role": "user", "content": user_input},
                    ]
                )

                # Check if the response contains choices and a valid message
                if response and 'choices' in response and len(response['choices']) > 0:
                    # Ensure that the response contains valid content
                    content = response['choices'][0].message.content.strip()

                    if content:
                        try:
                            # Attempt to parse the content as JSON
                            esp_list = json.loads(content)

                            # Create a DataFrame
                            df = pd.DataFrame(esp_list)

                            # Display the DataFrame
                            st.markdown("Spanish Analysed Table 💁‍♀️")
                            st.dataframe(df)  # Display DataFrame

                            # Allow CSV download
                            csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                            st.download_button(
                                label="Download Results as CSV",
                                data=csv,
                                file_name="spanish_text_analysis.csv",
                                mime="text/csv",
                            )
                    else:
                        st.error("The response from OpenAI does not contain valid content.")
                else:
                    st.error("No valid response received from the API.")

            except json.JSONDecodeError:
                st.error("There was an error parsing the response. It might not be in valid JSON format.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
