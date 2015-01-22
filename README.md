#docker-example

This repo is a example multi-tiered application that runs as a series of Docker containers.  The application is built using NGINX as a reverse proxy to handle client requests, two Python based Flask apps to process requests, and a MongoDB database for persistence.  As illustrated below, each component runs as its own Docker container.

Instructions for building these images from Dockerfiles are below. The images are also automatically built and available on Docker Hub at https://registry.hub.docker.com/u/lbracken.

<pre>
                                  +---------+
                             +--> |  app1   |
             +---------+    /     +---------+     +---------+
(Client) --> |  NGINX  | --+----> |  app2   | --> | MongoDB |
             +---------+          +---------+     +---------+
</pre>


Working from right to left...

MongoDB
---------

Docker Hub provides and maintains base images for many popular applications, including MongoDB.  So we can just pull down the latest *mongo* image from Docker Hub.

	$ docker pull mongo

By default all data is stored inside this container.  However, using Docker volumes it's possible to store data on the host system or in another data specific container.  If on a Linux host, just create a directory to store this data.  If on a Mac or Windows host and using boot2docker, then you'll need to create this directory inside the boot2docker VM.

	$ boot2docker ssh
	$ mkdir -p /var/docker-volumes/mongo-data
	$ exit

Now we can start the *mongo* container. The `-v` flag maps the directory just created to the directory */data/db* inside the container.

    $ docker run -d --name mongo -v /var/docker-volumes/mongo-data:/data/db mongo --noprealloc --smallfiles

For more information on this image see: https://registry.hub.docker.com/_/mongo/


app1 & app2
-------------
Both *docker-example-app1* and *docker-example-app2* are very basic Flask apps.  Within each, `app.py` defines the Flask application and `server.py` supports running in the CherryPy WSGI server.  *docker-example-app2* takes the additional step of linking to the MongoDB container we previsouly started.

However, instead of building two similiar Docker images for both *docker-example-app1* and *docker-example-app2*, let's first create a generic base image called *flask-app*.  Our Flask applications can later extend from this base image.

*Run all of the following commands from the root of this repo, and replace lbracken with your name.*

Build the base image for Flask applications...

	$ docker build -t="lbracken/flask-app" flask-app

Build images for *app1* and *app2*...

	$ docker build -t="lbracken/docker-example-app1" app1
	$ docker build -t="lbracken/docker-example-app2" app2

Start *docker-example-app1* and *docker-example-app2* containers....

	$ docker run -d -P --name app1 lbracken/docker-example-app1
	$ docker run -d -P --name app2 --link mongo:db lbracken/app2

To access the apps, you'll need to figure out which port Docker mapped it to.  While the app runs on port 8080 inside the container, on the host system the `-P` flag binds it to a random high port.  If you're on a Mac or Windows system with boot2docker, you'll also need to find the container's IP.  

	$ docker ps app*
	$ boot2docker ip

You can then access the apps at the given IP and ports in your browser (ex: http://192.168.59.103:49160/).


Project TODOs
-------------
* Add nginx container and link to app1/app2
* Use Docker Compsoe or Fig to orchestrate it all together
* Deploying to AWS container service
* Documentation
