"""app.py - Version 1 of the AI Escape Room (run with: streamlit run version1/app.py)."""
import streamlit as st
from llm import ask_gemini
from prompts import ESCAPE_TOKEN, INTRO, SYSTEM_PROMPT

st.set_page_config(page_title="AI Escape Room - V1", page_icon="🗝️")
st.title("🗝️ AI Escape Room - Version 1")

# ---------- Sidebar: instructions and restart button ----------
with st.sidebar:
    st.header("How to play")
    st.write("Type what you want to do in normal English, for example:")
    st.markdown("- *look around*\n- *examine the bookshelf*\n- *take the key*\n- *enter 123 on the drawer*")
    if st.button("🔄 Restart game"):
        st.session_state.clear()
        st.rerun()

# ---------- Game memory: the conversation is kept in st.session_state ----------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": INTRO}]
    st.session_state.escaped = False

# ---------- Show the whole conversation ----------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------- Game over ----------
if st.session_state.escaped:
    st.success("🎉 You escaped! Press 'Restart game' to play again.")
    st.stop()

# ---------- Player's turn ----------
player_text = st.chat_input("What do you do?")
if player_text:
    st.session_state.messages.append({"role": "user", "content": player_text})
    with st.chat_message("user"):
        st.markdown(player_text)

    with st.chat_message("assistant"):
        with st.spinner("The Game Master is thinking..."):
            try:
                history = [{"role": "user", "content": "Start the game."}] + st.session_state.messages
                reply = ask_gemini(SYSTEM_PROMPT, history)
            except Exception as error:
                st.error(f"Gemini error: {error}. Please try again.")
                st.session_state.messages.pop() 
                st.stop()

        if ESCAPE_TOKEN in reply: 
            st.session_state.escaped = True
            reply = reply.replace(ESCAPE_TOKEN, "").strip()
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    if st.session_state.escaped:
        st.rerun()