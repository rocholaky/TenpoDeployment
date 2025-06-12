# TenpoDeployment

A production-ready machine learning model deployment solution using FastAPI, Docker, and Google Cloud Run. This project demonstrates how to deploy a PyTorch model as a scalable REST API with Infrastructure as Code (IaC) using Terraform.

## 🏗️ Architecture

This project implements a complete MLOps pipeline with the following components:

- **FastAPI Application**: High-performance REST API server for model inference
- **PyTorch Model**: Serialized model (`doubleit_model.zip`) loaded at startup
- **Docker Container**: Containerized application for consistent deployment
- **Google Cloud Run**: Serverless container platform for scalable deployment
- **Terraform**: Infrastructure as Code for reproducible cloud deployments
- **GitHub Actions**: CI/CD pipeline for automated deployments

## 📋 Prerequisites

Before running this project, ensure you have:

- Python 3.13+
- Docker
- Google Cloud Platform account
- Terraform >= 1.3
- Git

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TenpoDeployment
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Run the development server**
   ```bash
   uvicorn api.server:app --host 0.0.0.0 --port 8080 --reload
   ```

4. **Test the API**
   ```bash
   curl -X POST "http://localhost:8080/predict" \
        -H "Content-Type: application/json" \
        -d '{"inputs": [1.0, 2.0, 3.0]}'
   ```

### Docker Development

1. **Build the Docker image**
   ```bash
   docker build -t tenpo-ml-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8080:8080 tenpo-ml-api
   ```

## 📖 API Documentation

### Endpoints

#### POST `/predict`

Performs inference using the loaded machine learning model.

**Request Body:**
```json
{
  "inputs": [1.0, 2.0, 3.0, 4.5]
}
```

**Request Schema:**
- `inputs` (required): Array of float values for model inference
- Must be a non-empty list of floating-point numbers

**Response:**
```json
{
  "result": [2.0, 4.0, 6.0, 9.0]
}
```

**Error Response:**
```json
{
  "error": "Prediction failed"
}
```

**Status Codes:**
- `200`: Successful prediction
- `422`: Invalid request body (validation error)
- `500`: Internal server error during prediction

### Interactive API Documentation

When running locally, access the interactive API documentation at:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## 🏗️ Project Structure

```
TenpoDeployment/
├── api/                          # API source code
│   ├── server.py                # FastAPI application and endpoints
│   ├── api_payload.py           # Pydantic models for request validation
│   └── models/                  # ML model files
│       └── doubleit_model.zip   # Serialized PyTorch model
├── cloudrun-terraform/          # Terraform infrastructure code
│   ├── main.tf                  # Main Terraform configuration
│   ├── variables.tf             # Variable definitions
│   └── terraform.tfvars         # Variable values (not in repo)
├── .github/workflows/           # CI/CD pipeline
│   └── terraform.yml            # GitHub Actions workflow
├── tests/                       # Test files
│   └── test_api.py             # API tests
├── dockerfile                   # Docker container configuration
├── pyproject.toml              # Python project configuration
├── docker-compose.yml          # Local development with Docker Compose
├── up.sh                       # Development startup script
└── README.md                   # Project documentation
```

## ⚙️ Configuration

### Environment Variables

The application uses the following environment variables:

- `PORT`: Server port (default: 8080)
- `PYTHONPATH`: Python module path (set to `/app` in container)
- `PYTHONUNBUFFERED`: Disable Python output buffering

### Terraform Variables

Create a `cloudrun-terraform/terraform.tfvars` file with your specific values (not included in repository for security):

```hcl
project_id            = "my-gcp-project"
region               = "us-central1"
service_name         = "my-ml-api"
image_url            = "us-central1-docker.pkg.dev/my-project/my-repo/double_api:latest"
cloud_run_sa_email   = "my-service-account@my-project.iam.gserviceaccount.com"
```

**⚠️ Important:** The [`terraform.tfvars`](cloudrun-terraform/terraform.tfvars) file is excluded from version control (see [`.gitignore`](.gitignore:192)) for security reasons. You must create this file locally with your specific values.

## 🚢 Deployment

### Automated CI/CD Pipeline

This project uses GitHub Actions for fully automated CI/CD. When you push to the `main` branch, the following workflow is triggered:

1. **Build and Push to Google Artifact Registry** ([`deploy-to-gcp-registry.yml`](.github/workflows/deploy-to-gcp-registry.yml))
   - Builds the Docker image with the current timestamp and 'latest' tags
   - Pushes the image to Google Artifact Registry

2. **Deploy to Google Cloud Run with Terraform**
   - Automatically runs after the image is pushed
   - Uses Terraform to provision/update the Cloud Run service
   - Applies infrastructure changes with the latest image

### Required GitHub Configuration

To enable the CI/CD pipeline, configure:

1. **GitHub repository secrets:**
   - `GCP_CREDENTIALS`: Service account JSON key with appropriate permissions

2. **GitHub repository variables:**
   - `PROJECT_ID`: Your GCP project ID
   - `GCP_REGION`: Deployment region (e.g., `us-central1`)
   - `REPOSITORY`: Artifact Registry repository name
   - `service_name`: Cloud Run service name
   - `image_url`: Container image URL (including latest tag)
   - `cloud_run_sa_email`: Service account email for Cloud Run

### Manual Deployment (Development Only)

For local testing before pushing to main:

```bash
# Build and test locally
docker build -t tenpo-ml-api .
docker run -p 8080:8080 tenpo-ml-api

# Test Terraform plan (optional)
cd cloudrun-terraform
terraform init
terraform plan
```

### Infrastructure Components

The Terraform configuration creates:

- **Google Cloud Run Service**: Serverless container deployment
- **IAM Bindings**: Public access permissions for the API
- **Backend State**: GCS bucket for Terraform state management

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Test the deployed API:

```bash
curl -X POST "https://your-service-url/predict" \
     -H "Content-Type: application/json" \
     -d '{"inputs": [1.0, 2.0, 3.0]}'
```

## 🔧 Development

### Adding New Features

1. **API Endpoints**: Modify `api/server.py`
2. **Request Models**: Update `api/api_payload.py`
3. **Infrastructure**: Update Terraform files in `cloudrun-terraform/`
4. **Dependencies**: Add to `pyproject.toml`

### Code Style

The project follows Python best practices:
- Type hints for better code documentation
- Pydantic for data validation
- Structured JSON logging
- Error handling and proper HTTP status codes

### Logging

The application uses structured JSON logging with the following format:
```json
{
  "asctime": "2024-01-01T12:00:00Z",
  "severity": "INFO",
  "name": "APILogger",
  "message": "Prediction successful"
}
```

## 🔍 Monitoring and Observability

- **Logs**: Available in Google Cloud Logging
- **Metrics**: Cloud Run provides built-in metrics
- **Health Checks**: Automatic health monitoring
- **Error Tracking**: Errors logged with stack traces

## 🔖 Model and Data Versioning: 
 - For model and data versioning, eventhough its not implemented, we propose to use the DVC Framework which lets us keep track of the versions of both the model and the data in github without storing the actual data, but leaving space for experiment replication. 

## 🔒 Security

- **CORS**: Configured for cross-origin requests
- **Input Validation**: Pydantic validates all inputs
- **Error Handling**: Prevents information leakage
- **Service Account**: Least privilege access principle

## Version 0.1.0
- Initial release with FastAPI and PyTorch model serving
- Google Cloud Run deployment with Terraform
- CI/CD pipeline with GitHub Actions
- Docker containerization
- Comprehensive API documentation
