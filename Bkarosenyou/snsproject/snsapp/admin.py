from django.contrib import admin
from .models import Coment,Review,Profile,Reply
# Register your models here.

admin.site.register(Coment)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Reply)