from django.db import models
from django.utils import timezone

class Master_Table_List(models.Model):
    Table_name=models.CharField(max_length=40)
    Last_update=models.DateTimeField(default=timezone.now)
    Duration=models.CharField(max_length=3,default=2)
    New_update=models.CharField(max_length=3)
    
