from django.contrib.contenttypes.models import ContentType
from django.db import connection

from pierre.site_search.models import Search

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
