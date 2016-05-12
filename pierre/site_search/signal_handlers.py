from django.contrib.contenttypes.models import ContentType

from db import get_signal_handler_backend
from models import Search
from utils import get_searchable_models

# The method used to update the index will vary by backend:
update_index = getattr(get_signal_handler_backend(), 'update_index')

def delete_index(sender, instance, **kwargs):
    """
    This function recieves signals from models that are being indexed and
    remove associated indecies from the search index model.
    
    Becuase this signal handler does not depend on any particular DB backend,
    (unlike the update_index function) is can be defined here rather than in a 
    specific DB backend module.
    """
    if not hasattr(instance, "fields_to_index"):
        return
    content_type = ContentType.objects.get_for_model(instance)
    search = Search.objects.get(content_type__pk=content_type.id, object_id=instance.id)
    search.delete()

def bulk_update_index(verbose=True):
    """
    A convinience function that can be used to resync the index after data has
    been manually added to tables which you application models (via the 
    direct execution of SQL commands,some other non-Django application or after 
    using your RDMBS' importing functions).
    
    Keep in mind, this is a fairly naive implementation, so if your tables are
    regularly being updated by a non-django process, it would be preferrable
    to find some other way of notifying site_search only of the records it needs
    to re/index rather than by checking every record in every search-indexed
    model to see if it needs resyncing, as this does.
    
    Becuase this signal handler does not depend on any particular DB backend,
    (unlike the update_index function) is can be defined here rather than in a 
    specific DB backend module.
    """
    models = get_searchable_models()
    count = 0
    for model in models:
        if verbose:
            print "Indexing %s from %s..." % (model.__name__, model.__module__)
        print model
        for instance in  model.objects.all():
            update_index(None, instance, None)
            if verbose:
                count += 1
        if verbose:
            print "Done. %d records were indexed." % count
    