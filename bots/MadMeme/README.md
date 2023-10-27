# MadMeme 🥴

Welcome the first multi modal comedian on stage. 🎉

MadMeme's **strength** is **presenting and interpreting memes**, but it can tell normal jokes as well!

https://github.com/nengelmann/ai-comedy-club/assets/120744129/8f5defa7-1cb6-4136-aacd-d96fdb5a278c

# Requirements
MadMeme should just be run on a PC with **Nvidia GPU** and at least **16GB** free GPU **memory**.
There is an option to run on CPU with enough RAM, but the time constraint is not feasible. If you still want to enforce to run it on CPU, checkout app.py and change 'force_cpu' as well as the 'model_id'.

# Installation
```bash
python -m pip install --upgrade pip
pip install -e .
pip install streamlit
pip install requests
pip install git+https://github.com/huggingface/transformers.git
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
You can run it as a normal bot.




# TODO

- [ ] Fine tune model with noisy image data and jokes as labels.
