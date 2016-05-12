from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from db import get_search_backend
"""
There are basically three things you need to tell the search mixin about the
particular model it is indexing.

1. What columns should be searched. You will very likely only want to search a
subset of fields. You specify this in the search_fields attribute. By default
(if this method is not overriden), every field in a model will be indexed.

2. Limiting factors on what records should be searched. For example, you might
not want to index unplublished blog entries. You sepecify and is_indexable
method, which takes the instance being saved as an argument and returns true os
false. The default is to index everything.

3. Describing how a record is to be represented. 

Many thanks to Andy McKay: http://www.agmweb.ca/blog/andy/category/18/
who had lots of good ideas to get me started
"""

try:
    from settings import SITE_SEARCH_DEFAULT_SORT
except ImportError:
    SITE_SEARCH_DEFAULT_SORT = 'relevance'

backend_specific = get_search_backend()

class Search(models.Model):
    """
    A model of a relation between an item and its index, and basic data about 
    each  item for display in a search result.
    """
    index = backend_specific.IndexField()
    date = models.DateTimeField(null=True)
    title = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()    
    content_object = generic.GenericForeignKey()
    
    query = backend_specific.query
    
    def __unicode__(self):
        """Useful for debugging, not much else."""
        fk_app = self.content_object._meta.app_label
        fk_model = self.content_object.__class__.__name__
        fk_str = self.content_object.__unicode__()        
        return u"%s.%s: %s" % (fk_app, fk_model, fk_str)    

    class Meta:
        db_table = "search_index"
        get_latest_by = "date"
        ordering = ("-date",)
         
    @classmethod
    def query(*args, **kwargs):
        """
        Simple pass-through to the db backend's query method.
        NB: there is a bit of subtlety involved here. As a classmethod, the 
        first argument this method get is the Search model class itself. 
        We pass this through to the query method becuase the query method will 
        need to act on it. This avoids a  reciprocal-import failure which would 
        arise if the db backend tried to import the Search model directly.
        """
        return backend_specific.query(*args, **kwargs);