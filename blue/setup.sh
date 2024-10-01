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
cp /blue/apache/default.conf /etc/apache2/sites-available/000-default.conf
cp /blue/apache/index.php /var/www/html/index.php
cp /blue/apache/memo.txt /var/www/html/memo.txt
cp /blue/apache/.htaccess /var/www/html/.htaccess
chown -R www-data:www-data /var/www/html/
a2ensite 000-default.conf
apachectl start

# ssh
mkdir -p /run/sshd
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
/usr/sbin/sshd -D &

tail -f /dev/null