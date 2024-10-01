FROM python:3.12-bullseye

RUN mkdir /var/www
WORKDIR /var/www
COPY ./ ./

RUN pip3 install -r requirements.txt

ENV LANG C.UTF-8

RUN chmod 755 -R /var/www
RUN adduser -u 1000 red
USER red

CMD ["uwsgi", "--ini", "/var/www/uwsgi.ini"]