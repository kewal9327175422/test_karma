from typing import get_args
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from . models import Cart, Product, ShippingAddress, BillDetails, ProductList
from django.shortcuts import redirect, render
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from . forms import RegistrationForm, LoginForm, ShippingAddressForm, EditRegistrationForm
from django.contrib import messages
from django.db.models import Q
import random
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

def tally(product):
  subtotal = 0
  for data in product :
    subtotal += (data.qty*data.product.d_price)
  tax = ((subtotal/100)*118 - subtotal)
  net_total = tax + subtotal
  return subtotal, tax, net_total


class Index(TemplateView):
  template_name = 'home/index.html'
  
  def get_context_data(self,*args, **kwargs):
    context = super().get_context_data(**kwargs)
    feature = Product.objects.filter(featured=True)
    man = Product.objects.filter(catagory='M').order_by('stock_qty')[0:8]
    woman = Product.objects.filter(catagory='W').order_by('stock_qty')[0:8]
    all = Product.objects.all()[0:9]
    
    params = {'feature':feature,'man':man, 'woman':woman, 'all':all  }
    context.update(params)
    return context

class Product_details(TemplateView):
  template_name = 'home/product_details.html'
  
  def get_context_data(self, id, **kwargs):
    context = super().get_context_data(**kwargs)
    product = Product.objects.get(pk=id)
    all = Product.objects.all()[0:9]
    params = {'all':all,'product':product}
    context.update(params) 
    return context

class Category (ListView):
  def get(self, request, cat):
    count_m = len(Product.objects.filter(catagory='M'))
    count_w = len(Product.objects.filter(catagory='W'))
    b1 = len(Product.objects.filter(brand='No 1 brand'))
    b2 = len(Product.objects.filter(brand='No 2 brand'))
    b3 = len(Product.objects.filter(brand='No 3 brand'))
    if cat == '1':
      data = Product.objects.filter(brand= 'No 1 brand')
    elif cat == '2':
      data = Product.objects.filter(brand= 'No 2 brand')
    elif cat == '3':
      data = Product.objects.filter(brand= 'No 3 brand')
    else:
      data = Product.objects.filter(catagory=cat)
    
    context = {'p_data': data, 'count_m':count_m, 'count_w':count_w, 'b1':b1, 'b2':b2, 'b3':b3}
    return render(request, 'home/category.html', context)

@method_decorator(login_required, name='dispatch')
class EditProfile(View):
  def get(self, request):
    pi = User.objects.get(pk=request.user.id)
    form = EditRegistrationForm(instance=pi)
    return render(request, 'home/edit_profile.html',{'form':form})
  
  def post(self, request):
    pi = User.objects.get(pk = request.user.id)
    form = EditRegistrationForm(request.POST, instance=pi)
    if form.is_valid():
      form.save()
      return redirect('/profile/')
    return render(request, 'home/edit_profile.html',{'form':form})


@method_decorator(login_required, name='dispatch')
class AddAddress(View):
  def get(self, request):
    form = ShippingAddressForm()
    return render(request, 'home/address.html', {'form':form})
  
  def post(self, request):
    form = ShippingAddressForm(request.POST)
    if form.is_valid():
      user = request.user
      fname = form.cleaned_data.get('fname')
      lname = form.cleaned_data.get('lname')
      mobile_no = form.cleaned_data.get('mobile_no')
      alternative_mobile_no = form.cleaned_data.get('alternative_mobile_no', '0')
      country = form.cleaned_data.get('country')
      line1 = form.cleaned_data.get('address_line1')
      line2 = form.cleaned_data.get('address_line2')  
      city = form.cleaned_data.get('city')
      state = form.cleaned_data.get('state')
      Zipcode = form.cleaned_data.get('Zipcode')
      
      x = ShippingAddress(user=user, fname=fname, lname=lname, mobile_no=mobile_no, alternative_mobile_no=alternative_mobile_no, country=country, address_line1=line1, address_line2=line2, city=city, state=state, Zipcode=Zipcode )
      x.save()
      return redirect('/checkout/')
    return render(request, 'home/address.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class UpdateAddress(View):
  def get(self, request, id):
    pi = ShippingAddress.objects.get(pk=id)
    form = ShippingAddressForm(instance=pi)
    return render(request, 'home/address.html', {'form':form})
  
  def post(self, request, id):
    form = ShippingAddressForm(request.POST)
    if form.is_valid():
      user = request.user
      line1 = form.cleaned_data.get('address_line1')
      line2 = form.cleaned_data.get('address_line2')  
      city = form.cleaned_data.get('city')
      state = form.cleaned_data.get('state')
      Zipcode = form.cleaned_data.get('Zipcode')
      country = form.cleaned_data.get('country')
      mobile_no = form.cleaned_data.get('mobile_no')
      alternative_mobile_no = form.cleaned_data.get('alternative_mobile_no', '0')
      
      x = ShippingAddress(id=id, user=user, address_line1=line1, address_line2=line2, city=city, state=state, Zipcode=Zipcode, country=country, mobile_no=mobile_no, alternative_mobile_no=alternative_mobile_no)
      x.save()
      return redirect('/profile/')
    return render(request, 'home/address.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class DeleteAddress(View):
  def get(self, request, id):
    x = ShippingAddress.objects.get(pk=id)
    x.delete()
    return redirect('/profile/')

@method_decorator(login_required, name='dispatch')
class Add_to_cart(View):
  def get(self, request):
    id = request.GET.get('sid')
    product = Product.objects.get(pk=id)
    if Cart.objects.filter(user=request.user, product=product).exists():
      return JsonResponse(dict(status=0))
    else:
      x = Cart(user=request.user, product=product,qty=1)
      x.save()
    return JsonResponse(dict(status=1))

@method_decorator(login_required, name='dispatch')
class CartView(View):
  def get(self, request):
    product = Cart.objects.filter(user=request.user)
    subtotal, tax, net_total = tally(product)
    context = dict(product=product, subtotal=subtotal, tax=tax, net_total=net_total)
    return render(request, 'home/cart.html', context)

@method_decorator(login_required, name='dispatch')
class Profileview(View):
  def get(self, request):
    return render(request, 'home/profile.html')

@method_decorator(login_required, name='dispatch')
class Checkout(View):
  def get(self, request):
    address = ShippingAddress.objects.filter(user=request.user)
    product = Cart.objects.filter(user=request.user)
    subtotal, tax, net_total = tally(product)
    context = dict(address=address, product=product , subtotal=subtotal, tax=tax, net_total=net_total,)
    return render(request, 'home/checkout.html', context)
  
  def post(self, request):
    a = False
    address = ShippingAddress.objects.filter(user=request.user)
    product = Cart.objects.filter(user=request.user)
    subtotal, tax, net_total = tally(product)
    id = request.POST.get('address', None)
    payment_mode = request.POST.get('payment_method', None)
    bill_no = random.randint(111111,999999)
    
    if id == None or payment_mode==None:
      context = dict(msg = "Please Select Address & Payment Method",address=address, subtotal=subtotal, tax=tax, net_total=net_total,)
      return render(request, 'home/checkout.html', context)
    else:
      address1 = ShippingAddress.objects.get(pk=id)
      x = BillDetails(user=request.user, address=address1, bill_no=bill_no, net_total= net_total, payment_mode=payment_mode)
      x.save()
      order = BillDetails.objects.get(pk=x.id)
      available_stock = []
      no_stock = []
      for data in product:
        if data.product.stock_qty >= data.qty :
          y = ProductList(order=order, item=data.product, qty=data.qty)
          y.save()
          available_stock.append(y.item)
          b = Cart.objects.get(pk=data.id)
          b.delete()
        else:
          no_stock.append(data.product)
      
      if available_stock == [] :
        x.delete()
        subject = 'Order Details'
        msg = 'Products is not in Stock...'
        from_mail = 'kewal@gmail.com'
        to_mail = ['keval.123456@gmail.com']
      
        send_mail(subject, msg, from_mail, to_mail, fail_silently=False)
      else:
        c = ProductList.objects.filter(order=order)
        available = []
        not_available = []
        for data in c :
          available.append(data.item.title)
        for data in no_stock:
          not_available.append(data.title) 
        
        subject = 'Order Details'
        msg = f'{available} is ready to dispatch, {not_available} is not in Stock...'
        from_mail = 'kewal@gmail.com'
        to_mail = ['keval.123456@gmail.com']
      
        send_mail(subject, msg, from_mail, to_mail, fail_silently=False)
      
    context = dict(product=no_stock,a = True)    
    return render(request, 'home/confirmation.html',context)

@method_decorator(login_required, name='dispatch')
class Confirmation(View):
  def get(self, request):
    return render(request, 'home/confirmation.html')

def plusqty(request):
  if request.method == "GET":
    id = request.GET.get('sid')
    c = Cart.objects.get(pk=id)
    c.qty += 1
    c.save()
    product = Cart.objects.filter(user=request.user)
    subtotal, tax, net_total = tally(product)
    return JsonResponse(dict(status=1, qty=c.qty, total=c.get_total, subtotal=subtotal, tax=tax, net_total=net_total))
  return JsonResponse(dict(status=0))

def minusqty(request):
  if request.method == "GET":
    id = request.GET.get('sid')
    c = Cart.objects.get(pk=id)
    if c.qty <= 1:
      c.qty = 1
    else:
      c.qty -= 1
    c.save()
    product = Cart.objects.filter(user=request.user)
    subtotal, tax, net_total = tally(product)
    return JsonResponse(dict(status=1, qty=c.qty, total=c.get_total, subtotal=subtotal, tax=tax, net_total=net_total))
  return JsonResponse(dict(status=0))


class Login(LoginView):
  template_name = 'home/login.html'
  form_class = LoginForm

@method_decorator(login_required, name='dispatch')
class Logout(LogoutView):
  pass


class Registration(View):
  def get(self, request):
    form = RegistrationForm()
    return render(request, 'home/registration.html',{'form':form})
  
  def post(self, request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
      messages.success(request, 'Registered Succesfully... ')
      form.save()
      form = LoginForm()
      return redirect('/accounts/login/')
    return render(request, 'home/registration.html',{'form':form})

@method_decorator(login_required, name='dispatch')
class DeleteCart(View):
  def get(self, request, id):
    x = Cart.objects.get(pk=id)
    x.delete()
    return redirect ('/cart/')