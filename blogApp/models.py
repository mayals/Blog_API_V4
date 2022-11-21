from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid

#----------------------------------------[  Category  ]----------------------------------------------------
class Category(models.Model):
    id          = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    name        = models.CharField(max_length=20,unique=True,null=True,blank=False)
    slug        = models.SlugField(max_length=25, blank=True, null=True)
    description = models.TextField(null =True,blank=True)
    date_add    = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True,  auto_now_add=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('api:category-detail', kwargs = {"slug":self.slug})      #vue view_name='{model_name}-detail'

    def save(self, *args, **kwargs):  
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # Call the "real" save() method. 

    
    class Meta:
        ordering =['name']
        verbose_name_plural = "Categories"

