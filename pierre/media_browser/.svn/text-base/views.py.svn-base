from math import ceil
import mimetypes
from os import path
from urlparse import urlparse

from django.conf import settings
from django import forms
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, Template
from django.views.generic import simple

from sorl.thumbnail.main import DjangoThumbnail

from models import Image, Dimension
from utils import get_image_list_attributes, get_template_attributes, get_preview_attributes
from forms import StandardTemplateForm, ResizedImageForm, CKEditor, CKEDITOR_PATH


GROUP_SIZE = 5

def image(request, id=None):
    """ 
    A view of an image HTML snippet to be inserted into a rich text editor 
    """
    image = get_object_or_404(Image, id=id)
    # Calculate root-relative image src:
    url_pieces = urlparse(image.image.url)
    if len(url_pieces) >= 3:
        src = url_pieces[2]
    else:
        src = image.image.url
    return render_to_response(
        "media_browser/image_snippet.html", {
        'src': src,
        'height': image.image.height,
        'width': image.image.width,
        'caption': image.caption,
        'credit': image.credit,
        'title': image.title,
        'template': get_template_attributes(request, StandardTemplateForm)
    })

def preview(request, id=None):
    """ 
    A view of an image file 
    """
    image = get_object_or_404(Image, id=id)
    thumbnail = DjangoThumbnail(
        image.image.path.replace(settings.MEDIA_ROOT + path.sep, ""),
        (150, 150),
    )
    mimetype = mimetypes.guess_type(thumbnail.dest)[0]
    kwargs = {}
    if mimetype:
        kwargs['mimetype'] = mimetype
    resized_file = open(thumbnail.dest, 'r')
    return HttpResponse(resized_file.read(), **kwargs)

def resized_image(request, id=None, dimension_id=None):
    """
    A view of a cropped image HTML snippet to be inserted into a rich text 
    editor. 
    """
    image = get_object_or_404(Image, id=id)
    dimension = get_object_or_404(Dimension, id=dimension_id)
    # Sorl takes a size param of the form "(h)x(w)", which we'll calculate:
    if dimension.type == 'resize':    
        if dimension.width:
            ratio = 1.0 * image.image.height/image.image.width
            height = ceil(ratio * dimension.width)
            size = "%dx%d" % (dimension.width, height)
        if dimension.height:
            ratio = 1.0 * image.image.width/image.image.height
            width = ceil(ratio * dimension.length)
            size = "%dx%d" % (dimension.length, width)
    else:
        # Height and width are both set so we'll be cropping:
        size = "%dx%d" % (dimension.width, dimension.height)
    # Calculate root-relative image src:
    url_pieces = urlparse(image.image.url)
    if len(url_pieces) >= 3:
        src = url_pieces[2]
    else:
        src = image.image.url
    # Calculate root-relative MEDIA_URL:
    root_rel_media_url = urlparse(settings.MEDIA_URL)[2]
    return render_to_response(
        "media_browser/resized_image_snippet.html", {
        'full_image_url': src,
        'root_rel_media_url': root_rel_media_url,
        'image': image.image,
        'height': size.split("x")[1], 
        'width': size.split("x")[0],
        'size': size,
        'caption': image.caption,
        'credit': image.credit,
        'title': image.title,
        'template': get_template_attributes(request, ResizedImageForm)
    })

    
###############################################################################
#                                Admin Views
###############################################################################

def image_list(request):
    """A view for a list of images in a js editor plugin"""
    images = Image.objects.all()
    grouped_images = get_image_list_attributes(images, group_by=GROUP_SIZE)
    return simple.direct_to_template(request, 
        template="media_browser/admin/image_list.html",
        extra_context={
            'images': grouped_images,
            'CKEDITOR_PATH': CKEDITOR_PATH
        }
    )    

def image_search(request):
    """A view for a search of images in a js editor plugin"""
    search_term = request.GET.get('search')
    imgs = []
    if search_term:
        for field in ['title', 'caption', 'credit']:
            arg = "%s__icontains" % field
            [imgs.append(m) for m in Image.objects.filter(**{arg: search_term})]
        imgs = get_image_list_attributes(imgs, group_by=GROUP_SIZE)
    return simple.direct_to_template(request, 
        template="media_browser/admin/image_search.html",
        extra_context={
            'images': imgs,
            'search_term': search_term,
            'CKEDITOR_PATH': CKEDITOR_PATH
        }
    )    

def image_template(request, id=None):
    """A view for templating an image in a js editor plugin"""
    image = get_object_or_404(Image, id=id)
    preview = get_preview_attributes(image)
    return simple.direct_to_template(request, 
        template="media_browser/admin/image_template.html",
        extra_context={
            'image': image, 
            'preview': preview,
            'form': StandardTemplateForm(),
            'CKEDITOR_PATH': CKEDITOR_PATH
        }
    )
    

def image_resize(request, id=None):
    """A view for resizing an image in a js editor plugin"""
    image = get_object_or_404(Image, id=id)
    preview = get_preview_attributes(image)
    dimensions = Dimension.objects.all()
    return simple.direct_to_template(request, 
        template="media_browser/admin/image_resize.html",
        extra_context={
            'image': preview, 
            'dimensions': dimensions,
            'form': ResizedImageForm(),
            'CKEDITOR_PATH': CKEDITOR_PATH
        }
    )

def image_chooser(request, id=None):
    """ A view for choosing an image from the list """
    images = Image.objects.all()
    grouped_images = get_image_list_attributes(images, group_by=GROUP_SIZE)
    return simple.direct_to_template(request, 
        template="media_browser/admin/image_chooser.html",
        extra_context={
            'images': grouped_images,
            'is_chooser_view': True,
            'CKEDITOR_PATH': CKEDITOR_PATH
        }
    )     