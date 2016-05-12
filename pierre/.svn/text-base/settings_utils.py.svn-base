from os import path

def get_application_template_directory(python_module):
    """
    Searches for a folder called "templates" in the given python module and
    if it exists, returns the absolute path to it:
    
    >>> from pierre import media_browser
    >>> get_application_template_directory(media_browser)
    '/path/to/pierre/media_browser/templates'
    
    """
    assert hasattr(python_module, '__file__'), "This isn't a python module."
    template_path =  path.join(
        path.dirname(python_module.__file__), 
        "templates"
    )
    return path.exists(template_path) and template_path or None