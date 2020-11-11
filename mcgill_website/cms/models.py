from django.db import models
import uuid

# A Page model stores a page created by the user.
class Page(models.Model):
    parent = models.ForeignKey('self',null=True,blank=True,related_name="children", default=None,on_delete=models.CASCADE) #parent page of this page. When the parent is deleted, ITS CHILDREN WILL BE DELETED
    page_level = models.IntegerField() #level of this page. A number between 1 to 4 inclusive

    page_template = models.CharField(max_length=200,default='default') #template to be used for this page

    page_name_en = models.CharField(max_length=200,default='') #Name of page as appear in path in English
    page_name_fr = models.CharField(max_length=200,default='') #Idem, in French

    page_title_en = models.TextField(blank=True,default='') #Title of the page
    page_title_fr = models.TextField(blank=True,default='')

    page_content_en = models.TextField(blank=True,default='') #Content of the page in English, to be put in the appropriate place in body
    page_content_fr = models.TextField(blank=True,default='') #Idem, in French

    custom_js_css_en = models.TextField(blank=True,default='') #Custom JS and CSS of the page in English
    custom_js_css_fr = models.TextField(blank=True,default='') #idem