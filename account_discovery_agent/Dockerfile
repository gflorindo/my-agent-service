# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# First, copy just the pyproject.toml to leverage Docker layer caching
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN apt-get update && apt-get install -y libstdc++6 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -e .

# Copy the rest of the application's code into the container
COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the application when the container launches
CMD ["uvicorn", "account_discovery_agent.deployment:app", "--host", "0.0.0.0", "--port", "8080"]
