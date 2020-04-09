FROM texas-example-rds-python:build

RUN pip install uwsgi

WORKDIR /app

COPY . .

RUN chmod +x start.sh

EXPOSE 5000

ENTRYPOINT ["./start.sh"]