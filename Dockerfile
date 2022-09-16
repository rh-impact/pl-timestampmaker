# Docker file for timestampmaker ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-timestampmaker .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-timestampmaker .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-timestampmaker
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-timestampmaker
#

FROM python:3.9.1-slim-buster
LABEL maintainer="barbacbd <bbarbach@redhat.com>"

WORKDIR /usr/local/src

COPY requirements.txt .

RUN pip install -r requirements.txt && \
    apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install ruby \
                       ffmpeg \
                       imagemagick \
                       tzdata && \
    rm -rf /var/lib/apt/lists/* && \
    gem install --no-document timestamp_maker -v 1.3.1

COPY . .

RUN pip install .

CMD ["timestampmaker", "--help"]
