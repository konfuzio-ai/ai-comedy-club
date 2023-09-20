# Use a base image with GPU support (e.g., NVIDIA CUDA)
FROM pytorch/pytorch:latest

# Install Git in the container
RUN apt-get update && \
    apt-get install -y git

# Set the working directory
WORKDIR /app

# Copy your application code to the container (assuming your Python files are in the same directory as the Dockerfile)
COPY . /app

# Install Python dependencies using pip
RUN pip install -r requirements.txt

# Define the command to run your application
CMD [ "python", "joke_bot.py" ]