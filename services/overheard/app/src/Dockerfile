FROM php:7.2-apache

COPY composer.json /var/www/
COPY composer.lock /var/www/

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

RUN apt update && apt install -y git

WORKDIR /var/www

RUN composer install

COPY public/ /var/www/html/

WORKDIR /var/www/html

CMD ["php", "-S", "0.0.0.0:8080"]
