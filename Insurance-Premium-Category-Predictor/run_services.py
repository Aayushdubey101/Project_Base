import subprocess
import time
import os
import signal
import sys

def run_services():
    # Start FastAPI backend
    backend = subprocess.Popen(
        ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    
    # Wait a bit for backend to initialize
    time.sleep(2)
    
    # Start Streamlit frontend
    frontend = subprocess.Popen(
        ["uv", "run", "streamlit", "run", "frontend.py", "--server.port", "8501", "--server.address", "0.0.0.0"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    def signal_handler(sig, frame):
        print("Shutting down...")
        backend.terminate()
        frontend.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Keep the script running
    backend.wait()
    frontend.wait()

if __name__ == "__main__":
    run_services()
