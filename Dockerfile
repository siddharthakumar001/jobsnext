# TALENTNEXT/Dockerfile

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libmariadb-dev-compat libmariadb-dev netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
# Increase the timeout to 100 seconds
RUN pip install --default-timeout=100 -r requirements.txt

# Copy project
COPY . /app/

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
