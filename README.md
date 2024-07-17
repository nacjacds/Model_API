# Model API

This repository contains a FastAPI-based web application for serving a machine learning model. The application allows users to predict outcomes, ingest new data, and retrain the model based on new data.

## Features

- **Prediction Endpoint**: Provides predictions based on input data.
- **Data Ingestion**: Allows new data to be ingested into the system.
- **Model Retraining**: Enables retraining of the model with newly ingested data.

## Endpoints

### 1. Predict
- **URL**: `/predict`
- **Method**: `POST`
- **Description**: Takes a list of features and returns a prediction.
- **Input Example**:

### 2. Ingest
URL: /ingest
Method: POST
- **Description**: Ingests new data into the database.

### 3. Retrain
URL: /retrain
Method: POST
- **Description**: Retrains the model using the data in the database.

### Testing with Postman
The API endpoints have been tested using Postman to ensure they work correctly. Postman allows for easy interaction with the API to verify functionality and troubleshoot issues.

### Docker Containerization
The application has been encapsulated in a Docker container to ensure consistency across different environments and to simplify deployment.
