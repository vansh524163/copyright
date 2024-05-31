FROM python:3.10.4-slim-buster

# Update and install necessary packages
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y git curl ffmpeg wget bash neofetch software-properties-common python3-pip

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Expose the port the health check server runs on
EXPOSE 8000

# Start the main application
CMD ["python3", "main.py"]
