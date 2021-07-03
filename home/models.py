from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


CATAGORY_CHOICES = (
  ('M','man'),
  ('W','woman'),
)

class Product(models.Model):
  photo1 = models.ImageField(upload_to='products')
  title = models.CharField(max_length=100)
  brand = models.CharField(max_length=50)
  stock_qty = models.IntegerField()
  price = models.FloatField()
  d_price = models.FloatField()
  description = models.TextField()
  catagory = models.CharField(max_length=4, choices=CATAGORY_CHOICES)
  featured = models.BooleanField()
  objects=models.Manager()

  class Meta:
    verbose_name = ("Product")
    verbose_name_plural = ("Products")

class Cart(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  qty = models.PositiveIntegerField(default=1)
  objects = models.Manager()
  
  @property
  def get_total(self):
    return self.qty*self.product.d_price

class ShippingAddress(models.Model):
  
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  fname = models.CharField(max_length=100)
  lname = models.CharField(max_length=100)
  mobile_no = models.IntegerField()
  country = models.CharField(max_length=100)
  alternative_mobile_no = models.IntegerField(blank=True, null=True)
  address_line1= models.CharField(max_length=150)
  address_line2= models.CharField(max_length=150)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  Zipcode = models.IntegerField()


class BillDetails(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
  bill_no = models.IntegerField()
  net_total = models.IntegerField()
  payment_mode = models.CharField(max_length=20)


class ProductList(models.Model):
  order = models.ForeignKey(BillDetails, on_delete=models.CASCADE)
  item = models.ForeignKey(Product, on_delete=models.CASCADE)
  qty = models.IntegerField()