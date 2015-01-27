# Builds a Docker image to run docker-example-app2.  The base image will handle
# adding any application files and required dependencies to this image.
#
FROM lbracken/flask-uwsgi
MAINTAINER Levi Bracken <levi.bracken@gmail.com>

# Create a symlink with a unique name to the Flask app's static resources.
# This volume can then get mounted and used by another container.
RUN ln -s /var/www/app/static /var/www/app2-static
VOLUME /var/www/app2-static

# Expose the port where uWSGI will run
EXPOSE 5000

# If running this app behind a webserver using the uwsgi protocol (like nginx),
# then use --socket.  Otherwise run with --http to run as a full http server.
#CMD ["uwsgi", "--http", ":5000",         "--wsgi-file", "app.py", "--callable", "app", "--processes",  "2", "--threads", "4"]
CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--wsgi-file", "app.py", "--callable", "app", "--processes",  "2", "--threads", "4"]