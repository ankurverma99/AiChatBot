import streamlit as st
from langchain_groq import ChatGroq

st.set_page_config(page_title='My AI Chat', layout='centered')

st.title("🤖 The Groq Chatbot")
st.write('A fully integrated, memory enabled AI Assistant')

# 1. Sidebar
with st.sidebar:
    st.header('⚙️ Configuration')
    user_api_key = st.text_input('Enter your Groq api key:', type='password')
    st.info('Your key is required to wake up the AI brain')


# 2. Memory vault
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display History
# Redraw all past messages every time the page reruns
for msg in st.session_state.messages:
    with st.chat_message(msg['role']): # This display human and ai message differently
        st.markdown(msg['content'])

# 3. The input box(pinned to the bottom)
if user_query := st.chat_input('Message the AI....'):

    if not user_api_key:
        st.error('Please enter API Key in the sidebar first')

    else:
    # Display the user message instantly
        with st.chat_message('user'):
            st.markdown(user_query)

        # Save the user message to the vault
        st.session_state.messages.append({"role":"user", "content": user_query})

        llm = ChatGroq(
            temperature = 0.7,
            model_name = 'llama-3.3-70b-versatile',
            api_key = user_api_key
        )

        # Call the Actual AI

        with st.spinner('AI is thinking....'):
            response = llm.invoke(st.session_state.messages)
            bot_answer = response.content


        # Display the bot message instantly
        with st.chat_message('assistant'):
            st.markdown(bot_answer)

        # Save the user message to the vault
        st.session_state.messages.append({"role":"assistant", "content": bot_response})
