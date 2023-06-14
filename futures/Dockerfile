FROM python:3.10-slim
WORKDIR app/
COPY requirements.txt .
ENV env .env
RUN pip install -r requirements.txt --no-cache-dir
COPY . futures
CMD ["python3", "futures/main.py"]