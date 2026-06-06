import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

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
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# 4. The input box (pinned to the bottom)
if user_query := st.chat_input('Message the AI....'):

    if not user_api_key:
        st.error('Please enter API Key in the sidebar first')

    else:
        # Display the user message instantly
        with st.chat_message('user'):
            st.markdown(user_query)

        # Save the user message to the vault
        st.session_state.messages.append({"role": "user", "content": user_query})

        llm = ChatGroq(
            temperature=0.7,
            model_name='llama-3.3-70b-versatile',
            api_key=user_api_key
        )

        # Convert session messages to LangChain message objects
        langchain_messages = []
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                langchain_messages.append(HumanMessage(content=msg['content']))
            else:
                langchain_messages.append(AIMessage(content=msg['content']))

        # Call the AI
        with st.spinner('AI is thinking....'):
            response = llm.invoke(langchain_messages)
            bot_answer = response.content  # ✅ consistent variable name

        # Display the bot message instantly
        with st.chat_message('assistant'):
            st.markdown(bot_answer)

        # Save the bot message to the vault ✅ fixed: was bot_response (undefined)
        st.session_state.messages.append({"role": "assistant", "content": bot_answer})
