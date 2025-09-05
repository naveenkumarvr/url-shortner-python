FROM python:3.9.23-bookworm
WORKDIR /apps
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# Set environment variables
ENV MYSQL_HOST=mysql
ENV REDIS_HOST=redis
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318/v1/traces"

ENTRYPOINT ["python", "./app.py"]