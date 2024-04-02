## Rhombus Infer Data Types

A simple web application for inferring data types from a CSV or XLSX files.

## Python Version - **3.11.6**

## Installation

The easiest way to run the app locally is by docker and docker compose since this app uses Redis.

### Options for installing docker

For Mac,

> Option 1: Installation of [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)

For Linux,

> Option 1: Installation of [Docker Desktop for Linux](https://docs.docker.com/desktop/install/linux-install/)

> Option 2: Installation of [Docker Engine for Linux Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

There are more ways to install docker. See full details of [docker here](https://docs.docker.com/manuals/)

### Options for installing docker compose

> Option 1: Install as [plug in](https://docs.docker.com/compose/install/linux/)

> Option 2: Install as [stand alone](https://docs.docker.com/compose/install/standalone/)

## Running locally for docker

If you installed docker compose as plug in,

```
docker compose up
```

If installed as stand alone,

```
docker-compose up
```

## _Notes_

You can add the `--build` flag when running to rebuild the images.

ex. `docker compose up --build` or `docker-compose up --build`

If you don't want to use docker, you are free to install manually.
This project uses [Celery](https://docs.celeryq.dev/en/stable/index.html) for background tasks.
So make sure to install a [broker](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#choosing-a-broker).
If you installed a broker besides Redis, please set the environment variable `CELERY_BROKER_URL`.

## Running manually

It is preferred to use a virtual environment when running local python applications.

Install requirements,
`pip3 install -r requirements.txt`

Run django app,
`python3 manage.py runserver`

Run celery,
`celery -A rhombus_api worker -l INFO`
