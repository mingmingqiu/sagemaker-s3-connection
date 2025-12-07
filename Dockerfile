# Use an official base image for SageMaker (Python 3.6 with Ubuntu 18.04)
FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:2.5.1-cpu-py311-ubuntu22.04-sagemaker

# Set the working directory in the container
WORKDIR /opt/ml/code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    gcc \
    g++ \
    build-essential \
    libssl-dev \
    libffi-dev \
    libcurl4-openssl-dev \
    git \
    wget \
    && apt-get clean

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install pandas scikit-learn s3fs boto3 numpy

# Copy the feature engineering script into the container
COPY feature_engineering.py /opt/ml/code/

# Set the entrypoint to run the feature engineering script when the container starts
ENTRYPOINT ["python", "feature_engineering.py"]

# Expose the port if necessary (optional)
EXPOSE 8080
