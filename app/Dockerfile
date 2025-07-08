FROM python:3.9.23-bookworm
WORKDIR /apps
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "./app.py"]