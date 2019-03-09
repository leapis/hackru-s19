FROM nitincypher/docker-ubuntu-python-pip

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt --no-cache-dir

RUN pyppeteer-install

ADD . /code
WORKDIR /code
