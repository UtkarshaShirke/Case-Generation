import streamlit as st
#from dotenv import load_dotenv
import os
import openai
from htmlTemplates import css, bot_template, user_template
import toml

def main():
    #load_dotenv()
    st.set_page_config(page_title="Generate Case Studies", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    st.session_state.user_text = ""
    st.session_state.conversation = None

    st.header("Generate Case Studies :books:")

    selected_tab = st.sidebar.radio("Navigation", options=["Case Study"], horizontal=True, label_visibility="collapsed")

    if selected_tab == "Case Study":
        st.sidebar.subheader("Generate Case Study about:")
        user_text = st.session_state.user_text

        user_text = st.sidebar.text_area("Enter your text here", user_text)

        if st.sidebar.button('Process'):
            with st.spinner('Processing'):
                if user_text:
                    total_character_count = len(user_text)
                    if total_character_count > 1000:
                        st.warning("Total input data should not exceed 1,000 characters.")
                        st.stop()
                    questions = [
                        f"Generate a case study for a sample company in detail in the following field: {user_text}.",
                    ]

                    initial_prompt = "Act like a management case study generator. Make sure to include tables with sample data regarding the case."

                    if st.session_state.conversation is None:
                        #config = toml.load("secrets.toml")
                        #api_key = config["openai"]["api_key"]
                        openai.api_key = st.secrets['OPENAI_API_KEY'] # Replace with your OpenAI API key
                        st.session_state.conversation = []

                        for i, question in enumerate(questions):
                            response = openai.ChatCompletion.create(
                                model="gpt-4",
                                messages=[
                                    {"role": "system", "content": initial_prompt},
                                    {"role": "user", "content": question},
                                ],
                            )

                            st.session_state.conversation.append(response['choices'][0]['message']['content'])

                    # Store user_text in session_state
                    st.session_state.user_text = user_text

                # Generate answers to questions and print them
                for i, (question, response) in enumerate(zip(questions, st.session_state.conversation)):
                    st.write(user_template.replace("{{MSG}}", f"Question {i + 1}: {question}"), unsafe_allow_html=True)
                    st.write(bot_template.replace("{{MSG}}", f"{response}\n"), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
