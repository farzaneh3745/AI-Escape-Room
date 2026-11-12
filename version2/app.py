"""app.py - Version 2 of the AI Escape Room (run with: streamlit run version2/app.py)."""
import streamlit as st
from game_engine import CONFIG, do_action, new_game
from llm import describe_result, understand_action

st.set_page_config(page_title="AI Escape Room - V2", page_icon="🗝️")
st.title("🗝️ AI Escape Room - Version 2")

if "game" not in st.session_state:
    st.session_state.game = new_game()
    st.session_state.messages = [{"role": "assistant", "content": CONFIG["intro"]}]
    # st.session_state.last_turn = None
game = st.session_state.game

with st.sidebar:
    st.header("How to play")
    st.markdown("- *look around*\n- *examine the bookshelf*\n- *take the key*\n"
                "- *use the key on the painting*\n- *enter 123 on the drawer*")
    if st.button("🔄 Restart game"):
        st.session_state.clear()
        st.rerun()

    st.header("Game state (kept by Python)")
    st.write("🎒 Inventory:", ", ".join(game["inventory"]) or "empty")
    st.write("✅ Solved:", ", ".join(game["solved"]) or "nothing yet")
    # if st.session_state.last_turn:
    #     st.json(st.session_state.last_turn)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if game["escaped"]:
    st.success("🎉 You escaped! Press 'Restart game' to play again.")
    st.stop()

player_text = st.chat_input("What do you do?")
if player_text:
    try:
        command = understand_action(player_text)                 # 1. Gemini translates
    except Exception as error:
        st.error(f"Gemini error: {error}. Please try again.")
        st.stop()

    code = str(command["code"]) if command.get("code") else None
    fact = do_action(game, command.get("action"), command.get("target"), command.get("item"), code)  # 2. Python decides

    try:
        reply = describe_result(fact)                            # 3. Gemini tells the story
    except Exception:
        reply = fact                                             

    st.session_state.messages.append({"role": "user", "content": player_text})
    st.session_state.messages.append({"role": "assistant", "content": reply})
    # st.session_state.last_turn = {"You said": player_text, "Gemini understood": command, "Python decided": fact}
    st.rerun()