# Use Oracle Python base image
FROM ghcr.io/oracle/oraclelinux8-python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY app.py .

CMD ["python3", "app.py"]