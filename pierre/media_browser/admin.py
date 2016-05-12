from django.contrib import admin
from django import forms

from models import Dimension, Image
    
class DimensionAdminForm(forms.ModelForm):
    class Meta:
        model = Dimension

    def clean(self):
        """Ensure that height and width are not both blank."""
        cleaned_data = self.cleaned_data
        height = cleaned_data.get("height")
        width = cleaned_data.get("width")
        if not width and not height:
            raise forms.ValidationError("Both width and height have been left"
                " blank. One or both must be filled out.")
        return super(DimensionAdminForm, self).clean()

class DimensionAdmin(admin.ModelAdmin):
    """An admin site object for media item dimensions"""
    form = DimensionAdminForm

class ImageAdmin(admin.ModelAdmin):
    """
    An admin site object for Images.
    """
    date_hierarchy = 'timestamp'
    list_display = ('preview', 'title', 'timestamp',)
    search_fields = ('title', 'caption', 'credit',)
    
    def __init__(self, *args, **kwargs):
        from admin_urls import urlpatterns
        self.urlpatterns = urlpatterns
        self.url_map = dict([(p.name, p.callback) for p in urlpatterns])
        super(ImageAdmin, self).__init__(*args, **kwargs)
        
    def preview(self, obj):
        attrs = {
            'title': obj.title,
            'alt': obj.caption,
            'src':  obj.image.url
        }
        MAX_DIMENSION = 200
        from math import ceil
        w = obj.image.width
        h = obj.image.height
        if w <= MAX_DIMENSION and h <= MAX_DIMENSION:
            attrs['height'] = h 
            attrs['width'] = w
        if w > MAX_DIMENSION:
            ratio = h * 1.0/w
            attrs['height'] = ceil(MAX_DIMENSION * ratio) 
            attrs['width'] = MAX_DIMENSION
        if h > MAX_DIMENSION:
            ratio = w * 1.0/h
            attrs['height'] = MAX_DIMENSION
            attrs['width'] = ceil(MAX_DIMENSION * ratio)
        return (
            '<img alt="%(alt)s" title="%(title)s" src="%(src)s"'
            'width="%(width)d" height="%(height)d" />'
        ) % attrs
    
    preview.allow_tags = True

admin.site.register(Image, ImageAdmin)
admin.site.register(Dimension, DimensionAdmin)