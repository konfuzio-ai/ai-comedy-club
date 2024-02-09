import streamlit as st
import os
import argparse


from joke_bot import Bot


def load_custom_css():
    custom_css = """
        <style>
        .stTextInput input {
            border: 2px solid #5B34DA;
        }
        .stTextInput input:focus {
            outline: none;
            border: 2px solid #5B34DA;
        }
        </style>
        """
    st.markdown(custom_css, unsafe_allow_html=True)


def init_history_dir():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--conversations_dir', '-cd', type=str, default='conversations')

    args = parser.parse_args()
    history_dir = args.conversations_dir
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)

    return history_dir


def save_history(filename, history_dir):
    filepath = os.path.join(history_dir, filename)
    with open(filepath, "w") as file:
        for line in st.session_state.conversation:
            file.write(line + "\n")
    st.success(f"Conversation saved as {filename}")


def load_history(bot, filename, history_dir):
    filepath = os.path.join(history_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            loaded_messages = [line.strip() for line in file]

        st.session_state.conversation.clear()

        st.session_state.thread = bot.client.beta.threads.create()
        bot.thread = st.session_state.thread

        for message in loaded_messages:
            if message.startswith("user:"):
                user_message = message.split("user:", 1)[1].strip()
                run = bot.submit_message(user_message)
                bot.wait_on_run(run)

        st.session_state.conversation = loaded_messages
        st.success(f"Loaded conversation from {filename}")
    else:
        st.error(f"File {filename} does not exist")


def start_new_history(bot):
    st.session_state.conversation = []

    if "thread" in st.session_state and st.session_state.thread:
        pass
    st.session_state.thread = bot.client.beta.threads.create()
    bot.thread = st.session_state.thread
    st.success("Started a new conversation history")


def handle_joke_tell(assistant):
        assistant_response = assistant.tell_joke(st.session_state.user_input)
        st.session_state.conversation.append(f"user: {st.session_state.user_input}")
        st.session_state.conversation.append(f"assistant: {assistant_response}")
        st.session_state.user_input = ""


def handle_rate_joke(assistant):
    assistant_response = assistant.rate_joke(st.session_state.user_input, str)
    st.session_state.conversation.append(f"user: {st.session_state.user_input}")
    st.session_state.conversation.append(f"assistant: {assistant_response}")
    st.session_state.user_input = ""


@st.cache_resource
def init_bot():
    
    assistant = Bot(st.session_state.thread)
    return assistant


def main():
    history_dir = init_history_dir()
    load_custom_css()

    if "thread" not in st.session_state:
        st.session_state.thread = None


    assistant = init_bot()

    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "thread" not in st.session_state or st.session_state.thread is None:
        st.session_state.thread = assistant.thread

    st.title("Comedy Chat with AI Assistant")
    with st.sidebar:
        st.title("Conversation Options")

        history_files = os.listdir(history_dir)
        selected_file = st.selectbox("Choose a file to load:", history_files)
        if st.button("Load Selected Conversation"):
            load_history(assistant, selected_file, history_dir)

        if st.button("Start New Conversation"):
            start_new_history(assistant)

        save_filename = st.text_input("Enter filename to save conversation:", "comedian_1")
        if st.button("Save Conversation"):
            save_history(save_filename, history_dir)


    for message in st.session_state.conversation:
        st.markdown(message)

    user_input = st.text_input("Your message:", key="user_input")

    st.button("Send", on_click=handle_joke_tell, args=(assistant, ))
    st.button("Estimate", on_click=handle_rate_joke, args=(assistant,))

if __name__ == "__main__":
    main()