FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY vehicle.py .

CMD ["python3", "vehicle.py"]