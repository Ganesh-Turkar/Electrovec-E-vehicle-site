from re import T
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from decimal import Decimal
from django.core.validators import MinValueValidator


class UserDetail(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    id = models.AutoField("id", primary_key=True)
    name = models.CharField('name', max_length=120)
    price = models.CharField('price', max_length=60, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    top_speed = models.CharField('top speed', max_length=60)
    range = models.CharField('range', max_length=60)
    charging_time = models.CharField('charging time', max_length=60)
    colors = models.CharField('colors', max_length=60, null=True, blank=True)
    rating = models.CharField('rating', max_length=60, null=True, blank=True)
    description = models.TextField(
        'description', max_length=1000, null=True, blank=True)
    frontimg = models.ImageField(
        upload_to="img/", null=True, blank=True)
    rearimg = models.ImageField(
        upload_to="img/", null=True, blank=True)
    sideimg = models.ImageField(
        upload_to="img/", null=True, blank=True)
    offers = models.CharField('offers', max_length=180, null=True, blank=True)
    battery_type = models.CharField(
        'battery type', max_length=180, null=True, blank=True)
    max_power = models.CharField(
        'max power', max_length=180, null=True, blank=True)
    speedometer = models.CharField(
        'speedometer', max_length=180, null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        null=True, blank=True, default=0, validators=[MinValueValidator(Decimal('1'))])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vehicle.name

    def vehicle_id(self):
        return self.vehicle.id


class V_Comment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=180)
    #comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True)
    replied_to = models.CharField(
        'replied_to', max_length=180, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[0:25] + "..." + " by " + self.user.username

 # temp class for rest framework


# class tempclass(models.Model):
#     vehicle_name = models.CharField(max_length=120)
#     price = models.IntegerField(
#         null=True, blank=True, default=0, validators=[MinValueValidator(Decimal('1'))])

#     def __str__(self):
#         return self.vehicle_name
