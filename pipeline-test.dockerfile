FROM python:3.7

WORKDIR /app

COPY . .

RUN pip install -r test_requirements.txt

ENV ENVIRONMENT JENKINS

RUN pytest -s --junitxml=/app/result.xml



