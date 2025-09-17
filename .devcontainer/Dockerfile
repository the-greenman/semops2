# Use an official Python image.
FROM python:3.11-slim

# Install Go and other necessary tools for buf installation.
RUN apt-get update && apt-get install -y curl unzip git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install buf CLI.
ENV BUF_VERSION=1.28.1
RUN curl -sSL "https://github.com/bufbuild/buf/releases/download/v${BUF_VERSION}/buf-Linux-x86_64" -o /usr/local/bin/buf && \
    chmod +x /usr/local/bin/buf

# Set the working directory.
WORKDIR /workspace

# Copy the requirements file and install Python dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Keep the container running.
CMD ["sleep", "infinity"]
