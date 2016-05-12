from itertools import chain, repeat, izip
from math import ceil
from os import path

from django.conf import settings

def get_image_list_attributes(image_object_list, group_by=None):
    """
    Creates a dictionary of image parameters for a QuerySet of images.
    """
    processed_image_list = []
    for image in image_object_list:
        processed_image_list.append({
        'image': image.image,
        'src': image.image.path.replace(settings.MEDIA_ROOT + path.sep, ""),
        'caption': image.caption,
        'title': image.title,
        'credit': image.credit,
        'width': image.image.width,
        'height': image.image.height,
        'id': image.id,
        'href': image.get_absolute_url()
    })
    if group_by:
        grouped_images = list(izip(*[chain(processed_image_list, \
            repeat(None, group_by-1))]*group_by))
        return grouped_images
    return processed_image_list

def get_template_attributes(request, form_class):
    """
    A utiliy function which takes a request object and a Form class and extracts
    the get params from request which exist in the form class, returning them as
    a dictionary. If none of the params are set, None is returned.
    """
    params = {}
    for field in form_class.base_fields.keys():
        params[field] = request.GET.get(field, None)
    if len(params.keys()) == 0:
        return None
    if params['display']:
        if params['display'] in ['left', 'right']:
            params['position'] = "float"
        else:
            params['position'] = params['display']
    else:
        params['position'] = 'inline'
    for show_item in ('show_caption', 'show_credit'):
        if params[show_item] == "yes":
            params[show_item] = True
        else:
            params[show_item] = False
    return params

def get_preview_attributes(image):
    """
    Calculate the preview size of an image, return a dictionary of image 
    attributes suitable for use in a temple.
    """
    if image.image.width > 800:
        ratio = 1.0 * image.image.height/image.image.width
        height = ceil(ratio * 800)
        img_attrs = {
            'width': 800,
            'height': int(height),
            'resized': True
        }
    else:
        img_attrs = {
            'width': image.image.width,
            'height': image.image.height
        }
    img_attrs.update({
        'id': image.pk,
        'src': image.image.url,
        'title': image.title,
        'caption': image.caption,
        'credit': image.credit,
        'url': image.get_absolute_url()
    })
    return img_attrs
    