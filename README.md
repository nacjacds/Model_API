# Model API

This repository contains a FastAPI-based web application for serving a machine learning model. The API provides sales predictions based on a company's marketing expenses in television, radio, and newspapers. You can also add data to the database in order to retrain the model.

## Project Structure
- **/data**: Contains the following data files:
  - Advertising.csv
  - advertising_model.pkl
  - test.db: SQLite database where marketing and sales data are stored.
- **README.md**: This file, which provides an overview of the project.
- **main.py**: Main FastAPI code defining the endpoints.
- **Dockerfile**: For running Docker.
- **test_api.py**: Tests for the API.

## Features

- **Prediction Endpoint**: Provides predictions based on input data.
- **Data Ingestion**: Allows new data to be ingested into the system.
- **Model Retraining**: Enables retraining of the model with newly ingested data.

## Endpoints

### 1. Predict
- **URL**: `/predict`
- **Method**: `POST`
- **Description**: Takes a list of features and returns a prediction using the trained model. Marketing expenses in "TV", "radio", and "newspaper" should be provided as query parameters.

### 2. Ingest
URL: /ingest
Method: POST
- **Description**: Allows adding new data for TV, radio, newspapers, and sales to the SQLite database. The ingested data is used to retrain the model.

### 3. Retrain
URL: /retrain
Method: POST
- **Description**: Retrains the model using all data stored in the database. After retraining, the updated model is saved to the file system for future predictions.

## Testing with Postman
The API endpoints have been tested using Postman to ensure they work correctly. Postman allows for easy interaction with the API to verify functionality and troubleshoot issues.

## Docker Containerization
The application has been encapsulated in a Docker container to ensure consistency across different environments and to simplify deployment.
- ### Docker Image Link: https://hub.docker.com/repository/docker/nacjacds/model-api/general
## Tools
- **FastAPI**: To build the API.
- **Pandas**: Library for data manipulation.
- **SQLite**: Database management system.
- **Pickle**: To save and load the trained model.
- **Postman**: To test the API endpoints.
- **Docker**: To deploy the API.
