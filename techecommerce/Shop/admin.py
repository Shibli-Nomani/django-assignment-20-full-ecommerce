from django.contrib import admin

#imports all models/tables
from .models import (Customer, Product, Cart, OrderPlaced)
# Register your models here.

#for Customer Table
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'division', 
                    'district', 'thana', 'villorroad','zipcode']
    
#for Product table
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'selling_price', 'discounted_price', 'description', 
                    'brand', 'category', 'product_image']
#for Cart table
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

#for OrderPlaced table
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity',
                    'ordered_date', 'status']
    