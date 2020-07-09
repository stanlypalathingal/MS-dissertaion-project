FROM python:3.7-slim

ADD . /

RUN pip install --upgrade pip
RUN pip install --no-cache-dir "scikit-learn==0.22"
RUN pip install --no-cache-dir "pandas==0.25.3"
RUN pip install --no-cache-dir "paho-mqtt"
RUN pip install --no-cache-dir "pymongo"

EXPOSE 9006

ENTRYPOINT ["/bin/bash"]
RUN chmod a+x script.sh

CMD ["script.sh" ]
