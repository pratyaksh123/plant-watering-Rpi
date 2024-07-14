# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libffi-dev \
    libi2c-dev \
    python3-dev \
    i2c-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock into the container at /app
COPY Pipfile Pipfile.lock /app/

# Install dependencies from Pipfile
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of your application code
COPY . /app

CMD ["python3"]
