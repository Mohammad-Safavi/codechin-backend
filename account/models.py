from django.db import models
from django.contrib.auth.models import User
from product.models import *


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.SmallIntegerField(default=1)
    options = models.ManyToManyField(
        Option, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Payment(models.Model):
    class Meta:
        verbose_name = 'پرداخت ها'
        verbose_name_plural = 'پرداخت ها'

    STATUS_PAID = 1
    STATUS_UNKNOWN = 2
    STATUS_FAILED = 2
    CHOICES_STATUS = (
        (STATUS_PAID , 'موفق'),
        (STATUS_UNKNOWN , 'نامشخص'),
        (STATUS_FAILED , 'ناموفق'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(max_length=255)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.CASCADE)
    trancation_id = models.IntegerField(null=True, blank=True)
    status = models.SmallIntegerField(choices=CHOICES_STATUS, default=STATUS_UNKNOWN)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Invoice(models.Model):

    class Meta:
        verbose_name = 'فاکتور ها'
        verbose_name_plural = 'فاکتور ها'

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount,  null=True, blank=True, on_delete=models.CASCADE)
    count = models.SmallIntegerField(default=1)
    options = models.ManyToManyField(
        Option, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Address(models.Model):
    class Meta:
        verbose_name = 'آدرس ها'
        verbose_name_plural = 'آدرس ها'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    title = models.CharField(max_length=255, verbose_name="عنوان")
    address = models.TextField(verbose_name="آدرس")
    post_code = models.CharField(null=True, blank=True, max_length=255, verbose_name="کد پستی")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username