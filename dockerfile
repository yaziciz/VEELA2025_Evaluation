# Use official Python image (no conda)
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for packages like scikit-image, nibabel)
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    synapseclient==2.6.0 \
    surface-distance==0.1 \
    scikit-image \
    scikit-learn \
    numpy==1.24.1 \
    pandas \
    nibabel

# Copy VEELA2025_Evaluation folder, Test_GT folder
COPY VEELA2025_Evaluation /app/VEELA2025_Evaluation
COPY Test_GT /app/Test_GT

# Run the main script
CMD ["python", "/app/VEELA2025_Evaluation/receiver.py"]
