from django.db import models

# Create your models here.

class Story(models.Model):
    author = models.CharField(max_length=20, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    levels = models.CharField(max_length=11, blank=True, null=True)
    likes = models.CharField(max_length=11, blank=True, null=True)
    pageno = models.CharField(db_column='pageNo', max_length=11, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'story'