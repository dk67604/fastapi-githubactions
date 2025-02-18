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


# FastAPI CI/CD Pipeline with GitHub Actions

This document explains the CI/CD pipeline set up using GitHub Actions for deploying a FastAPI application to AWS Lambda.

---

## **What is CI/CD?**
**CI/CD (Continuous Integration and Continuous Deployment)** is a practice used in software development to automate the process of testing and deploying applications.

- **CI (Continuous Integration):** Ensures code changes are automatically tested.
- **CD (Continuous Deployment):** Deploys the application to a server automatically.

This pipeline automates the deployment of a FastAPI application using **GitHub Actions** and **AWS Lambda**.

---

## **GitHub Actions Workflow Overview**

This GitHub Actions workflow consists of two jobs:

1. **CI (Continuous Integration) Job** - Runs tests and creates a deployment package.
2. **CD (Continuous Deployment) Job** - Uploads the package to AWS and deploys it to Lambda.

### **Triggers**
- The pipeline runs on **every push to the `master` branch**, except for changes to `README.md`.

```yaml
on:
    push:
        branches:
            - master
        paths-ignore:
            - 'README.md'
```

---

## **1. CI Job: Continuous Integration**
This job runs on **Ubuntu** and performs the following steps:

### **1. Checkout the Code**
Fetches the latest version of the repository.

```yaml
- uses: actions/checkout@v2
```

### **2. Setup Python**
Installs Python 3.12.9.

```yaml
- name: Setup Python
  uses: actions/setup-python@v2
  with:
    python-version: '3.12.9'
```

### **3. Install Virtual Environment**
Installs `virtualenv` to create an isolated Python environment.

```yaml
- name: Install Python Virtual Environment
  run: pip3 install virtualenv
```

### **4. Cache the Virtual Environment**
Caches dependencies to speed up subsequent builds.

```yaml
- name: Virtual Environment
  uses: actions/cache@v3
  id: cache-venv
  with:
    path: venv
    key: ${{ runner.os }}-venv-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-venv-
```

### **5. Create and Activate Virtual Environment & Install Dependencies**
Sets up a virtual environment and installs required Python dependencies.

```yaml
- name: Activate Virtual Environment
  run: |
    python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

### **6. Run Tests**
Runs the test suite using `pytest`.

```yaml
- name: Run Tests
  run: source .venv/bin/activate && pytest
```

### **7. Package Dependencies**
Zips the installed dependencies.

```yaml
- name: Create archive of dependencies
  run: |
    cd .venv/lib/python3.12/site-packages
    zip -r9 ../../../../api.zip .
```

### **8. Add API Code to the Deployment Package**
Includes application files in the zip archive.

```yaml
- name: Add API files to Zip file
  run: |
    cd ./api && zip -g ../api.zip -r .
```

### **9. Upload Artifact**
Uploads the packaged API to GitHub for deployment.

```yaml
- name: Upload zip file artifact
  uses: actions/upload-artifact@v4
  with:
    name: api
    path: api.zip
```

---

## **2. CD Job: Continuous Deployment**
This job runs **after the CI job completes successfully** and deploys the API to AWS Lambda.

### **1. Configure AWS CLI**
Authenticates with AWS using credentials stored as GitHub Secrets.

```yaml
- name: Install AWS CLI
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-region: ${{ env.AWS_REGION }}
    role-to-assume: ${{ env.AWS_ROLE_TO_ASSUME }}
    role-session-name: GitHubActionsLambdaDeployment
```

### **2. Download the Deployment Package**
Fetches the zip file created in the CI job.

```yaml
- name: Download artifact
  uses: actions/download-artifact@v4
  with:
    name: api
```

### **3. Upload the Package to S3**
Uploads the API package to an AWS S3 bucket.

```yaml
- name: Upload to S3
  run: aws s3 cp api.zip s3://fastapi20250217/api.zip
```

### **4. Deploy to AWS Lambda**
Updates the AWS Lambda function with the new API package.

```yaml
- name: Deploy to Lambda
  run: aws lambda update-function-code --function-name fastapi --s3-bucket fastapi20250217 --s3-key api.zip
```

---

## **How the Pipeline Works**
1. **Push Code to GitHub:** Developers push changes to the `master` branch.
2. **CI Job:**
   - Python environment is set up.
   - Dependencies are installed.
   - Tests are executed.
   - API code is packaged.
   - The package is uploaded as an artifact.
3. **CD Job:**
   - AWS credentials are configured.
   - The package is downloaded.
   - The package is uploaded to an S3 bucket.
   - The AWS Lambda function is updated.

---

## **Key Benefits**
- 🚀 **Automated Deployment**: Eliminates manual work.
- 🛠 **Consistent Builds**: Ensures the application runs in a stable environment.
- ✅ **Automated Testing**: Catches issues before deployment.
- ⏳ **Faster Deployments**: Reduces downtime and increases efficiency.

---

## **Conclusion**
This CI/CD pipeline streamlines the deployment of a FastAPI application to AWS Lambda, ensuring code is tested and deployed seamlessly.

---

📌 **Author**: GitHub Actions CI/CD Pipeline Guide 🚀

