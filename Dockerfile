FROM python:3.10-alpine

RUN apk add --no-cache openssl-dev musl-dev libffi-dev libmagic gcc g++ cargo
RUN apk add --no-cache python3-dev libjpeg-turbo-dev zlib-dev
RUN apk add --no-cache git openssh
RUN pip install poetry


WORKDIR /app
COPY . /app

ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

EXPOSE 5001
CMD poetry install \
    && poetry run python -m scripts.populate_db \
    && poetry run flask run -h 0.0.0.0 -p 5001

