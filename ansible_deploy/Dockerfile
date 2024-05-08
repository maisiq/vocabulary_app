FROM ubuntu:20.04

WORKDIR /srv
RUN apt-get update && apt-get install sshpass git pip -y
RUN pip install --no-cache-dir ansible
COPY ./requirements.txt ./requirements.txt