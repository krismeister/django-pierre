from django.views.generic import simple
from models import Search, SITE_SEARCH_DEFAULT_SORT
from settings import SORT_MAPPINGS
from __init__ import _ADAPTED_MODEL_CACHE

def index(request):
    if request.method == 'GET' and request.GET.get('query'):
        query = request.GET.get('query')
        #Sort by sort url parameter:        
        sort = request.GET.get('sort', SITE_SEARCH_DEFAULT_SORT)
        query_kwargs = {'sort': sort}
        sorts_list = get_sorts_list(request)
        
        ctype_filters = get_ctype_filters(request)
        #Filter by content type if URL param is set:        
        ctype_filter = request.GET.get('content_type')
        if ctype_filter and ctype_filter in [c['id'] for c in ctype_filters]:
            app_label, model = ctype_filter.split(".")
            query_kwargs['app_label'] = app_label
            query_kwargs['model'] = model
        results = Search.query(query, **query_kwargs)
        #FIXME: paginate results
        extra_context = {
            'results': results,
            'sorts': sorts_list,
            'filters': ctype_filters,
            'query_string': query            
        }
    else:
        extra_context = {'results': None}
    return simple.direct_to_template(request, 
        template="site_search/index.html",
        extra_context=extra_context
    )


# NB: the following are not view functions, but rather helper functions which
# help the "index" view construct controls dynamically for setting search 
# parameters (sorting and filtering by content type, respectively).

def get_sorts_list(request):
    """
    This function retuns a dictionary of parameters which will be needed to
    construct a menu of possible sorts.
    """
    # Copy the current request's QueryDict and use this copy to generate
    # url query strings for allowed sorts.
    query_dict = request.GET.copy()
    if query_dict.has_key('sort'):
        query_dict.__delitem__('sort')
    sorts = []
    for sort_name in SORT_MAPPINGS.keys():
        if sort_name != SITE_SEARCH_DEFAULT_SORT:
            # If the sort requested is the default one, it's preferable to
            # use a URL without the "sort" param as it's more friendly to 
            # upstream caches and avoids duplicative urls
            query_dict.__setitem__('sort', sort_name) 
        qs = request.path +  "?" +  query_dict.urlencode()
        q = {'qs': qs, 'active': request.GET.get('sort',SITE_SEARCH_DEFAULT_SORT) == sort_name,'name': sort_name}
        if sort_name == SITE_SEARCH_DEFAULT_SORT:
            sorts.insert(0, q)
        else:
            sorts.append(q)
        if query_dict.has_key('sort'):
            query_dict.__delitem__('sort') 
    return sorts    
        
def get_ctype_filters(request):
    """
    This function retuns a dictionary of parameters which will be needed to
    construct a menu of possible content type filters.
    """
    # Copy the current request's QueryDict and use this copy to generate
    # url query strings for allowed sorts.
    query_dict = request.GET.copy()
    has_reset = False;
    if query_dict.has_key('content_type'):
        has_reset = True
        query_dict.__delitem__('content_type')
    ctype_filters = []
    for model in _ADAPTED_MODEL_CACHE:
        id = "%s.%s" % (model._meta.app_label, model._meta.module_name)
        query_dict.__setitem__('content_type', id)
        ctype_filters.append({
            'title': model._meta.verbose_name_plural,
            'id': id,
            'url': request.path + "?" + query_dict.urlencode(),
            'active': id == request.GET.get('content_type')
        })
        query_dict.__delitem__('content_type')       
    #Sort in alpha order by title:    
    ctype_filters.sort(lambda x, y: cmp(x['title'], y['title']))
    if has_reset:
        ctype_filters.append({
            'title': "Show All",
            'id': None,
            'url': request.path + "?" + query_dict.urlencode(),
            'active': False
        })  
    return ctype_filters

