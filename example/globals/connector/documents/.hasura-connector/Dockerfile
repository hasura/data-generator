FROM ghcr.io/hasura/ndc-python-lambda:v0.2.0

# Install system dependencies for python-magic
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic-dev \
    file && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /functions

# Copy the requirements.txt and install Python dependencies
COPY requirements.txt /functions/
RUN python3 -m venv venv && \
    # Activate the virtual environment for all subsequent commands in this RUN instruction
    . venv/bin/activate && \
    # Upgrade pip, setuptools, and wheel in the virtual environment
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    # Pre-install PyTorch for CPU (only torch, as torchvision and torchaudio are not needed)
    echo "Pre-installing PyTorch CPU version (torch only)..." && \
    pip install --no-cache-dir \
        torch==2.7.0 \
        --extra-index-url https://download.pytorch.org/whl/cpu && \
    # Install dependencies from requirements.txt
    # If requirements.txt specifies torch, pip should recognize the pre-installed version
    # if it meets the version constraints.
    echo "Installing dependencies from requirements.txt..." && \
    pip install --no-cache-dir -r requirements.txt && \
    # Install additional Python dependencies in the same layer
    # If 'doculyzer' is listed in requirements.txt, this specific line for 'doculyzer'
    # might be redundant or could be used to ensure a specific version if needed.
    # Its torch dependency should be satisfied by the pre-installed version.
    echo "Installing python-magic and doculyzer..." && \
    pip install --no-cache-dir python-magic doculyzer

# Copy the rest of the application code
COPY ./ /functions

# Create a user and adjust permissions in a single layer
RUN adduser -u 1000 python && \
    chown -R python:python /functions

# Switch to the non-root python user
USER python

# Uncomment the command when ready to run
# CMD ["venv/bin/python", "startup.py", "--log-level", "DEBUG"]
