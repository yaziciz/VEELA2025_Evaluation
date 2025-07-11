# Base image with Miniconda
FROM continuumio/miniconda3

# Set environment variables
ENV ENV_NAME=myenv
ENV PYTHON_VERSION=3.9.15

# Set working directory
WORKDIR /app

# Copy environment file into container
COPY environment.yml .

# Create conda environment from environment.yml
RUN conda install -y python=${PYTHON_VERSION} && \
    conda env create -n $ENV_NAME -f environment.yml && \
    conda clean -afy

# Use bash shell with conda activated
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Copy your source code
COPY . .

# Set default command (update to match your script)
CMD ["conda", "run", "-n", "myenv", "python", "receiver.py"]