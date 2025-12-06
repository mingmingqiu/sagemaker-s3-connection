import pandas as pd
import numpy as np
import boto3
import os

# AWS S3 setup
s3 = boto3.client('s3')
bucket_name = 'feature-engineering-bucket-989220949c9c'
dataset_key = 'Dataset/bank-additional-full.csv'  # S3 path of the dataset
output_key = 'processed_data/bank_additional_transformed.csv'  # S3 path for saving the output

# Download dataset from S3
def download_file_from_s3(bucket_name, key, download_path):
    s3.download_file(bucket_name, key, download_path)

# Feature engineering function
def feature_engineering(df):
    # Add a new feature: Square of age
    df['age_squared'] = df['age'] ** 2
    
    # Log transform the balance column
    df['balance_log'] = np.log(df['balance'] + 1)
    
    # One-hot encode categorical columns
    df = pd.get_dummies(df, columns=['job', 'marital', 'education'], drop_first=True)
    
    # Fill missing values with the column mean
    df.fillna(df.mean(), inplace=True)
    return df

# File path to store downloaded dataset temporarily
local_dataset_path = '/opt/ml/code/bank-additional-full.csv'
download_file_from_s3(bucket_name, dataset_key, local_dataset_path)

# Load dataset
df = pd.read_csv(local_dataset_path)

# Apply feature engineering
df_transformed = feature_engineering(df)

# Save the processed file back to S3
df_transformed.to_csv(f"s3://{bucket_name}/{output_key}", index=False)
print(f"Feature engineering complete. Processed file saved to: s3://{bucket_name}/{output_key}")
