FROM python:3.12-slim-bookworm

WORKDIR /app

COPY server/requirements.txt .
RUN pip install --no-cache-dir --retries 5 --timeout 60 -r requirements.txt

COPY models.py .
COPY openenv.yaml .
COPY server/ ./server/
COPY static/ ./static/

EXPOSE 7860

CMD ["python", "server/app.py"]