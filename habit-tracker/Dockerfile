#1. Start from a base image with Python installed
FROM python:3.12
#2. Set the working directory in the container
WORKDIR /app
#3. Copy the requirements file into the container
COPY requirements.txt .
RUN pip install -r requirements.txt
#4. Copy the rest of the application code into the container,and tell Docker how to start the app
COPY habits.py .
CMD ["uvicorn", "habits:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
