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
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt && \
    # Install additional Python dependencies in the same layer
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
