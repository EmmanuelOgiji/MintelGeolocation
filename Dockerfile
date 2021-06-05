# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ARG location_key
ARG weather_key
ENV LOCATION_API_KEY=$location_key
ENV WEATHER_API_KEY=$weather_key


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src .

CMD [ "python3", "main.py", "--ips", "ip_addresses.txt"]