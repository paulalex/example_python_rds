Python-RDS Example application
=============================================================

This repository contains a sample `Flask` application running with a `uwsgi` server and
is intended for on-boarding applications to `kubernetes`.

You will find `kubernetes` deployment configuration, multi stage docker builds which run the unit
and integration tests in a test image, build a base image and a runtime image and `Jenkinsfile`
configuration for a sample pipeline build.

Unit tests can run locally against a `sqlite` database, as can local development. If you want to connect to a remote
database, currently only `postgres` by `SQLAlchemy` using the `psycopg` database driver is supported.

You can create a file in the root of the project called `dev.env` and add your database properties to this, these will 
be read in if the application is started with the environment variable `USE_DEV_ENV=True` set, supported configuration 
property names are listed below:

> DATABASE_URL=<my_db_url>

> DATABASE_ENGINE=<my_db_engine>

> DATABASE_PORT=<my_db_port>

> DATABASE_NAME=<my_db_name>

> DATABASE_USER=<my_db_user>

> DATABASE_PASSWORD=<my_db_password>


Quick start
==============

## Clone the repository

`https://github.com/paulalex/example_python_rds/example-python-rds.git`

Local Development
=================

Follow the steps below for local development using `python` standalone (no `docker`) and for building the build image and
the runtime image locally.

## Create a virtual environment and run python standalone against sqlite

• `mkvirtualenv -p python3 example-python-rds`

• `pip3 install -r requirements.txt`

• `ENVIRONMENT=LOCAL python run.py`

## Run python standalone against RDS

• `USE_DEV_ENV=True python run.py`

## Build image locally, tag and deploy to ECR

• `. mfa-clear`

• `mfa` Using awesume alias or custom script

• `aws ecr get-login --no-include-email`

• `docker login -u AWS -p <token>`

• `docker build -t x.dkr.ecr.eu-west-2.amazonaws.com/example-rds-python:build -f pipeline-build.dockerfile .`

• `docker push x.dkr.ecr.eu-west-2.amazonaws.com/example-rds-python:build`

• `docker build -t x.dkr.ecr.eu-west-2.amazonaws.com/example-rds-python:dev -f pipeline-runtime.dockerfile .`

• `docker push x.dkr.ecr.eu-west-2.amazonaws.com/example-rds-python:dev`

## Run container locally but use sqlite

`docker run -d -p5000:5000 -e "ENVIRONMENT=LOCAL" x.dkr.ecr.eu-west-2.amazonaws.com/example-rds-python:dev`

## Run container locally but use RDS

`docker run -d -p5000:5000 --env-file=dev.env x.dkr.ecr.eu-west-2.amazonaws.com/example-rds-python:dev`

## Database Migration

• Add `Flask-Migrate` to requirements.txt

• `pip install -r requirements.txt`

• `flask db migrate -m "Message"` # Create a migration file

• `flask db upgrade` # Perform the migration

Testing the application
========================

The application comes with some sample unit tests and integration tests using the `pytest` library. Integration tests
run against the `Flask` application using a `sqlite` database. To run the test suite:

## Run tests standalone against sqlite

• `pip3 install -r test_requirements.txt`

• `ENVIRONMENT=JENKINS pytest -s --junitxml=result.xml`

## Build test image and run tests locally in container

When the application is deployed via `Jenkins` a test container is build first (see `pipeline-test.dockerfile`) and 
tests run inside this container, you can simulate this locally with the command below:

• `docker build -t example-rds-python:test -f pipeline-test.dockerfile .`

Local Deployment to kubernetes to test config
==============================================

The application is designed to be deployed in a container to kubernetes and the config for the kubernetes deployments
can be found in the `deployment` folder in the root of the project.

• `kube_dev` (Or export your `KUBECONFIG`) 

• `./deploy.sh [args]`

For example:

`/deploy.sh dev master dev paoc-test-app.ckpj0be0i8x1.eu-west-2.rds.amazonaws.com postgres 5432 test-app-users postgres password123`
