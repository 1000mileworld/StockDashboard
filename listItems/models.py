from django.db import models

from stocks.models import Stock

# Create your models here.
class Search(models.Model):
    query = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.query

class SearchField(models.Model):
    count = models.IntegerField(default=0)
    is_duplicate = models.BooleanField(default=False)
    validity = models.BooleanField(default=True)