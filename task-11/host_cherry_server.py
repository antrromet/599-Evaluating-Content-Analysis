import os

import cherrypy

__author__ = "Antrromet"
__email__ = "antrromet@gmail.com"


class HostWebApp(object):
    @cherrypy.expose
    def index(self):
        return file('index.html')


if __name__ == "__main__":
    cherrypy.config.update(os.path.join(os.getcwd(), "app_config"))
    cherrypy.quickstart(HostWebApp(), config=os.path.join(os.getcwd(), "app_config"))
