#docker-example

This repo is a example multi-tiered application that runs as a series of Docker containers.  The setup involves NGINX as a reverse proxy to handle client requests, two Python based Flask applications, and a mongoDB database.  As illustrated below, each component runs as its own Docker container.

<pre>
                                 +---------+
             +---------+    /--> |   app1  |
(Client) --> |  NGINX  | --|     +---------+     +---------+
             +---------+    \--> |   app2  | --> | mongoDB |
                                 +---------+     +---------+
</pre>

Dockerfiles to build these images are contained in this repo.  The images are also available to pull from Docker Hub -- https://registry.hub.docker.com/u/lbracken.


app1 & app2
-------------
Both *app1* and *app2* are very basic Flask applications.  Within each, `app.py` defines the Flask application and `server.py` supports running in the CherryPy WSGI server.  *App2* takes the additional steps of talking to a mongoDB instance.

Instead of building two similiar Docker images for both app1 and app2, let's create a generic base image called *flask-app*.  The images for *app1*, *app2* and any other Flask applications can then extend from this base image.

*Run all of the following commands from the root of this repo, and replace lbracken with your name.*

Build the base image for Flask applications...

	$ docker build -t="lbracken/flask-app" flask-app

Build images for *app1* and *app2*...

	$ docker build -t="lbracken/app1" app1
	$ docker build -t="lbracken/app2" app2

Run *app1* and *app2* containers...

	$ docker run -d -P --name app1 lbracken/app1
	$ docker run -d -P --name app2 lbracken/app2

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
