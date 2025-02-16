# Use a base image with Python 3.11
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Install uv (since it's not included by default)
RUN pip install uv

# Copy dependency files first (to leverage caching)
COPY pyproject.toml requirements.txt ./

# Create a virtual environment with uv and install dependencies
RUN uv venv && uv pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Ensure the virtual environment is activated and run FastAPI
CMD ["uv", "pip", "run", "uvicorn", "agent:app", "--host", "0.0.0.0", "--port", "8000"]