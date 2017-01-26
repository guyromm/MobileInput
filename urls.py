# -*- coding: utf-8 -*-
'''
filedesc: default url mapping
'''
from routes import Mapper
from config import DEBUG
from noodles.utils.maputils import urlmap
import os

def get_map():
    " This function returns mapper object for dispatcher "
    map = Mapper()
    # Add routes here
    urlmap(map, [

                ('/', 'controllers#index'),
                ('/static/{path_info:.*}','noodles.utils.static#index', {'path': os.path.join(os.getcwd(), 'static')})
                #('/route/url', 'controllerName.actionName')     
            ])

    # Old style map connecting 
    #map.connect('Route_name', '/route/url', controller='controllerName', action='actionName')


    return map

