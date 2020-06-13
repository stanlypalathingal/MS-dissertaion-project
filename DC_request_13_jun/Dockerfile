FROM arm32v7/python:3.7-slim-buster

RUN apt-get -q update && \
	apt-get -qy install \ 
	libatlas-base-dev \
	libgomp1
RUN pip install --no-cache-dir "pandas==0.25.3" --extra-index-url=https://www.piwheels.org/simple
RUN pip install --no-cache-dir "scikit-learn==0.22" --extra-index-url=https://www.piwheels.org/simple
RUN pip install --no-cache-dir "paho-mqtt" --extra-index-url=https://www.piwheels.org/simple

ADD . /

EXPOSE 9003
ENTRYPOINT ["/bin/bash"]
RUN chmod a+x script.sh

CMD ["script.sh" ]