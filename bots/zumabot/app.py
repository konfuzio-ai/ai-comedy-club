import streamlit as st
from gtts import gTTS
from bot import Bot

TOOLTIP_TEXT_COMMENTS = "Write each comment separated by ;"

st.title("AI Comedy Club 🎭")

if "zuma_bot" not in st.session_state:
    with st.spinner("Initializing bot ..."):
        st.session_state["zuma_bot"] = Bot()
# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Do you want to be judged or to attend to the show?",
        ("Bot Preparation", "Zuma Comedian Bot", "Zuma Judge Bot")
    )

if add_radio == "Bot Preparation":
    st.image("bots/zumabot/data/images/bot_learning.jpeg")
    city = st.text_input("Next show city name:")
    st.session_state['zuma_bot'].current_city = city
    if st.button("Learn new jokes"):
        with st.spinner("Learning ..."):
            st.session_state["zuma_bot"].study_new_jokes()


elif add_radio == "Zuma Comedian Bot":
    st.title("Comedian Bot🤖")
    comedian_introduction = st.session_state['zuma_bot'].introduce_comedian()

    # TODO: move text to audio to utils folder
    # This module is imported so that we can
    # play the converted audio

    # Language in which you want to convert
    language = 'en'
    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=comedian_introduction, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome
    myobj.save("welcome.mp3")

    audio_file = open("welcome.mp3", 'rb')
    audio_bytes = audio_file.read()

    audio_widget = st.audio(audio_bytes, format='audio/ogg')
    introduction_text = st.markdown(comedian_introduction)
    # Here I will select jokes tanking into account assistants preferences
    st.session_state["zuma_bot"].select_current_show_jokes()
    do_assistants_want_a_joke = st.button("Tell me a joke!")
    if do_assistants_want_a_joke:
        st.session_state["zuma_bot"].tell_joke()
    joke = st.markdown(st.session_state["zuma_bot"].current_joke)
    are_there_laughs = st.checkbox("hahahaha")
    is_there_applause = st.checkbox("Applause")
    comments = st.text_input("Insert comments:", help=TOOLTIP_TEXT_COMMENTS).split(";")
    if comments:
        with st.spinner("Noticing feedback"):
            st.session_state["zuma_bot"].notice_feedback(are_there_laughs=are_there_laughs,
                                                         is_there_applause=is_there_applause,
                                                         comments=comments)
    placeholder = st.empty()
    do_assistants_want_to_finish = placeholder.button("Please, no more jokes")
    if do_assistants_want_to_finish:
        st.markdown("## No more jokes, please go to Bot Preparation and comeback again if you want more new jokes")
        st.session_state["zuma_bot"].finish_show()

elif add_radio == "Zuma Judge Bot":
    st.title("Judge Bot 🤖")
    joke = st.text_input("Provide your joke:")
    # Not adding Personalization judgement criteria. It will be added
    if joke:
        with st.spinner("Rating joke"):
            joke_rating = st.session_state["zuma_bot"].rate_joke(current_joke=joke)
    does_comedian_want_to_know_the_rating = st.button("Click to know the rating",
                                                      help="Do not click more than once with the same joke, it will re-rate the joke and add the rating to the current one")
    if does_comedian_want_to_know_the_rating:
        st.markdown(f"The rating of this joke is {st.session_state['zuma_bot'].current_joke_rating}")

    does_next_comedian_want_to_perform = st.button("Next comedian")

    if does_next_comedian_want_to_perform:
        st.session_state["zuma_bot"].finish_this_comedian_judgement()
