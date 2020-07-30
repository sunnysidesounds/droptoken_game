FROM python:3.8.1

RUN mkdir /flask_app

WORKDIR /flask_app

ADD ./sql/yaits_sample_db.sql /docker-entrypoint-initdb.d
ADD . /flask_app

RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y procps

EXPOSE 5000

COPY ./entrypoint.sh /flask_app/entrypoint.sh
RUN chmod +x /flask_app/entrypoint.sh

ENTRYPOINT /flask_app/entrypoint.sh
