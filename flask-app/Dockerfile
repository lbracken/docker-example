# Builds a base Docker image to run a Flask application using the CherryPy WSGI server.
FROM ubuntu
MAINTAINER Levi Bracken <levi.bracken@gmail.com>

# Get and install required packages.
RUN apt-get update && apt-get install -y -q \
    git \
    python \
    python-dev \
    python-pip \
  && rm -rf /var/lib/apt/lists/*

# Install required dependencies for Flask and CherryPy
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Create a place to deploy the application
ENV APP_DIR=/var/www/app
RUN mkdir -p $APP_DIR
WORKDIR $APP_DIR

# In a downstream build, add the application files and install any additional dependencies
ONBUILD COPY requirements.txt $APP_DIR/
ONBUILD RUN pip install -r $APP_DIR/requirements.txt
ONBUILD COPY . $APP_DIR/