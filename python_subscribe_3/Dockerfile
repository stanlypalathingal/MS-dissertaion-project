#!/bin/bash
FROM python:3.7-slim

LABEL maintainer="stanlywilson@stvincentngp.edu.in"

ADD . /

RUN pip install --upgrade pip
RUN pip install --no-cache-dir "scikit-learn==0.22"
RUN pip install --no-cache-dir "pandas==0.25.3"
RUN pip install --no-cache-dir "numpy==1.17.4"

CMD ["python", "./trial_data3.py" ]

