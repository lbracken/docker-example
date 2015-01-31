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
Docker Hub provides and maintains official images for many popular applications, including MongoDB. So we can just pull down the latest *mongo* image from Docker Hub and start it up. By default all data is stored inside this container.

    $ docker run -d --name mongo mongo

For more information on this image see: https://registry.hub.docker.com/_/mongo/


app1 & app2
-------------
Both *app1* and *app2* are very basic Flask apps. *app2* takes the additional step of persisting data in MongoDB. We want to create a Docker image for both *app1* and *app2*.

However, instead of building two similiar Docker images for each app, let's first create a generic base image they can each extend. *flask-uwsgi* is that base image. It will install the required packages and dependencies to run a Flask application using the uWSGI application server. The builtin Flask server is great for development, but isn't recommended for production use. uWSGI is fast, light, production ready and interfaces well with nginx. For more info see: http://flask.pocoo.org/docs/0.10/deploying/uwsgi/ and http://uwsgi-docs.readthedocs.org/en/latest/. Be sure to also read the `Dockerfile` for *app1*, *app2* and *flask-uwsgi* to learn more about the setup.

To build the base image...

	$ docker build -t="lbracken/flask-uwsgi" flask-uwsgi

Build images for *app1* and *app2* from this base image...

	$ docker build -t="lbracken/docker-example-app1" app1
	$ docker build -t="lbracken/docker-example-app2" app2

Start *app1* and *app2* containers...  (notice we link *app2* to our running *mongo* container)

	$ docker run -d -P --name app1 lbracken/docker-example-app1
	$ docker run -d -P --name app2 --link mongo:db lbracken/docker-example-app2

The next logic step is to access and test out *app1* and *app2*. The quick way to do that is to jump ahead and start up the nginx container. Right now we can't just access them with a browser.  The reason is that by default we've asked uWSGI to run with the `socket` option which means it's just speaking the uwsig protocol. This is ideal for performance when we have a uwsgi capable webserver in front of it (like nginx). If we want the uWSGI server to response to HTTP requests, then we need to run with the `http` option.  See the the Dockerfiles for more details on how to switch this. For more info see: https://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html.


nginx
-------------
Docker Hub also provides an official image for nginx, so we'll start from that. We just need the image to use our custom nginx config files. One option is to mount the config files via a Docker volume. But let's just build our own nginx image, extending form the official image, to keep everything self contained and portable.

So what's in this custom nginx config? The primary config file, `nginx.conf`, provides basic info about how nginx should run. We haven't changed much here, though certain deployments may need to. The second config file, `docker-example.nginx.conf`, is more interesting. It contains configuration specific to our application. In this file you'll find some location directives that tell nginx how to route requests to certain URLs. For example...

    location /app1/ {
        include uwsgi_params;
        uwsgi_pass app1:5000;
        uwsgi_intercept_errors on;        
        uwsgi_param SCRIPT_NAME /app1;
        uwsgi_modifier1 30;
    }

    location /app1/static {
        alias /var/www/app1-static;
    }

The first location directive will route all requests with the URL path `/app1/` to a uwsgi server on the container *app1* on the port 5000. (If were running *app1* with the uWSGI `http` option instead of the `socket` option, we'd need to use `proxy_pass` here, but `uwsgi_pass` is more efficient). The second location directive will allow nginx to directly serve all resources on the URL path `/app1/static/`. This is more efficient than having nginx ask our uWSGI server for static resources, and why we took the trouble of exposing a volume on *app1* and *app2* and mount it in our *nginx* container.

For more on nginx configuration see http://wiki.nginx.org/Configuration and http://uwsgi-docs.readthedocs.org/en/latest/Nginx.html.

To build our *nginx* image...

	$ docker build -t="lbracken/docker-example-nginx" nginx

Start our *nginx* container.  We link it to the *app1* and *app2* containers, and also mount volumes in these containers which contain static resources that nginx will directly serve up.

	$ docker run -d -p 80:80 --name nginx --link app1:app1 --volumes-from app1:ro --link app2:app2 --volumes-from app2:ro lbracken/docker-example-nginx 

We can now access our *nginx* container and *app1* and *app2* with a browser by going to http://localhost, http://localhost/app1 and http://localhost/app2.  If using boot2docker, you'll need to access the boot2docker IP instead of `localhost`.  To find that IP...

	$ boot2docker ip


Running all containers on AWS Container Service
------------------------------------------------
AWS has rolled out a new container service (ECS) that will allow you to run and manage a set of Docker containers that run on EC2 instances.  The service is currently in preview and requires an invite.  It looks promising, however, the preview currently doesn't support volumes (see: https://twitter.com/mndoci/status/549647072358440964), so it can't run this docker-example project.

Below are notes for registering and running a task definition that includes a *monog* container and a modified form of *app2* (modified form just flipped the commented out CMD line to run uWSIG with http instead of socket and then built with image name quick-test-2). See `aws-task-definition.json` in this repo as well.  Once volumes are supported I'll update this section to run docker-example.

AWS Container Service Dev Guide: http://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html

To register this task definition...

  $ aws ecs register-task-definition --family docker-example --container-definitions file://aws-task-definition.json

To see the list of task definitions...

  $ aws ecs list-task-definitions

To start this task...

  $ aws ecs run-task --task-definition docker-example:1 --count 1

See waht tasks are running...

  $ aws ecs list-tasks

To get more information about the running task...

  $ aws ecs describe-tasks --task <task_UUID>