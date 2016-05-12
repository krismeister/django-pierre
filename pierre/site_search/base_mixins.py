class SearchableMixin(object):
    """
    Base level Searchable mixin. NB: you don't have to use this to make a class
    searchable, but model class must have must have the methods and props 
    defined in ISearchable to be searched. If fields_to_index is set to True, 
    all fields in the model will be indexed.
    """
    
    fields_to_index = True
    
    
    def get_search_result_title(self):
        # This will need to be overriden on a model by model basis.
        return self.pk

    def get_search_result_description(self):
        return None

    def get_search_result_date(self):
        return None

    def is_searchable(self):
        return True

    