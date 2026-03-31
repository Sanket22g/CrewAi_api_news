FROM python:3.11-slim

WORKDIR /app

# Install uv for fast dependency management
RUN pip install uv

# Copy only the dependency files first to cache the installation step
COPY pyproject.toml uv.lock* ./

# Install project dependencies
RUN uv sync --no-dev

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Start the FastAPI application
CMD ["uv", "run", "uvicorn", "src.myagent_news_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
