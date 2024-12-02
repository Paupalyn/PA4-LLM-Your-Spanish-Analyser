import streamlit as st
import openai
import pandas as pd
import json

# Title and description
st.title("🎀 Tu Spanish Text Analyser 🇪🇸 🖋️")
st.markdown("""
This app analyzes Spanish text, breaking it into individual words and providing:
- IPA transcription
- English anAnalyze Textd Thai translations
- Part of Speech (POS) information
""")

# Sidebar for API key
api_key = st.sidebar.text_input("Enter your OpenAI API key 🔐", type="password")

# Input text area
user_input = st.text_area("Enter Spanish text ✍️:", "Escribe algo aquí.", height=200)

# Prompt for OpenAI
client = openai.OpenAI(api_key=user_api_key)
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
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    temperature = 0.6,
                    messages=[
                        {"role": "system", "content": processing_prompt},
                        {"role": "user", "content": user_input},
                    ]
                )
                esp_json = response.choices[0].message.content
                esp_list = json.loads(esp_json)
            
            # Extract and parse the response
                result_content = response['choices'][0]['message']['content']
            try:
                data = pd.DataFrame(eval(result_content))  # Convert JSON array to DataFrame
                st.markdown("### Analysis Results:")
                st.dataframe(data)  # Display DataFrame
                
                # Allow CSV download
                csv = data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="spanish_text_analysis.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")

        #สร้าง DataFrame
        df = pd.DataFrame(results)

        #แสดงผล
        st.subheader("Spanish Analysed Table 💁‍♀️")
        st.dataframe(df)
       

        #ดาวน์โหลด CSV
        csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label="🪄 download (CSV)",
            data=csv,
            file_name="nohablamosespanol_result.csv",
            mime='text/csv'
        )
