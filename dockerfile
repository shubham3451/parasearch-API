# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat gcc libpq-dev && \
    apt-get clean

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Give execution permissions to entrypoint script
RUN chmod +x ./entrypoint.sh

# Run app through entrypoint
ENTRYPOINT ["./entrypoint.sh"]
