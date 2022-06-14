from tkinter import CASCADE
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

#choices
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)

BRAND_CHOICES = (
    ('Cartier', 'Cartier'),
    ('Rolex', 'Rolex'),
    ('Patek Philippe', 'Patek Philippe'),
    ('Audemars Piguet', 'Audemars Piguet'),
    ('Omega', 'Omega')
)

MATERIAL_CHOICES = (
    ('Ceramic', 'Ceramic'),
    ('Titanium', 'Titanium'),
    ('Stainless steel', 'Stainless steel'),
    ('Steel watch', 'Steel watch')
)

MECHANISM_CHOICES = (
    ('Mechanical', 'Mechanical'),
    ('Automatic', 'Automatic'),
    ('Quartz', 'Quartz'),
    ('Seiko Kinetic', 'Seiko Kinetic'),
    ('Solar', 'Solar')
)

GLASS_CHOICES = (
    ('Regular', 'Regular'),
    ('Plastic', 'Plastic'),
    ('Sapphire', 'Sapphire'),
    ('Crystal', 'Crystal'),
    ('Mineral', 'Mineral')
)

WATER_RESISTANCE_CHOICES = (
    (30, '30 meters'),
    (50, '50 meters'),
    (100, '100 meters'),
    (200, '200 meters'),
    (300, '300 meters')
)

# Create your models here.

class Watch(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='photos/watches', blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    year = models.IntegerField(validators=[MaxValueValidator(2022)]) #dodati ogranicenja ??
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES)
    brand = models.CharField(max_length=30, choices=BRAND_CHOICES)
    material = models.CharField(max_length=30, choices=MATERIAL_CHOICES)
    mechanism = models.CharField(max_length=30, choices=MECHANISM_CHOICES)
    diameter = models.IntegerField(validators=[MinValueValidator(24), MaxValueValidator(56)]) #dodati ogranicenja
    glass = models.CharField(max_length=30, choices=GLASS_CHOICES)
    waterResistantType = models.IntegerField(choices=WATER_RESISTANCE_CHOICES)
    description = models.TextField(max_length=255, blank=True)
    availableItems = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(25)])

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ' '
        return url

class Review(models.Model):
    product = models.ForeignKey(Watch, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewText = models.TextField(max_length=500, blank=True)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.reviewText



