from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Category(models.Model):

    class Meta:
        verbose_name_plural = "دسته بندی سطح ۱"
        verbose_name = 'دسته بندی سطح ۱'

    title = models.CharField(max_length=200, verbose_name="عنوان")
    icon = models.TextField(null=True, blank=True, verbose_name="نشانک")

    def __str__(self):
        return self.title


class SubCategory(models.Model):

    class Meta:
        verbose_name_plural = "دسته بندی سطح ۲"
        verbose_name = 'دسته بندی سطح ۲'
    
    title = models.CharField(max_length=200, verbose_name="عنوان")
    icon = models.TextField(null=True, blank=True, verbose_name="نشانک")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته بندی سطح ۱")

    def __str__(self):
        return self.title


class SubSubCategory(models.Model):
        
    class Meta:
        verbose_name_plural = "دسته بندی سطح ۳"
        verbose_name = 'دسته بندی سطح ۳'
    
    title = models.CharField(max_length=200, verbose_name="عنوان")
    icon = models.TextField(null=True, blank=True, verbose_name="نشانک")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name="دسته بندی سطح ۲")

    def __str__(self):
        return self.title


class Picture(models.Model):
        
    class Meta:
        verbose_name_plural = "تصاویر"
        verbose_name = 'تصاویر'
    
    name = models.CharField(max_length=100, verbose_name="نام")
    path = models.CharField(max_length=600, verbose_name="آدرس")

    def __str__(self):
        return self.name


class Property(models.Model):
        
    class Meta:
        verbose_name_plural = "ویژگی ها"
        verbose_name = 'ويزگی ها'

    title = models.CharField(max_length=200, verbose_name="عنوان")
    value = models.CharField(max_length=200, verbose_name="مقدار")

    def __str__(self):
        return self.title + ' => ' + self.value


class Option(models.Model):
    
    class Meta:
        verbose_name_plural = "ویژگی های انتخابی"
        verbose_name = 'ویژگی های انتخابی'
    
    OPTION_TYPE_COLOR = 1
    OPTION_TYPE_LENGHT = 2
    OPTION_TYPE_SIZE = 3
    CHOICES_OPTION = (
        (OPTION_TYPE_COLOR, 'رنگ'),
        (OPTION_TYPE_LENGHT, 'طول'),
        (OPTION_TYPE_SIZE, 'اندازه'),
    )
    title = models.CharField(max_length=200, verbose_name="عنوان")
    type = models.SmallIntegerField(
        choices=CHOICES_OPTION, default=OPTION_TYPE_COLOR, verbose_name="نوع")

    def __str__(self):
        return self.title + ' | ' + str(self.type)


class Discount(models.Model):
        
    class Meta:
        verbose_name_plural = "تخفیفات"
        verbose_name = 'تخفیفات'
    
    title = models.CharField(max_length=200, verbose_name="عنوان")
    percent = models.IntegerField(validators=[MinValueValidator(1),
                                              MaxValueValidator(100)], verbose_name="مقدار")

    def __str__(self):
        return self.title


class Product(models.Model):
    
    class Meta:
        verbose_name_plural = "محصولات"
        verbose_name = 'محصولات'
    
    STATUS_AVAILABLE = 1
    STATUS_UNAVAILABLE = 2
    CHOICES_STATUS = (
        (STATUS_AVAILABLE , 'موجود'),
        (STATUS_UNAVAILABLE , 'ناموجود'),
    )

    name = models.CharField(max_length=200, verbose_name="نام")
    english_name = models.CharField(max_length=200,null=True, verbose_name="نام لاتین")
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="قیمت")
    discount = models.ForeignKey(Discount,  null=True,blank=True,on_delete=models.CASCADE, verbose_name="تخفیف")
    pictures = models.ManyToManyField(Picture, verbose_name="تصاویر")
    properties = models.ManyToManyField(Property, verbose_name="ویژگی ها")
    options = models.ManyToManyField(Option, null=True,blank=True, verbose_name="ویژگی های انتخابی")
    category = models.ManyToManyField(SubSubCategory, verbose_name="دسته بندی")
    about = models.TextField(blank=True, verbose_name="درباره محصول")
    status = models.SmallIntegerField(choices=CHOICES_STATUS, default=STATUS_AVAILABLE, verbose_name="وضعیت")
    active = models.BooleanField(default=1, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    class Meta:
        verbose_name = 'دیدگاه ها'
        verbose_name_plural = 'دیدگاه ها'


    STATUS_CONFIRMED = 1
    STATUS_UNCONFIRMED = 2
    CHOICES_STATUS = (
        (STATUS_CONFIRMED , 'تاییده شده'),
        (STATUS_UNCONFIRMED , 'تایید نشده'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    text = models.TextField(verbose_name="متن")
    status = models.SmallIntegerField(choices=CHOICES_STATUS, default=STATUS_UNCONFIRMED, verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
