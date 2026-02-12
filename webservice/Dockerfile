FROM python:3.11-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
# Copy requirements first (better Docker caching)
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
&& rm -rf /var/lib/apt/lists/*
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy project files
COPY . .
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "app:app"]