# Use an official Python image from the Docker Hub
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container
COPY . .

# Expose the Flask app port
EXPOSE 5001

# Set the environment variable for Flask to run in development mode (optional)
ENV FLASK_ENV=development

# Run the Flask app with Gunicorn for production or with Flask’s built-in server for dev
CMD ["python", "app.py"]
