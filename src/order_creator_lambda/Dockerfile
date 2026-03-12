FROM python:3.9

WORKDIR /app

COPY app.py .

RUN pip install boto3 psycopg2-binary

CMD ["python","app.py"]