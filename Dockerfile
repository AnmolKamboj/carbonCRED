# Use official Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV PIP_ROOT_USER_ACTION=ignore

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8080

# Start app with Gunicorn
CMD ["gunicorn", "--bind", ":8080", "wsgi:app"]
