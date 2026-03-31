FROM python:3.11-slim

WORKDIR /app

# Install uv for fast dependency management
RUN pip install uv

# Copy only the dependency files first to cache the installation step
COPY pyproject.toml uv.lock* ./

# Install project dependencies
RUN uv sync --no-dev --no-install-project

# Copy the rest of the application code
COPY . .

# Sync the project itself
RUN uv sync --no-dev

# Expose the port the app runs on
EXPOSE 8000

# Start the FastAPI application on the port Render provides
CMD ["sh", "-c", "uv run uvicorn src.myagent_news_api.app:app --host 0.0.0.0 --port ${PORT:=8000}"]
