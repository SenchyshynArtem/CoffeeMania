from django.db import models
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to= "products")
    description = models.TextField()
    price = models.CharField(max_length=255)
    
    def get_absolute_url(self):
        return reverse('product', kwargs = {'product_pk': self.pk})
        
    def  __str__(self):
        return self.name
