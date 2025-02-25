# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the correct port
EXPOSE 8000

# Set environment variables
#Use 'production' for production
ENV FLASK_APP=app.py
ENV FLASK_ENV=development  
ENV FLASK_RUN_PORT=8000

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]
