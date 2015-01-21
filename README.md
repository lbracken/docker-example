#docker-example

This repo is a example multi-tiered application that runs as a series of Docker containers.  The setup involves NGINX as a reverse proxy to handle client requests, two Python based Flask applications, and a mongoDB database.  As illustrated below, each component runs as its own Docker container.

<pre>
                                 +---------+
             +---------+    /--> |   app1  |
(Client) --> |  NGINX  | --|     +---------+     +---------+
             +---------+    \--> |   app2  | --> | mongoDB |
                                 +---------+     +---------+
</pre>

Working from right to left...

mongoDB
---------

Docker Hub provides and maintains base images for many popular applications, include mongoDB. No need to reinvent the wheel.  So pull down the latest *mongo* image from Docker Hub, then start it up.  Later we'll link to this container from other containers.  With the `-v` flag we'll mount a volume on the host to keep the DB data outside of the container, in this example at /tmp/mongo-data.  (If using boot2docker, data is stored inside the boot2docker VM instead of the host system)

    $ docker pull mongo
    $ docker run -d --name mongo -v /tmp/mongo-data:/data/db mongo

For more information on this image see: https://registry.hub.docker.com/_/mongo/



app1 & app2
-------------
Both *app1* and *app2* are very basic Flask applications.  Within each, `app.py` defines the Flask application and `server.py` supports running in the CherryPy WSGI server.  *App2* takes the additional step of linking to the mongoDB container we previsouly started.

Instead of building two similiar Docker images for both app1 and app2, let's create a generic base image called *flask-app*.  The images for *app1*, *app2* and any other Flask applications can then extend from this base image.

Instructions for building these images from Dockerfiles are below. The images are also available on Docker Hub at https://registry.hub.docker.com/u/lbracken.

*Run all of the following commands from the root of this repo, and replace lbracken with your name.*

Build the base image for Flask applications...

	$ docker build -t="lbracken/flask-app" flask-app

Build images for *app1* and *app2*...

	$ docker build -t="lbracken/app1" app1
	$ docker build -t="lbracken/app2" app2

Start *app1*, *app2* containers....

	$ docker run -d -P --name app1 lbracken/app1
	$ docker run -d -P --name app2 --link mongo:db lbracken/app2

To access the apps, you'll need to figure out which port Docker mapped it to.  While the app runs on port 8080 inside the container, on the host system the `-P` flag binds it to a random high port.  If you're on a Mac or Windows system with boot2docker, you'll also need to find the container's IP.  

	$ docker ps app*
	$ boot2docker ip

You can then access the apps at the given IP and ports in your browser (ex: http://192.168.59.103:49160/).


Project TODOs
-------------
* Run a mongoDB container
* Modify app2 to use mongoDB and link to its container
* Add nginx container and link to app1/app2
* Use Docker Compsoe or Fig to orchestrate it all together
* Deploying to AWS container service
* Documentation