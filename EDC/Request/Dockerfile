FROM arm32v7/python:3.7-slim-buster

RUN pip install --no-cache-dir "paho-mqtt" --extra-index-url=https://www.piwheels.org/simple
RUN pip install --no-cache-dir "asymcrypt" --extra-index-url=https://www.piwheels.org/simple

ADD Publish.py /
ADD Subscribe.py /
ADD priv.pem /
ADD deciderPub.pem /
ENTRYPOINT ["python","./Publish.py"]