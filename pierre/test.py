from copy import copy

from django.contrib.auth.models import User
from django.core.urlresolvers import NoReverseMatch
"""
This file provides a TestCase derived class which provides a 
convinience methods for some typical django test case patterns
"""

from django.test import TestCase

class ModelTest(TestCase):
    
    query_sets = ()
    
    test_user = 'testrunner'
    test_password = 'pass123'    
    
    def test_object_urls(self):
        """
        Calls the get_absolute_url method each object for each QuerySet in 
        self.query_sets and verifies that that url does not return an error.
        """
        for query_set in self.query_sets:            
            for item in query_set:
                try:
                    url = item.get_absolute_url()
                except NoReverseMatch:
                    url = None
                if url and url != "":
                    response = self.client.get(url)
                    self.assertTrue(response.status_code == 200)


    def setup_admin_user(self):
        """Check to see if test runner user was already created (perhaps by
        another test class) and if not, create it.
        """
        try:
            User.objects.get(username=self.test_user)
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                self.test_user,
                'test@localhost.com',
                self.test_password
            )
        
    def log_test_client_in(self, login_url=None):
        """Log the test client in using the test runner user"""
        self.setup_admin_user()
        """r = self.client.login(
            username=self.test_user, 
            password=self.test_password
        )"""
        if not login_url:
            from django.conf.global_settings import LOGIN_URL as login_url
        resp = self.client.post(
            login_url, 
            {'username': self.test_user, 'password': self.test_password}
        )
        
        
    def log_test_client_out(self):
        """Log the test client out using the test runner user"""    
        self.client.logout()
        



