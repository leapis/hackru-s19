FROM python:3.7-alpine

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt --no-cache-dir

RUN pyppeteer-install

ADD . /code
WORKDIR /code
