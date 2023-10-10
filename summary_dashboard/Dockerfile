# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster
RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update

LABEL maintainer="leojfrancis.now@gmail.com"
LABEL description="Django dashboard for node analysis"

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y --no-install-recommends install binutils libproj-dev gdal-bin netcat

WORKDIR /workspace
COPY requirements.txt .
COPY gunicorn.conf.py .
RUN pip install --no-cache --upgrade pip setuptools wheel
RUN pip install --no-cache -r requirements.txt

COPY ./scripts ./scripts
RUN chmod +x ./scripts/entrypoint.sh

ARG RE_BUILD=unknown
COPY . .

CMD [ "sh","./scripts/entrypoint.sh" ]
# CMD [ "sleep" ,"10000" ]