from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    class Meta:
        verbose_name = 'دسته بندی'

    title = models.CharField(max_length=150)

    def __str__(self):
       return self.title

class Article(models.Model):
    class Meta:
        verbose_name = 'مقالات'

    title = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=400)
    keywords = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    modify_date = models.DateTimeField(auto_now_add=True)
    picture_path = models.CharField(max_length=400)
    description = models.CharField(max_length=500)
    text = models.TextField(blank=True)

    def __str__(self):
        return self.title