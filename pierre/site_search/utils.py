from django.db import connection
from django.db.models.loading import AppCache
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django import dispatch


def implements(implementor, implementee):
    """
    Verifies that the implementor has the same methods and properties as the
    implementee. __XXX__ classes are excluded. For the purposes of method
    comparison, arguemtn order is importent.
    
    >>> class Implementor(object):
    ...    foo = 1
    ...    def bar(self):
    ...        pass
    >>> class Implementee(object):
    ...    foo = 2
    ...    def bar(self):
    ...        pass    
    >>> implements(Implementor, Implementee)
    True
    >>> class NonImplementor(object):
    ...    foo = 1
    ...    bar = 5
    >>>implements(NonImplementor, Implementee)
    False
    
    """
    ia = [attr for attr in implementee.__dict__.keys() if not attr.startswith("__")]
    for attr in ia:
        if not hasattr(implementor, attr):
            return False
        if callable(getattr(implementee, attr)) and not callable(getattr(implementor, attr)):
            return False
    return True

class ISearchable(object):
    """
    Defines an interface which a model class must implement if it wishes to be 
    searchable. 
    """

    fields_to_index = tuple()
    
    def get_search_result_title(self):
        """Should return the "human-readable" representation of a record"""
        pass

    def get_search_result_description(self):
        """Should return the "human-readable" description of a record"""
        pass

    def get_search_result_date(self):
        """Should return a datetime object  if any for the item"""
        pass

    def is_searchable(self):
        """Returns True/False based on whether the item should be indexed."""
        pass

def get_searchable_models():
    """
    Returns a list of all models in the Django project which implement ISearchable
    """
    app = AppCache();
    return filter(lambda klass: implements(klass, ISearchable), app.get_models())
