from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db import connection

from pierre.site_search.settings import SORT_MAPPINGS

# Adapted from http://www.djangosnippets.org/snippets/1328/
class IndexField (models.Field):
    """
    Field type used by Postgres for full-text indexing
    Uses the tsvector object, which is built into Postgres 8.3.
    Users of earlier versions can get the tsearch2 package here:
    www.sai.msu.su/~meg.../V2
    """
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['editable'] = False
        kwargs['serialize'] = False
        super(IndexField, self).__init__(*args, **kwargs)

    def db_type( self ):
        return 'tsvector'

def query(search_model, query, sort="relevance", app_label=None, model=None):
    assert sort in SORT_MAPPINGS.keys()
    query = connection.ops.quote_name(query)
    where=["index @@ plainto_tsquery(%s)"]
    params=[query,]
    if app_label and model:
        id = ContentType.objects.filter(app_label=app_label, model=model)[0].id
        where.insert(0, "content_type_id = %s")
        params.insert(0, id)            
    result = search_model.objects.extra(
        select_params=(query,),
        select = {'relevance': "ts_rank(index, to_tsquery(%s))"},
        where=where,
        params=params
    ).order_by(SORT_MAPPINGS[sort])
    return result

def update_index(sender, instance, created, **kwargs):
    if not hasattr(instance, "fields_to_index"):
        return        
    catalog = 'pg_catalog.english'
    if instance.fields_to_index == True:
        # If this prop is True, we assume all model fields should be indexed.
        data = " ".join([getattr(instance, field) for field in instance._meta.fields])
    else: 
        data = " ".join([getattr(instance, field) for field in instance.fields_to_index])
    content_type = ContentType.objects.get_for_model(instance)
    try:
        search = Search.objects.get(content_type__pk=content_type.id, object_id=instance.id)
    except Search.DoesNotExist:
        search = Search.objects.create(content_object=instance)
    
    search.title = instance.get_search_result_title()
    search.description = instance.get_search_result_description()
    search.date = instance.get_search_result_date() 
    search.url = instance.get_absolute_url()
    search.save()

    cursor = connection.cursor()
    sql = "update search_index set index = to_tsvector(%s, %s) where id = %s"
    cursor.execute(sql, (catalog, data, search.id))
    cursor.execute("COMMIT;")
    cursor.close()
