from django.conf.urls.defaults import *

urlpatterns = patterns('pierre.media_browser.views', 
    url(r'^(?P<id>[\d]+)/$', "image", name="image"),
    url(r'^preview/(?P<id>[\d]+)/$', "preview", name="preview"),
    url(r'^(?P<id>[\d]+)/thumb/(?P<dimension_id>[\d]+)/$', "resized_image", name="resized_image")
)    
