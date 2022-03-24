from django.contrib import admin
from .models import Coffee, Processing, Roaster


# Register your models here.
admin.site.register(Coffee)
admin.site.register(Processing)
admin.site.register(Roaster)
