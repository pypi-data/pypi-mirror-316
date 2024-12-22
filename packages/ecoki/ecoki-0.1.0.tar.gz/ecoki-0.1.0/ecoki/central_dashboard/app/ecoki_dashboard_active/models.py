from django.db import models
from ckeditor.fields import RichTextField 
# Create your models here.



from django.contrib.auth.models import User

# pipeline model
class Pipeline(models.Model):

    # api information
    name = models.CharField(max_length=180)
    adress = models.CharField(max_length=180)
    port = models.CharField(max_length=180)

    # more information
    #- bb_names, bb_descriptions, ...

    # from the template
    #task = models.CharField(max_length = 180)
    #timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    #completed = models.BooleanField(default = False, blank = True)
    #updated = models.DateTimeField(auto_now = True, blank = True)
    #user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.name

class ActiveBB(models.Model):
    activebb = models.CharField(max_length=180)
    
    def __str__(self):
        return self.activebb
    
class BB(models.Model):
    
    bbname = models.CharField(max_length=180)
    
    def __str__(self):
        return self.bbname
    
class editor(models.Model):
    
    content = RichTextField(blank=True, null=True)
    
    def __str__(self):
        return self.content