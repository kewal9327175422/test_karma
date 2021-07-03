from django.contrib import admin
from . models import Product,Cart,BillDetails,ProductList

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ['id','photo1','title', 'brand', 'stock_qty', 'price', 'd_price', 'description', 'catagory','featured']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product','qty']

@admin.register(BillDetails)
class BillDetailsAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'address', 'bill_no','net_total','payment_mode']

@admin.register(ProductList)
class ProductListAdmin(admin.ModelAdmin):
  list_display = ['id', 'order', 'item', 'qty']
