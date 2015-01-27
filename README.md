#docker-example

This repo is a example multi-tiered application that runs as a set of Docker containers.  The application is built using nginx as a reverse proxy to handle client requests, two Python based Flask apps to process requests, and a MongoDB database for persistence.  As illustrated below, each component runs as its own Docker container.

Instructions for building these images from included Dockerfiles are below. The images are also automatically built and available on Docker Hub at https://registry.hub.docker.com/u/lbracken.

<pre>
                                  +---------+
                             +--> |  app1   |
             +---------+    /     +---------+     +---------+
(Client) --> |  nginx  | --+----> |  app2   | --> | MongoDB |
             +---------+          +---------+     +---------+
</pre>


Working from right to left...

MongoDB
---------
Docker Hub provides and maintains base images for many popular applications, including MongoDB. So we can just pull down the latest *mongo* image from Docker Hub and start it up. By default all data is stored inside this container.

    $ docker run -d --name mongo mongo

For more information on this image see: https://registry.hub.docker.com/_/mongo/


app1 & app2
-------------
Both *app1* and *app2* are very basic Flask apps. *app2* takes the additional step of persisting data in MongoDB. We want to create a Docker image for both *app1* and *app2*.

However, instead of building two similiar Docker images for each app, let's first create a generic base image they can each extend. *flask-uwsgi* is that base image. It will install the required packages and dependencies to run a Flask application using the uWSGI application server. The builtin Flask server is great for development, but isn't recommended for production use. uWSGI is fast, light, production ready and interfaces well with nginx. For more info see: http://flask.pocoo.org/docs/0.10/deploying/uwsgi/ and http://uwsgi-docs.readthedocs.org/en/latest/. Be sure to also read the `Dockerfile` for *app1*, *app2* and *flask-uwsgi* to learn more about the setup.

To build the base image...

	$ docker build -t="lbracken/flask-uwsgi" flask-uwsgi

Build images for *app1* and *app2* from this base image...

	$ docker build -t="app1" app1
	$ docker build -t="app2" app2

Start *app1* and *app2* containers...  (notice we link *app2* to our running *mongo* container)

	$ docker run -d -P --name app1 app1
	$ docker run -d -P --name app2 --link mongo:db app2

The next logic step is to access and test out *app1* and *app2*. The quick way to do that is to jump ahead and start up the nginx container. Right now we can't just access them with a browser.  The reason is that by default we've asked uWSGI to run with the `socket` option which means it's just speaking the uwsig protocol. This is ideal for performance when we have a uwsgi capable webserver in front of it (like nginx). If we want the uWSGI server to response to HTTP requests, then we need to run with the `http` option.  See the the Dockerfiles for more details on how to switch this. For more info see: https://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html.


nginx
-------------
Coming soon...


Project TODOs
-------------
* Add nginx container and link to app1/app2
* Use Docker Compsoe / Fig to orchestrate it all together
* Deploying to AWS container service