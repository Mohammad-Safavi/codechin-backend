import code
from django.db import models


class RegisterCode(models.Model):
    class Meta:
        verbose_name = 'کد ورود'
        verbose_name_plural = 'کد ورود'

    username = models.CharField(max_length=255)
    code = models.CharField(max_length=200)

    def __str__(self):
        return self.username
