FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt ./

RUN apt update && apt upgrade
RUN apt install -y build-essential curl g++ gcc gettext git make libc-dev libffi-dev memcached pkg-config wget
RUN apt install -y apt-transport-https ca-certificates dirmngr software-properties-common
RUN apt install -y python3-dev python3-pip python3-virtualenv default-libmysqlclient-dev python3-psycopg2
RUN apt install -y nodejs npm
RUN npm install -g bower less recess

RUN pip install --upgrade pip
RUN pip install --upgrade --no-cache-dir -r requirements.txt

COPY ./ddcore    ./ddcore
COPY ./settings  ./settings
COPY ./manage.py .
COPY ./urls.py .

RUN mkdir -p ./logs
RUN mkdir -p ./media
RUN mkdir -p ./static

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
