""" 
Streamlit app which runs the MadMeme UI in your browser.
"""

from typing import Tuple

import cv2
import numpy as np
import streamlit as st

from bots.MadMeme.meme import MemeAPI
from bots.MadMeme.model import Fuyu
from bots.MadMeme.utils import url_to_image

# title
title = "MadMeme 🥴"
st.title(title)

# layout
col1, col2 = st.columns(2)
tab = st.container()

# meme api
meme_api = MemeAPI()

# define states
if "clear" not in st.session_state:
    st.session_state["clear"] = True

if "out" not in st.session_state:
    st.session_state["out"] = None

if "img" not in st.session_state:
    st.session_state["img"] = None

if "running" not in st.session_state:
    st.session_state["running"] = False

if "run_button" not in st.session_state:
    st.session_state["running"] = False

# define functions
def get_meme() -> Tuple[np.ndarray, str]:
    """get random meme"""
    name, url = meme_api.get_random()
    image = url_to_image(url)
    return image, name


def update_img() -> None:
    """update meme image"""
    col1.placeholder.image(*st.session_state["img"])
    st.session_state["clear"] = False


def disable() -> None:
    """disable buttons with switch to run state"""
    st.session_state["running"] = True


# logic
with col1:
    # image section
    col1.placeholder = st.empty()
    if st.session_state["clear"]:
        image = url_to_image(
            "https://api.memegen.link/images/buzz/memes/memes_everywhere.png"
        )
        st.session_state["img"] = [image, "Memes everywhere!"]
        update_img()

with col2:
    # Choice section
    option = st.selectbox(
        "Get memes via:",
        ("API", "Upload"),
        disabled=st.session_state["running"],
    )

    if option == "API":
        if st.button(
            "Get meme", type="primary", disabled=st.session_state["running"]
        ):
            try:
                image, name = get_meme()
            except:
                print("Meme API call faild, trying one more time")
                image, name = get_meme()

            st.session_state["img"] = [image, name]
            update_img()

    if option == "Upload":
        upload = st.file_uploader(
            "Upload meme",
            accept_multiple_files=False,
            type=["png", "jpg"],
            disabled=st.session_state["running"],
        )
        if upload:
            file_bytes = np.asarray(bytearray(upload.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            st.session_state["img"] = [image, ""]
            update_img()

    if "bot" not in st.session_state:
        with st.spinner("Initializing bot ..."):
            # adapt model_id and force_cpu depending on your system
            model_id = (  # choice: "ybelkada/fuyu-8b-sharded" | "adept/fuyu-8b"
                "ybelkada/fuyu-8b-sharded"
            )
            force_cpu = False
            st.session_state["bot"] = Fuyu(model_id, force_cpu)

with tab:
    # Prompt and output section
    if "bot" in st.session_state:
        prompt = st.text_area(
            "Your prompt 👇",
            value=(
                "Perform OCR to extract text contained within the image. The"
                " extracted text in combination with the image represent a"
                " joke or funny situation. Explain why it is funny."
            ),
            max_chars=200,
            height=10,
            on_change=None,
        )

        if st.button(
            "Run",
            type="primary",
            disabled=st.session_state["running"],
            on_click=disable,
            use_container_width=True,
            key="run_button",
        ):
            if not st.session_state["out"]:
                with st.spinner(
                    "🏃 running model ...    (if you run on GPU, this should"
                    " take ~5-10s, on CPU ~10-20min)"
                ):
                    image = st.session_state["img"][0]
                    update_img()
                    st.session_state["out"] = st.session_state["bot"].prompt(
                        prompt, image
                    )
            if (
                "run_button" in st.session_state
                and st.session_state["running"]
            ):
                st.session_state["running"] = False
                st.rerun()

    if st.session_state["out"]:
        st.divider()
        update_img()
        st.text_area(
            "Model output:",
            st.session_state["out"],
            on_change=None,
            disabled=True,
        )
        st.session_state["out"] = None
