#!/bin/bash

# user
for i in {1..10}; do
    username="user$i"
    useradd -m $username
    echo "$username:$username" | chpasswd
done
echo "root:root" | chpasswd
useradd -m dev
echo "dev:devpass" | chpasswd

# apache
cp /blue/apache/ports.conf /etc/apache2/ports.conf
cp /blue/apache/default.conf /etc/apache2/sites-available/000-default.conf
mkdir -p /var/www/html/file-reader /var/www/html/ping-checker
cp -r /blue/file-reader/* /var/www/html/file-reader/
cp -r /blue/ping-checker/* /var/www/html/ping-checker/
cp /blue/apache/.htaccess /var/www/html/file-reader/.htaccess
cp /blue/apache/.htaccess /var/www/html/ping-checker/.htaccess
a2ensite 000-default.conf
apachectl start

# ssh
mkdir -p /run/sshd
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
/usr/sbin/sshd -D &

tail -f /dev/null