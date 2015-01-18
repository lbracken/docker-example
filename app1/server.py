# -*- coding: utf-8 -*-
from app import app
import cherrypy

if __name__ == '__main__':

    # Mount the application
    cherrypy.tree.graft(app, "/")

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = "0.0.0.0"
    server.socket_port = 8080
    server.thread_pool = 2
    server.thread_pool_max = 10

    # Subscribe this server
    server.subscribe()

    # Start the server engine
    cherrypy.engine.start()
    cherrypy.engine.block()