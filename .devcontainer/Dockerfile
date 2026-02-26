# Use an official Python image.
FROM python:3.11-slim

# Install OS dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    git \
    procps \
    build-essential \
    && apt-get clean && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install buf CLI.
ENV BUF_VERSION=1.36.0
RUN curl -sSL "https://github.com/bufbuild/buf/releases/download/v${BUF_VERSION}/buf-Linux-x86_64" -o /usr/local/bin/buf && \
    chmod +x /usr/local/bin/buf

# Install task CLI.
ENV TASK_VERSION=3.38.0
RUN curl -sSL "https://github.com/go-task/task/releases/download/v${TASK_VERSION}/task_linux_amd64.tar.gz" -o /tmp/task.tar.gz && \
    tar -xzf /tmp/task.tar.gz -C /tmp task && \
    mv /tmp/task /usr/local/bin/task && \
    chmod +x /usr/local/bin/task && \
    rm -f /tmp/task.tar.gz

# Set the working directory.
WORKDIR /workspace

# Copy the requirements files and install Python dependencies.
COPY requirements.txt requirements-devcontainer.txt ./

# Devcontainer builds should be fast/reliable. Default to a lighter dependency
# set that avoids downloading large ML/CUDA wheels.
ARG REQUIREMENTS_FILE=requirements-devcontainer.txt
RUN pip install --no-cache-dir -r ${REQUIREMENTS_FILE}

# Copy the rest of the application code.
COPY . .

# Keep the container running.
CMD ["sleep", "infinity"]
