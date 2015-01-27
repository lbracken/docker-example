# Builds a base Docker image to run a Flask application using the uWSGI
# application server.
#
# !!! Requirements for the downstream build !!!
#
#  (1) Declare a CMD instruction to start the uWSGI application server.
#      For example:
#        CMD ["uwsgi", "--http :5000 --wsgi-file app.py --callable app --processes 2 --threads 4"]
#
#        If running behind a webserver using the uwsgi protocol (like nginx)
#        then use `--socket` instead of `--http`.
#
#      For more info, see:
#        https://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html
#        http://uwsgi-docs.readthedocs.org/en/latest/Nginx.html
#
#  (2) Expose the port uWSGI will run on.
#      For example:
#        EXPOSE 5000
#
# TODOs for this Dockerfile...
#  * See about running uWSGI as a non-root user
#
FROM debian:wheezy
MAINTAINER Levi Bracken <levi.bracken@gmail.com>

# Get and install required packages.
RUN apt-get update && apt-get install -y -q \
    build-essential \
    python-dev \
    python-pip \
  && rm -rf /var/lib/apt/lists/*

# Install required dependencies (includes Flask and uWSGI)
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Create a place to deploy the application
ENV APP_DIR /var/www/app
RUN mkdir -p $APP_DIR
WORKDIR $APP_DIR

# When building a downstream image, copy the application files and then setup
# additional dependencies. It's assumed the application files are present in
# the same directory as the downstream build's Dockerfile.
ONBUILD COPY . $APP_DIR/
ONBUILD RUN pip install -r $APP_DIR/requirements.txt