FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/reports /app/services/data /app/services/data/research_cache

# Set permissions
RUN chmod +x /app/deployment/entrypoint.sh

# Expose ports
EXPOSE 8080 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python /app/services/control_interface.py dashboard || exit 1

# Set entrypoint
ENTRYPOINT ["/app/deployment/entrypoint.sh"]
CMD ["autonomous"]
