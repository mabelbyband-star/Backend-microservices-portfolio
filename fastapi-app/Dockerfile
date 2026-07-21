FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

#Note: --host 0.0.0.0 is important — it tells the server to accept connections 
#from outside the container, not just from inside it.