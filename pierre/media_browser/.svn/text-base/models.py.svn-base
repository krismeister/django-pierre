from django.db import models
from django.utils.translation import ugettext_lazy as _

class Dimension(models.Model):
    """
    This model allows users to specify dimensions for media items. A dimension
    can be either a "resize and crop" (both width and height are set) or just a
    "resize" (width *or* height are set, but not both. In the former option, 
    images are resized to the given width and any excess above the given height
    is cut from the bottom. If the image is shorter than the specified height
    when resized horizonatlly, then nothing is done: the image remains shorter
    then the sepcified crop height. 
    """
    name = models.CharField(_("Name"), max_length=255)
    width = models.IntegerField(_("Width"), 
        blank=True, 
        null=True, 
        help_text=_("In pixels")
    )
    height = models.IntegerField(_("Height"),
        blank=True, 
        null=True, 
        help_text=_("In pixels")
    )
    
    def __unicode__(self):
        if self.type == "resize and crop":
            return "%s (%d x %d)" % (
                self.name,
                self.width,
                self.height
            )
        elif not self.height:
            return "%s (%d pixels wide)" % (
                self.name,
                self.width
            )
        else:
            return "%s (%d pixels high)" % (
                self.name,
                self.height
            )
    
    @property
    def type(self):
        if self.width and self.height:
            return "resize and crop"
        else:
            return "resize"
    
    def save(self, force_insert=False, force_update=False):
        """
        This bit of validation is a last resort to ensure than width and 
        height are not both left blank.
        Django form validation is used in the admin to do this validation in a
        user-friendly way before it come to this nasty point of raising an 
        unhandled-exception; this overrdie of the model's "save" method merely 
        ensures that both fields are not left blank for cases where the form may
        not have been used. In those cases an unhandled exception is preferred 
        to allowing bad data.
        """
        if not self.width and not self.height:
            from django.db import IntegrityError
            raise IntegrityError, "A dimension must have a width and a height."
        else:
            super(Dimension, self).save(force_insert, force_update)
            

class MediaItem(models.Model):
    """This abstract class contains fields common to all Media types"""
    
    title = models.CharField(_("Title"), max_length=255)
    caption = models.TextField(_("Caption"), blank=True)
    credit = models.TextField(_("Credit"), blank=True)
    timestamp = models.DateTimeField(_("Last updated"), auto_now=True)
    
    croppable = False
    resizeable = False
    
    class Meta:
        abstract=True
    
def get_upload_path(instance, filename):
    """
    If MEDIA_BROWSER_UPLOAD_BASE is specified in the django project 
    settings, a subdirectory of that name in MEDIA_ROOT will hold
    all uploaded files. Otherwise, the subdirectory will be called 
    'media_browser_uploads'. Beneath that, files will be stored in sub-
    directories names by type of media item.
    If MEDIA_BROWSER_ORGANIZE_BY_DATE is set to True, then media items will
    further be organized in year/month/day sub folders.
    """
    from os import path
    from django.conf import settings
    from django.template.defaultfilters import slugify
    
    if hasattr(settings, 'MEDIA_BROWSER_UPLOAD_BASE'):
        base = settings.MEDIA_BROWSER_UPLOAD_BASE
    else:
        base = 'media_browser_uploads'
    type = slugify(instance._meta.verbose_name_plural)
    upload_path = path.join(base, type)
    # If MEDIA_BROWSER_ORGANIZE_BY_DATE is not set or is False, return 
    # current path:
    if not hasattr(settings, 'MEDIA_BROWSER_ORGANIZE_BY_DATE') \
    or settings.MEDIA_BROWSER_ORGANIZE_BY_DATE:
        return path.join(upload_path, filename)
    # Otherwise, put in dated subfolders:
    else:
        return path.join(upload_path, "%Y", "%m", "%d", filename)
    
class Image(MediaItem):
    """A model of an Image media item"""
    image = models.ImageField(_("Image"), upload_to=get_upload_path)
    
    croppable = True
    resizeable = True
    
    def __unicode__(self):
        return self.title

    
    @models.permalink
    def get_absolute_url(self):
        return ("media_browser:image", (), {'id': self.pk})  
        