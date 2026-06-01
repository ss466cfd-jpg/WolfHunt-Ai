import streamlit as st
import google.generativeai as genai

# Streamlit Community Cloud-oda 'Secrets' la irunthu key-a edukkum
# Ithu thaan safe-ana murai
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("API Key config la issue irukku, Streamlit Secrets-la set pannungapa!")
    st.stop()

# Model setup
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.set_page_config(page_title="WolfHunt AI", page_icon="🐺")
st.title("🐺 WolfHunt Core Engine")

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input processing
if user_input := st.chat_input("Sollunga pa, enna help venum?"):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        try:
            # Response generation
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Oops! Edho technical error. Refresh panni try pannunga.")