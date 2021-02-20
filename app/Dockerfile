# pull official base image
FROM python:3.9.1-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk --no-cache add musl-dev linux-headers g++

# install dependencies
RUN pip install --upgrade pip
# install psycopg2 dependencies

COPY ./requirements.txt .

RUN pip install -r requirements.txt
COPY ./entrypoint.sh .

# copy project
COPY . ./
CMD ["/bin/bash","/usr/src/app/entrypoint.sh"]
