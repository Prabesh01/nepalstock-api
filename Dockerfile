FROM python:latest
RUN mkdir /app
WORKDIR /app
ADD . /app
RUN python main.py
