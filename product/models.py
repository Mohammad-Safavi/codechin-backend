from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    title = models.CharField(max_length=200)
    icon = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class SubCategory(models.Model):
    title = models.CharField(max_length=200)
    icon = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class SubSubCategory(models.Model):
    title = models.CharField(max_length=200)
    icon = models.TextField(null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Picture(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=600)

    def __str__(self):
        return self.name

class Property(models.Model):
    title = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.title + ' => ' + self.value

class Option(models.Model):

    OPTION_TYPE_COLOR = 1
    OPTION_TYPE_LENGHT = 2
    OPTION_TYPE_SIZE = 3
    CHOICES_OPTION = (
        (OPTION_TYPE_COLOR, 'color'),
        (OPTION_TYPE_LENGHT, 'lenght'),
        (OPTION_TYPE_SIZE, 'size'),
    )
    title = models.CharField(max_length=200)
    type = models.SmallIntegerField(choices=CHOICES_OPTION, default=OPTION_TYPE_COLOR)

    def __str__(self):
        return self.title + ' | ' + str(self.type)

class Discount(models.Model):
    title = models.CharField(max_length=200)
    percent = models.IntegerField(validators=[MinValueValidator(1),
                                              MaxValueValidator(100)])
    def __str__(self):
        return self.title

class Product(models.Model):

    STATUS_AVAILABLE = 1
    STATUS_UNAVAILABLE = 2
    CHOICES_STATUS = (
        (STATUS_AVAILABLE , 'available'),
        (STATUS_UNAVAILABLE , 'unavailable'),
    )

    name = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200,null=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    discount = models.ForeignKey(Discount,  null=True,blank=True,on_delete=models.CASCADE)
    pictures = models.ManyToManyField(Picture)
    properties = models.ManyToManyField(Property)
    options = models.ManyToManyField(Option, null=True)
    category = models.ManyToManyField(SubSubCategory)
    about = models.TextField(blank=True)
    status = models.SmallIntegerField(choices=CHOICES_STATUS, default=STATUS_AVAILABLE)
    active = models.BooleanField(default=1)

    def __str__(self):
        return self.name