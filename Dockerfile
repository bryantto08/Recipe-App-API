FROM python:3.9-alpine3.13
LABEL maintainer="bryantto08"

ENV PYTHONUNBUFFERED 1

# Copies specific directories
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# Runs several commands:
# First creates venv, then upgrades pip
# Then installs dependencies in requirements.txt
# Then we remove tmp directory since its unnecessary
# Then we call adduser command (simple user, not admin)
# (not recommended to run app with root user if app gets compromised)
# if statement is a shell command
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin:$PATH"

USER django-user