# Use Python 3.12 slim image
FROM python:3.12-slim

# Install uv package manager
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies using uv
RUN uv sync

# Expose port for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Run the startup script
CMD ["python", "run_services.py"]
