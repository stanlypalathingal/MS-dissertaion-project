FROM python:3

ADD . /app 
WORKDIR . /app

RUN pip3 install --no-cache-dir pandas
RUN pip3 install --no-cache-dir numpy
RUN pip3 install --no-cache-dir sklearn

COPY requirements.txt ./
CMD ["python", "trial_data3.py" ]




FROM python:3.6.4-slim-jessie

RUN pip install pandas



FROM python:3.7-alpine

RUN echo "http://dl-8.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
  && apk update \
  && apk add py3-numpy py3-pandas


FROM python:3.7-alpine
RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk add --update --no-cache py3-numpy py3-pandas@testing


FROM python:3.6-alpine3.7

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev

RUN pip install --upgrade pip


docker run -v /home/stanlysac/Documents:/data decision:part2