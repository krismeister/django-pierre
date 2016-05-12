from django.db.models.loading import cache
from django.db.models import signals
from django.db.models.base import ModelBase
from django.utils.importlib import import_module

from signal_handlers import update_index, delete_index, bulk_update_index
from utils import get_searchable_models

"""
How autodiscover works:
1. Import all instances of site_search.py in installed Django apps.
2. Importing will execute adapt_model() calls in site_search, adapting app
   models with the necessary metadata needed to index them.
3. Once models are adapted, register signals on them so that when the model is
   changes, the site_search.models.Search model (our search index) will be able
   mirror that change (adding or removing the record from the index).
"""

_ADAPTED_MODEL_CACHE = []

def register(model, mixin):
    """ 
    Copies relevant properties and methods from the search_mixin to the original
    model class. This is a little hackier than, say, using the mixin as an 
    actual mixin in the model's class declarartion, but it's the best way to 
    adapt models to be indexed programatically, which is the only way auto-
    discover can work.
    
    >>> class TestModel(ModelBase):
    ...     pass
    >>> class TestMixin():
    ...     __docstring__ = "do not copy"
    ...     mixin_prop = 5
    >>> adapt_model(TestModel, mixin=TestMixin)
    >>> instance = TestModel()
    >>> instance.mixin_prop
    5
    >>> instance.__docstring__ != "do not copy"
    true
    >>> TestModel in _ADAPTED_MODEL_CACHE
    True
    >>> class NotModel:
    ...     pass
    >>>try:
    ... adapt_model(NotModel, mixin=TestMixin)
    >>>except ValueError:
    ...     print 'Not a model class'
    'Not a model class'
    
    """
    if not isinstance(model, ModelBase):
        raise ValueError, "The class used for the model argument is not a django model."
    for key, value in mixin.__dict__.items():
        #Don't copy special python props:
        if not key.startswith("__"):
            model.add_to_class(key, value)        
    # Store all adapted models here, so that we don't have to call 
    # site_search.utils.get_searchable_models every time.
    _ADAPTED_MODEL_CACHE.append(model)


def register_signal_handlers():
    """
    Attaches post_save and post_delete handlers for all models which implement 
    ISearchable. 

    NB: Don't call this function until *after* models are adapted for search via
    adapt_model.
    """
    update_signals = ('post_save',)
    remove_signals = ('post_delete',)
    models = get_searchable_models()
    for model in models:
        for signal in update_signals:
            getattr(signals, signal).connect(update_index, sender=model)
        for signal in remove_signals:
            getattr(signals, signal).connect(delete_index, sender=model)

# A flag to tell us if autodiscover is running.  autodiscover will set this to
# True while running, and False when it finishes.
SITE_SEARCH_LOADING = False

def autodiscover():
    """
    Adapted from django.contrib.admin. Works in much the same way.
    
    Auto-discover INSTALLED_APPS site_search.py modules and fail silently when
    not present. This forces an import on them to register any site_search bits 
    they may want.
    """
    # Bail out if autodiscover didn't finish loading from a previous call
    global SITE_SEARCH_LOADING
    if SITE_SEARCH_LOADING:
        return
    SITE_SEARCH_LOADING = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        # For each app, we need to look for an site_search.py inside that app's
        # package. We can't use os.path here -- recall that modules may be
        # imported different ways (think zip files) -- so we need to get
        # the app's __path__ and look for site_search.py on that path.

        # Step 1: find out the app's __path__ Import errors here will (and
        # should) bubble up, but a missing __path__ (which is legal, but weird)
        # fails silently -- apps that do weird things with __path__ might
        # need to roll their own site search registration.
        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        # Step 2: use imp.find_module to find the app's site_search.py. For some
        # reason imp.find_module raises ImportError if the app can't be found
        # but doesn't actually try to import the module. So skip this app if
        # its site_search.py doesn't exist
        try:
            imp.find_module('site_search', app_path)
        except ImportError:
            continue

        # Step 3: import the app's site_search file. If this has errors we want them
        # to bubble up. By doing this import, we'll adapt existing models with
        # The additional data they need to be indexed and searched properly.
        import_module("%s.site_search" % app)
        
    
    # autodiscover was successful. Once all models are adapted for search, 
    # register signal handlers to index/deindex model records as needed, then
    # reset SITE_SEARCH_LOADING flag.
    register_signal_handlers()
    SITE_SEARCH_LOADING = False
