from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.utils.hashcompat import md5_constructor
from django.utils.http import urlquote

def compose(func_1, func_2, unpack=False):
    """
    compose(func_1, func_2, unpack=False) -> function

    The function returned by compose is a composition of func_1 and func_2.
    That is, compose(func_1, func_2)(5) == func_1(func_2(5))
    """
    if not callable(func_1):
        raise TypeError("First argument to compose must be callable")
    if not callable(func_2):
        raise TypeError("Second argument to compose must be callable")

    if unpack:
        def composition(*args, **kwargs):
            return func_1(*func_2(*args, **kwargs))
    else:
        def composition(*args, **kwargs):
            return func_1(func_2(*args, **kwargs))
    return composition

def invalidate_template_cache(fragment_name, *variables):
    args = md5_constructor(u':'.join(apply(compose(urlquote, unicode), variables)))
    cache_key = 'template.cache.%s.%s' % (fragment_name, args.hexdigest())
    cache.delete(cache_key)

def invalidate_view_cache(view_name, args=[], namespace=None, key_prefix=None):
    """
    This function allows you to invalidate any view-level cache. 
        view_name: view function you wish to invalidate or it's named url pattern
        args: any arguments passed to the view function
        namepace: if an application namespace is used, pass that
        key prefix: for the @cache_page decorator for the function (if any)
    """
    from django.utils.cache import get_cache_key
    from django.core.cache import cache
    # create a fake request object
    request = HttpRequest()
    # Loookup the request path:
    if namespace:
        view_name = namespace + ":" + view_name
    request.path = reverse(view_name, args=args)
    # get cache key, expire if the cached item exists:
    key = get_cache_key(request, key_prefix=key_prefix)
    if key:
        if cache.get(key):
            cache.set(key, None, 0)
        return True
    return False    
    