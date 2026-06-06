import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title='My AI Chat', layout='centered')

st.title("🤖 The Groq Chatbot")
st.write('A fully integrated, memory enabled AI Assistant')

# 1. Sidebar
with st.sidebar:
    st.header('⚙️ Configuration')
    user_api_key = st.text_input('Enter your Groq API Key:', type='password')
    submit_key = st.button('Submit API Key ✅')

    if submit_key and user_api_key:
        st.session_state.api_key = user_api_key
        st.success('API Key saved!')
    elif submit_key and not user_api_key:
        st.error('Please enter an API key first!')

    if "api_key" in st.session_state:
        st.info('🔑 API Key is active')

# 2. Memory vault
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display History
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# 4. The input box
if user_query := st.chat_input('Message the AI....'):

    if "api_key" not in st.session_state:
        st.error('Please enter and submit your API Key in the sidebar first!')

    else:
        # Display the user message instantly
        with st.chat_message('user'):
            st.markdown(user_query)

        # Save the user message to the vault
        st.session_state.messages.append({"role": "user", "content": user_query})

        llm = ChatGroq(
            temperature=0.7,
            model_name='llama-3.3-70b-versatile',
            api_key=st.session_state.api_key
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
            bot_answer = response.content

        # Display the bot message
        with st.chat_message('assistant'):
            st.markdown(bot_answer)

        # Save bot message to vault
        st.session_state.messages.append({"role": "assistant", "content": bot_answer})
