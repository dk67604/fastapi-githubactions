# fastapi-githubactions

## Overview
This repository demonstrates how to set up a CI/CD pipeline for a FastAPI application using GitHub Actions. The pipeline includes steps for testing, packaging, and deploying the application to AWS Lambda.

## Features
- Automated CI/CD pipeline with GitHub Actions
- Deployment to AWS Lambda
- Python 3.12.9 support
- Virtual environment setup and caching
- Automated testing with pytest

## Installation
To set up the project locally, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/dk67604/fastapi-githubactions.git
    ```
2. Navigate to the project directory:
    ```bash
    cd fastapi-githubactions
    ```
3. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```
4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To run the FastAPI application locally:
```bash
uvicorn main:app --reload
