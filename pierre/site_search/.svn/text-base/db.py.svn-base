from django.utils.importlib import import_module
from django.db import backend

from psycopg2_backend import model

def import_backend_component(component_type):
    """
    This function acts as a kind of proxy which imports the correct search
    backend components based on the the db backend being used. It should always
    return an object with 3 attributes: a "SearchField" class, a "query" function 
    and an "update_index" function. This means any db backend must define these
    items.
    """
    db = backend.Database.__name__
    try:
        # This is kinda whack...but it works:
        search_backend = getattr(__import__("pierre.site_search.%s_backend" % db, {}, {},[component_type]), component_type)
    except ImportError, e:
        # Not likely SQLite will ever be supported...
        err = db == 'sqlite3' and "SQLite has no full text search capabilities. Please use another backend." or "This database backend (%s) has not been implemented yet." % db
        raise NotImplementedError, err     
    return search_backend

def get_signal_handler_backend():
    """The backend that we import must contain an update_index function"""
    signal_handlers = import_backend_component("signal_handlers")
    assert hasattr(signal_handlers, 'update_index') and callable(signal_handlers.update_index), "Backend does not define an 'update_index' function or it is not callable."
    return signal_handlers
    
def get_search_backend():
    """
    The backend that we import must contain an IndexField class and a query 
    function.
    """
    model = import_backend_component("model")
    assert hasattr(model, 'query') and callable(model.query), "Backend does not have a query object or it is not a function."
    assert hasattr(model, 'IndexField'), "Backend does not define an index field."
    return model