# See https://hub.docker.com/u/qmentasdk/ for more base images
FROM ubuntu:bionic-20201119

RUN apt-get update -y && \
apt-get install -y wget && \
rm -rf /var/lib/apt/lists/* 

# Install the SMT v0.4 software
RUN wget https://github.com/ekaden/smt/releases/download/v0.4/smt-0.4-linux-x64.tar.gz
RUN tar -zxvf smt-0.4-linux-x64.tar.gz
RUN rm smt-0.4-linux-x64.tar.gz

COPY runSMT.sh /scripts/
RUN ["chmod","+x","/scripts/runSMT.sh"]

ENTRYPOINT ["/scripts/runSMT.sh"] 

