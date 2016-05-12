================================
Intro
================================

This application works by leveraging the full text search capabilities of 
the RDBMS that Django supports. It handles indexing and searching of models, 
and can be added to an existing Django project easily.

================================
Requirements
================================

* Django 1.1
* Python 2.4 or higher

**RDBMS:**

* MySQL (MyISAM only)
* Postgres
* (Coming soon: Oracle, SQL Server)

================================
Installation and Setup
================================

This section provides information about installing site search in your django app
and geting it setup to begin indexing your models. 

Overview
--------

There are five steps in activating the site_search

    1. Add ``pierre.site_search`` to your ``INSTALLED_APPS`` setting.

    2. Determine which of your application's models should be searchable.

    3. For each of those models, create an ``EntrySearchMixin`` class that
       encapsulates the customized search functionality and options for that
       particular model.

    5. Hook the ``site_search`` instance into your URLconf.
    
    4. Instantiate the ``site_search`` app and tell it about each of your 
        models and ``EntrySearchMixin`` classes.    
    
Step 1: Installing ``pierre``
---------------------------------
The *pierre* in ``pierre.site_search`` references a whole package of Django utilities of which ``site_search`` 
is only a part. For now though, none of those are available for public release, so the ``pierre`` package
just contains one module: ``site_search``.

Step 2: Decide which models you want to index
-----------------------------------------------------
Any model is a candidate for being indexed, although only Django model fields which are stored in databases as text 
are can be indexed by ``site_search``. This includes: :class:`CharField`, :class:`TextField`, and any field which 
inherits from those (e.g. :class:`EmailField`)

Step 3: Creating ``EntrySearchMixin`` objects
----------------------------------------------------------

.. class:: EntrySearchMixin

The ``EntrySearchMixin`` class is the representation of a model to the site
search. These must be stored in a file named ``site_search.py`` in each Django 
application that contains models you wish to search (similar to the way admin.py
functions for the Django admin app). Let's take a look at a simple example 
of the ``EntrySearchMixin``::

    from pierre.site_search.base_mixins import SearchableMixin
    from pierre import site_search
    from myproject.myapp.models import Entry
    
    class EntrySearchMixin(SearchableMixin):
        """A mix-in for a blog entry"""
        
        fields_to_index  = ('headline', 'summary', 'body')
        
        def is_searchable(self):
            return self.published
        
        def get_search_result_title(self):
            return self.headline
        
        def get_search_result_description(self):
            return self.summary
    
        def get_search_result_date(self):
            return self.pub_date
    
    site_search.register(Entry, EntrySearchMixin)

The classes you define which inherit EntrySearchMixin, will, as the name 
suggests be mixed in with existing model classes, extending them to provide 
metadata about how the site search app should index models. 
    
``SearchableMixin`` Options
----------------------------

The ``SearchableMixin`` class is fairly flexible. It has several options for 
dealing with customizing how models are indexed and searched. All options are 
defined on the ``SearchableMixin`` subclass.

.. attribute:: SearchableMixin.fields_to_index

This attribute is a list of fields in your model to index. This attribute must 
be specified. By default, no fields of a model will be indexed. 

.. method:: SearchableMixin.is_searchable

This method will be called on your model to determine if a particular record
should be indexed. For example, you would not want to index unpublished blog
entries. 

Example::

    class EntrySearchMixin(SearchableMixin):
        """A mix-in for a blog entry"""
        
        def is_searchable(self):
            return self.published

This example returns the contents of a boolean field on our example Blog entry
model called "published:. If published is True, the site search app will index
the entry.

.. method:: SearchableMixin.get_search_result_title

A search result has two pieces, a title and a description. It is up to you to
define how your model will provide these items, which are then stored in the 
search index. 

Example::

    class EntrySearchMixin(SearchableMixin):

        def get_search_result_title(self):
            return self.headline

In the above example, the search description is taken from Entry model's 
"headline" field.

.. method:: SearchableMixin.get_search_result_description

A search result has two pieces, a title and a description. It is up to you to
define how your model will provide these items, which are then stored in the 
search index. 

Example::

    class EntrySearchMixin(SearchableMixin):

        def get_search_result_description(self):
            return self.summary

In the above example, the search description is taken from Entry model's 
"summary" field.

.. method:: SearchableMixin.get_search_result_date

If you wish to be able to sort search results by date, have the method return 
a datetime object from you model. By default, this returns None. Models which
do not have a date associated with them need not define this method.

Example::

    class EntrySearchMixin(SearchableMixin):

        def get_search_result_date(self):
            return self.pub_date

Step 4: Hooking Models Into the Site Search application
-------------------------------------------------------

Hooking ``Site Search`` instances into your URLconf
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The last step in setting up the site search is to hook your ``Site Search``
instance into your URLconf. Do this by pointing a given URL at the
`site_search.views.index`` function.

In this example, we register our ``Site Search`` instance
``pierre.site_search.admin.site`` at the URL ``/search/`` ::

    # urls.py
    from django.conf.urls.defaults import *

    urlpatterns = patterns('',   
        (r'^search/', 'pierre.site_search.views.index'),
    )

At this point, the site search app only has one view, so that's all you need
to configure in your URLconf file. 

Finally, we need to automatically load the ``INSTALLED_APPS`` site_search.py
modules. This code will do that::

    from pierre import site_search
    
    site_search.autodiscover()

This should look very similar to the way the ``django.contrib.admin`` 
application is used. The difference is that the admin auto-discover code is
usually placed in the main urls.py file of a Django project. However, that code
is not executed until the first Django reqest/response cycle occurs, which is much too
late for our site search app. To ensure that ``site_search.autodiscover()`` is 
executed while the Django application is starting up, it is reccomended that you 
place this code in the __init__.py file located in the root directory of your 
Django project. That way, it will be executed once at startup.

Congrats, you should be ready to go. 

Indexing existing records.
-------------------------------------------------

All records added to your DB after site search has been installed will be 
indexed, updated and de-indexed automatically. However, records that existed in 
your database prior to installation of ``pierre.site_search`` will not be indexed
automatically. You can solve this problem by manually re-indexing your models. A
helper function called ``bulk_update_index`` will do this for you. The best way to
invoke it is from within the Django shell::

    $> ./manage.py shell
    Python 2.5.1 (r251:54863, Feb  6 2009, 19:02:12) 
    [GCC 4.0.1 (Apple Inc. build 5465)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> from pierre.site_search import bulk_update_index
    >>> bulk_update_index()
    Indexing Entry from test.apps.blog.models...
    <class 'class.apps.blog.models.Entry'>
    
    [...]
    
    Indexing Article from test.apps.article.models...
    <class 'class.apps.articles.models.Article'>
    Done. 5 records were indexed.
