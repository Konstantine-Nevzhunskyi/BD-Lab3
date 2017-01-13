# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Address(models.Model):
    address_name = models.CharField(max_length=45)
    address_x = models.IntegerField()
    address_y = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'address'


class Car(models.Model):
    driver_name = models.TextField()
    phone_num = models.TextField()

    class Meta:
        managed = False
        db_table = 'car'


class Client(models.Model):
    client_name = models.CharField(max_length=45)
    client_phone = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'client'


class TaxiOrder(models.Model):
    data = models.DateTimeField()
    client = models.ForeignKey(Client)
    car = models.ForeignKey(Car)
    start = models.ForeignKey(Address, related_name='start_id')
    finish = models.ForeignKey(Address, related_name='finish_id')

    class Meta:
        managed = False
        db_table = 'taxi_order'
        unique_together = (('id', 'client', 'car', 'start', 'finish'),)
