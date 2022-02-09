FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get install -y apt-utils

RUN apt-get install -y build-essential libssl-dev

RUN apt-get install -y git-core
RUN apt-get install -y dnsutils
RUN apt-get install -y curl
RUN apt install -y python3.8

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 10
RUN update-alternatives --config python

RUN apt-get install -y python3.8-distutils
RUN apt-get install -y python3.8-dev


RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py

RUN pip install -U pip setuptools
RUN pip install psutil

WORKDIR src/
COPY . /src

EXPOSE 11000

RUN pip install -r requirements.txt

CMD ["make", "start"]
