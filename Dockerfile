# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the current directory contents into the container at /app
COPY pyproject.toml poetry.lock* /app/

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Copy the rest of your application's code
COPY . /app

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
