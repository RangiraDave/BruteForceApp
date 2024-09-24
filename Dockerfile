# Use the official Python image from the Docker Hub
FROM python:3.10-slim
# # Use the official Nginx image from the Docker Hub
# FROM nginx:alpine

# # Set environment variables
# COPY ./nginx.conf /etc/nginx/nginx.conf

# # Start nginx and keep it running
# CMD ["nginx", "-g", "daemon off;"]

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file
COPY requirements.txt .

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Download the NLTK data required for your app
RUN python -m nltk.downloader words

# Copy the current directory contents into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
