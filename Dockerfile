FROM python:3.10-slim

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r requirements_api.txt

RUN airflow db init

RUN airflow webserver -p 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]