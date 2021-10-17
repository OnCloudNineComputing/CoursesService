# syntax=docker/dockerfile:1

FROM python:3.9-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV DBHOST=oh-app-courses.c5sbmxpf4730.us-east-1.rds.amazonaws.com
ENV DBUSER=mysqluser
ENV DBPASSWORD=mysqluserve2170

CMD ["python3", "app.py"]