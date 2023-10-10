# syntax=docker/dockerfile

FROM nginx:1.23-alpine

USER root

COPY ./default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /vol/www/
RUN chmod 755 /vol/www/

# USER nginx