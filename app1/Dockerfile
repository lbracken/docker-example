# Builds a Docker image to run docker-example-app1.  The base image will handle
# adding any application files and required dependencies to this image.

FROM lbracken/flask-app
MAINTAINER Levi Bracken <levi.bracken@gmail.com>

# Expose CherryPy WSGI server port for this application
EXPOSE 8080

# Run the CherryPy WSGI server when this container is started
CMD ["python", "server.py"]