FROM python:3.10.4-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    python3-pip \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Copy the entire project
COPY . .

# Run the bot as a module
CMD ["python3", "-m", "devgagan.main"]
