import streamlit as st
import openai
import pandas as pd

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
user_input = st.text_area("Enter Spanish text:", "Escribe algo aquí.✍️", height=200)

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

# Submit button
if st.button("Analizar Texto"):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not user_input.strip():
        st.error("Please enter some text to analyze.")
    else:
        try:
            # Set OpenAI API key
            openai.api_key = api_key
            
            # API call to OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": processing_prompt},
                    {"role": "user", "content": user_input},
                ]
            )
            
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
            except Exception as parse_error:
                st.error(f"Error parsing results: {parse_error}")
        except Exception as api_error:
            st.error(f"Error with OpenAI API: {api_error}")