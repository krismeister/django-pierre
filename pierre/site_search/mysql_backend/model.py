from django.contrib.contenttypes.models import ContentType
from django.db import models

from settings import SORT_MAPPINGS

# from http://www.djangosnippets.org/snippets/1328/
class IndexField (models.TextField):
    """
    The MYSQL index field can just be a simple text field. 
    """
    pass

def query(search_model, query, sort="relevance", app_label=None, model=None):
    assert sort in SORT_MAPPINGS.keys()
    query = connection.ops.quote_name(query)
    #where=["index @@ plainto_tsquery(%s)"]
    where=["MATCH index AGAINST %s"]
    params=[query,]
    if app_label and model:
        id = ContentType.objects.filter(app_label=app_label, model=model)[0].id
        where.insert(0, "content_type_id = %s")
        params.insert(0, id)            
    result = search_model.objects.extra(
        select_params=(query,),
        #select = {'relevance': "ts_rank(index, to_tsquery(%s))"},
        select = {'relevance': "MATCH index AGAINST %s"},        
        where=where,
        params=params
    ).order_by(SORT_MAPPINGS[sort])
    return result