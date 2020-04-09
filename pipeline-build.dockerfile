FROM python:3.7

COPY requirements.txt .

RUN apt-get update && apt-get install -y build-essential && apt-get install -y python-dev && apt-get install -y python3-setuptools

RUN pip install -r requirements.txt

RUN pip install awscli