from django.conf.urls.defaults import *

urlpatterns = patterns('pierre.media_browser.views', 
    url(r'^edit/$', 'image_list', name="image_list"),
    url(r'^find/$', 'image_search', name="image_search"),
    url(r'^edit/(?P<id>\d+)/?$', 'image_template', name="image_template"),
    url(r'^resize/(?P<id>\d+)/?$', 'image_resize', name="image_resize"),
    url(r'^choose/$', 'image_chooser', name="image_chooser"),    
)
