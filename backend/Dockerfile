FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY backend /app
ENV PYTHONUNBUFFERED=1
EXPOSE 5001
CMD ["python", "app.py"]

