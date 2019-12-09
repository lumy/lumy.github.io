FROM python:3.5

RUN apt-get update && apt-get install --no-install-recommends -y make optipng nodejs npm libjpeg-turbo-progs
RUN npm install -g svgo
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
