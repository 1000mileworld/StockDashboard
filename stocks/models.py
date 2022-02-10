from django.db import models

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=5)
    company = models.CharField(max_length=100)
    open = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    close = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    low_52wk = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    high_52wk = models.DecimalField(max_digits=8,decimal_places=2,default=0)