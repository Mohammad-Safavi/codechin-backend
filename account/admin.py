from django.contrib import admin
from .models import *

admin.site.register(Payment)
admin.site.register(Cart)
admin.site.register(Invoice)
admin.site.register(Address)

