from django.contrib import admin

from .models import Review, Watch

# Register your models here.
admin.site.register(Watch)
admin.site.register(Review)