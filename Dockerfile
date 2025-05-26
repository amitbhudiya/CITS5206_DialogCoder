# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port for Streamlit app
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start command
CMD ["streamlit", "run", "app/Home.py"] 
