from django.conf import settings
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

import ck_palettes

class StandardTemplateForm(forms.Form):
    display = forms.ChoiceField(
        label = _("Image Position"),
        choices = (
            ('inline', 'Image Inline'),
            ('center', 'Center Image'),
            ('right', 'Float Image Right'),
            ('left', 'Float Image Left'),
        )
    )
    show_caption = forms.BooleanField(
        label = _("Show Caption"),
        required = False
    )
    show_credit = forms.BooleanField(
        label = _("Show Credit"),
        required = False
    )

class ResizedImageForm(StandardTemplateForm):
    action = forms.ChoiceField(
        label = _("When User Clicks Image..."),
        choices = (
            ('', 'Do nothing.'),
            ('lightbox', 'Show original size in lightbox.'),
            ('tab', 'Show original size in new tab.'),
            ('link', 'Link to original size.'),
        )
    )


CKEDITOR_PATH = getattr(settings, 'CKEDITOR_PATH', 'js/ckeditor/')
GLOSSARY_PREFIX = getattr(settings, 'GLOSSARY_PREFIX', '')


class CKEditor(forms.Textarea):
    """A richtext editor widget that uses CKEditor.
    Inspired by http://code.google.com/p/django-ck
    """
    class Media:
        js = (
            
            CKEDITOR_PATH + 'jquery.ui/js/jquery-1.3.2.min.js',
            CKEDITOR_PATH + 'ckeditor.js',
            CKEDITOR_PATH + 'media_browser.js',
            CKEDITOR_PATH + 'jquery.ui/js/jquery-ui-1.7.2.custom.min.js',
        )
        css = {
            'all': (CKEDITOR_PATH + 'jquery.ui/css/ui-lightness/jquery-ui-1.7.2.custom.css',)
        }

    def __init__(self, *args, **kwargs):
        
        self.ck_attrs = kwargs.get('ck_attrs', {})
        if self.ck_attrs:
            kwargs.pop('ck_attrs')
        
        self.additional_plugins_js = kwargs.get('additional_plugins_js', None)
        if self.additional_plugins_js:
            kwargs.pop('additional_plugins_js')

        self.pallete = kwargs.get('custom_pallete', ck_palettes.full_pallete)
        if kwargs.get('custom_pallete'):
            kwargs.pop('custom_pallete')
        super(CKEditor, self).__init__(*args, **kwargs)
        
    def serialize_script_params(self):
        ck_attrs = ''
        if not 'language' in self.ck_attrs:
            self.ck_attrs['language'] = get_language()[:2]
        for k,v in self.ck_attrs.iteritems():
            ck_attrs += k + " : '" + v + "',\n"
        return ck_attrs
    
    def render(self, name, value, attrs=None):
        rendered = super(CKEditor, self).render(name, value, attrs)
        ck_attrs = self.serialize_script_params()
        var_name = name.replace("-", "_")
        if self.additional_plugins_js:
            additional_plugins_js = mark_safe(self.additional_plugins_js)
        else:
            additional_plugins_js = ''
        return render_to_string('media_browser/ckeditor_object.html', {
            'basepath': settings.MEDIA_URL + CKEDITOR_PATH,
            'field': rendered,
            'field_name': name,
            'field_var_name': var_name,
            'options': mark_safe(ck_attrs),
            'pallete': mark_safe(self.pallete),
            'additional_plugins_js': mark_safe(additional_plugins_js),
            'GLOSSARY_PREFIX': GLOSSARY_PREFIX
        })
    