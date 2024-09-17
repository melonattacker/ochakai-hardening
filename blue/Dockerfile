FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /blue

RUN apt-get update && \
    apt-get install -y \
    apache2 \
    php \
    libapache2-mod-php \
    php-mysql \
    openssh-server \
    iputils-ping \
    build-essential \
    net-tools \
    ufw \
    w3m \
    openssh-server && \
    apt-get clean

COPY . .
RUN chmod +x setup.sh

RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

EXPOSE 22 80 81

RUN a2enmod php8.3 && \
    a2enmod rewrite

CMD ["/blue/setup.sh"]