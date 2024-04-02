# Use an official Python runtime as a parent image
FROM python:3.9-slim
# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*
# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the current directory contents into the container at /app
COPY pyproject.toml poetry.lock* /app/

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . /app
COPY . /domain
COPY . /infrastructure
COPY . /schemas

COPY wait-for-db.sh entrypoint.sh ./

ENTRYPOINT ["./entrypoint.sh"]
