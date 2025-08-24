FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Environment variables:
# - no .pyc files
# - unbuffered output (so pytest prints immediately)
# - add /app/src to Python path so "import toy_robot" works
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Install pytest (and any other dev deps if needed)
RUN pip install --no-cache-dir pytest

# Copy all project files into /app
COPY . .

# Default command: run all tests
CMD ["pytest", "-v"]
