# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Top100(models.Model):
    ranking = models.IntegerField()
    title = models.CharField(unique=True, max_length=255)
    stars = models.CharField(max_length=255)
    release_time = models.CharField(max_length=255)
    score = models.FloatField()
    img_url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'top_100'
