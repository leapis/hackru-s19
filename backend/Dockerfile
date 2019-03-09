FROM python:3.7-alpine

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt --no-cache-dir

ADD . /code
WORKDIR /code
