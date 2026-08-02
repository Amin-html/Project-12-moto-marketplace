from django.contrib import admin
from .models import Category, Product,ProductImage, ProductVideo

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVideo)
# Register your models here.
