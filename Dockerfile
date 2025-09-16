# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# First, copy just the pyproject.toml to leverage Docker layer caching
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy the rest of the application's code into the container
COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the application when the container launches
# Assuming your FastAPI app instance is named 'app' in 'my-fullstack-agent/app/agent_engine_app.py'
CMD ["uvicorn", "app.agent_engine_app:app", "--host", "0.0.0.0", "--port", "8080"]
