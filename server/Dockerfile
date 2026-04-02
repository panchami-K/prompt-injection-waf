FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY models.py .
COPY openenv.yaml .
COPY server/ ./server/

# Expose port
EXPOSE 8000

# Start the server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]