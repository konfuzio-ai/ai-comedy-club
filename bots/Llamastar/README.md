
# AI Comedy Club - Docker Setup with GPU Support

Welcome to the AI Comedy Club, where humor meets technology! In this repository, you'll discover a Dockerfile that empowers you to run my AI comedian bot with GPU support. This README will serve as your trusty guide, walking you through the process of setting up and running your bot within a Docker container.

## Prerequisites

Before you begin, make sure you have the following prerequisites:

- A system with an NVIDIA GPU.
- NVIDIA Docker runtime (nvidia-docker2) installed. You can find installation instructions here: [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-runtime).

## Step 1: Clone the Repository (if not already done)

If you haven't already, clone the AI Comedy Club repository to your local machine:

```bash
git clone https://github.com/onur-rgb/ai-comedy-club.git

```

## Step 2: Build the Docker Image


1. Open a terminal and navigate to the project directory.

2. Build the Docker image using the following command:

```bash
cd ai-comedy-club/bots/Llamastar
docker build -t my-joke-bot .
```

This command builds a Docker image named `my-joke-bot` with GPU support based on the contents of the Dockerfile.

## Step 3: Run the Docker Container

To run your AI comedian bot inside a Docker container with GPU support, use the following command:

```bash
docker run --gpus all -it my-joke-bot
```

AI comedian bot is now running within the Docker container. You can interact with it as needed.

## About the Chatbot - Meet Llamastar
Let's introduce you to the star of the show, Llamastar! This AI comedian bot was crafted using TheBloke's Llama-2-7B-chat-GPTQ model. But that's not all; I've spiced it up with Gradio and Langchain applications to provide you with an interactive and entertaining experience. Feel free to explore Llamastar's comedic talents and have a blast at the AI Comedy Club!

This README is your backstage pass to the world of Llamastar and GPU-supported AI comedy. It's time to enjoy the show and let the laughter begin! 🎤😄

