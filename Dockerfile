# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install SQLite3 and necessary Python libraries
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application and the SQLite DB to the container
COPY . .

# Set necessary permissions
RUN chown -R 1000:1000 /app && chmod 755 /app && chmod 644 /app/db_loader/example.db

# Switch to a non-root user (optional but recommended for security reasons)
USER 1000

# Command to run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
