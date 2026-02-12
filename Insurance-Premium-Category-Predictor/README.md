# Insurance Premium Category Predictor

This application predicts the insurance premium category for individuals based on various health and demographic factors. It features a machine learning backend served via **FastAPI** and an interactive user interface built with **Streamlit**.

The application is fully containerized using **Docker** for easy deployment.

## Features

- **Predictive Model**: Estimates insurance premium tiers based on age, BMI, income, occupation, etc.
- **REST API**: Fast and efficient backend using FastAPI.
- **Interactive UI**: User-friendly web interface using Streamlit.
- **Dockerized**: Ready-to-use Docker container for seamless deployment.

## Tech Stack

- **Language**: Python 3.12
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **Package Manager**: uv
- **Containerization**: Docker

## Quick Start (Docker)

The easiest way to run the application is using Docker.

### Option 1: Pull from Docker Hub

If you want to run the pre-built image directly:

```bash
docker pull aayushdubey101/insurance-premium-category-predictor:latest
docker run -p 8000:8000 -p 8501:8501 aayushdubey101/insurance-premium-category-predictor:latest
```

### Option 2: Build Locally

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Insurance-Premium-Category-Predictor
   ```

2. **Build the Docker image**:
   ```bash
   docker build -t insurance-predictor .
   ```

3. **Run the container**:
   ```bash
   docker run -p 8000:8000 -p 8501:8501 insurance-predictor
   ```

Access the application at:
- **Frontend (UI)**: [http://localhost:8501](http://localhost:8501)
- **Backend (API Docs)**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Local Development (Without Docker)

To run the project locally, you need Python installed. We recommend using `uv` for dependency management, but `pip` also works.

### Prerequisites

- Python 3.12+
- `uv` (optional, but recommended)

### Setup

1. **Install dependencies**:
   ```bash
   # Using uv (Recommended)
   pip install uv
   uv sync

   # OR using pip
   pip install -r pyproject.toml  # Note: You might need to generate requirements.txt first if not using uv
   ```

2. **Run the Application**:
   The project includes a helper script `run_services.py` that launches both the FastAPI backend and Streamlit frontend.

   ```bash
   python run_services.py
   ```

   Unlike Docker, this script attempts to bind to `0.0.0.0`. If running locally on Windows/Mac, you might need to access `localhost` or `127.0.0.1`.

## API Endpoints

- `GET /`: Health check (Human readable).
- `GET /health`: Health check with model version status (Machine readable).
- `POST /predict`: Prediction endpoint.

**Request Body Example**:
```json
{
  "bmi": 25.5,
  "age_group": "25-30",
  "lifestyle_risk": "Low",
  "city_tier": "Tier 1",
  "income_lpa": 15.0,
  "occupation": "private_job"
}
```

## Project Structure

- `app.py`: FastAPI backend application.
- `frontend.py`: Streamlit frontend application.
- `run_services.py`: Script to run both services concurrently.
- `model/`: Contains the ML model and prediction logic.
- `schema/`: Pydantic models for API validation.
- `Dockerfile`: Configuration for building the Docker image.
