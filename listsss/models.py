from django.db import models


# Create your models here.
class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    # django 2.0 需要添加on_delete=models.CASCADE，原因可查
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
