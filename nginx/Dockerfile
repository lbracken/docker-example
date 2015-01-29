# Builds a Docker image, extending from the official nginx image, that contains
# custom configuration.
#
FROM nginx
MAINTAINER Levi Bracken <levi.bracken@gmail.com>

# Install custom nginx config
COPY nginx.conf /etc/nginx/
COPY docker-example.nginx.conf /etc/nginx/conf.d/
RUN rm /etc/nginx/conf.d/default.conf