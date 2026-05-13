FROM python:3.11-slim

# Install system dependencies for OpenCV and MediaPipe
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements_docker.txt .
RUN pip install --no-cache-dir -r requirements_docker.txt

# Copy app files
COPY api.py .
COPY index.html .
COPY models/maurice_model/saved_models/ ./models/maurice_model/saved_models/

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
