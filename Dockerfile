FROM apache/airflow:3.1.7-python3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard /app/dashboard
COPY database /app/database
COPY extraction /app/extraction
COPY transformation /app/transformation
COPY load /app/load
COPY dags /app/dags

RUN mkdir -p /app/data/bronze /app/data/silver /app/data/gold

ENV PYTHONPATH=/app
ENV AIRFLOW__CORE__DAGS_FOLDER=/app/dags
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

EXPOSE 8501 8080