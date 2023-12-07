from django.db import models
from datetime import datetime
from django.utils import timezone
import pytz
from django.contrib.auth.models import User

# Create your models here.

class ProductModel(models.Model):
    p_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    p_name = models.CharField(max_length=256)
    p_desc = models.TextField()
    p_img = models.FileField(upload_to='media')
    p_price = models.FloatField(default=None, null=True)
    
    def __str__(self) -> str:
        return self.p_name


class BidModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    bid_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('product', 'price')

class BlockChainModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    block = models.CharField(max_length=128)
    time_stamp = models.DateTimeField(default=timezone.now)
    type_of_block = models.CharField(max_length=200)
    block_detail = models.CharField(max_length=200)