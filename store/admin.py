from django.contrib import admin
from store.models import Product,UserProfile,Category
# Register your models here.

admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Category)
