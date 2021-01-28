# See https://hub.docker.com/u/qmentasdk/ for more base images
FROM ubuntu:bionic-20201119

RUN apt-get update -y && \
apt-get install -y python3 python3-pip wget && \
rm -rf /var/lib/apt/lists/* 

# Install the DIPY package
RUN pip3 install dipy

# Copy the source files (only this layer will have to be built after the first time)
COPY wmti.py /scripts/


ENTRYPOINT ["/usr/bin/python3", "/scripts/wmti.py"] 

