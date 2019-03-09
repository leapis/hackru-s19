FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y curl software-properties-common && \
    curl -sL https://deb.nodesource.com/setup_10.x | bash -

RUN apt-get update && apt-get install -y python3 python3-pip

ADD requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt --no-cache-dir

RUN apt-get install -y nodejs

ADD . /code
WORKDIR /code

RUN cd get_site

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN cd get_site && npm install

RUN apt-get install -y gconf-service libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxss1 libxtst6 libappindicator1 libnss3 libasound2 libatk1.0-0 libc6 ca-certificates fonts-liberation lsb-release xdg-utils wget
