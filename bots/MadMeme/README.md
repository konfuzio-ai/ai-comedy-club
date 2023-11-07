# MadMeme 🥴

Welcome the first multi modal comedian on stage. 🎉

MadMeme's **strength** is **presenting and interpreting memes**, but it can tell normal jokes as well!

Check it out in this colab or watch the video down below! 👇

<a href="https://colab.research.google.com/github/nengelmann/ai-comedy-club/blob/main/bots/MadMeme/Fuyu_8B_Exploration.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

https://github.com/nengelmann/ai-comedy-club/assets/120744129/8f5defa7-1cb6-4136-aacd-d96fdb5a278c

# Requirements
MadMemes multi modal capabilities (streamlit app) should just be run on a PC with **Nvidia GPU** and at least **16GB** free GPU **memory**.
There is an option to run on CPU with enough RAM, but the time constraint is not feasible. If you still want to enforce to run it on CPU, checkout app.py and change 'force_cpu' as well as the 'model_id'.

# Create virtual env (optional)

```bash
virtualenv -p /usr/bin/python3.9 .venv && source .venv/bin/activate
```

# Installation: ai-comedy-club
Installation of common dependencies as in '/ai-comedy-club/.github/workflows/main.yml'.
```bash
python -m pip install --upgrade pip
pip install tensorrt --extra-index-url https://pypi.nvidia.com
pip install -e .
```

# Installation: Additional dependencies for MadMemes streamlit app
```bash
pip install streamlit
pip install requests
pip install transformers
pip install bitsandbytes
pip install accelerate
pip install opencv-python
```

# Usage

## MadMeme Multi-Modal
```bash
streamlit run bots/MadMeme/app.py
```
Then checkout [`http://localhost:8501`](http://localhost:8501) to use MadMemes multi modal capabilities.

## MadMeme Normal
You can run it as a normal bot with /ai-comedy-club/main.py, however no memes or images are used here.
Or you can run it directly by:
```bash
python bots/MadMeme/joke_bot.py
```

# TODO
- [ ] Fine tune fuyu-8b model with noisy image data (randomness) and jokes as labels.
- [ ] Add logging
