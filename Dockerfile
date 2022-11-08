FROM python:3.9.12
ADD . /python-flask
WORKDIR /python-flask
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
