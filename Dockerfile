FROM python:3.8-slim-buster

ARG weather_key
ENV WEATHER_API_KEY=$weather_key
ENV MPLCONFIGDIR=/app/matlab


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src .

CMD [ "python3", "main.py", "--ips", "ip_addresses.txt"]