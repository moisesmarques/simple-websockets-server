FROM python:3.9-slim-buster as base

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

WORKDIR /backend

FROM base as dev

ENV PYTHONUNBUFFERED 1
ENTRYPOINT [ "./docker-entrypoint.sh" ]
