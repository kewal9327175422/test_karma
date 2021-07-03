from django.urls import path
from . import views

urlpatterns = [
  path('', views.Index.as_view() , name='home'),
  path('product_details/<int:id>/', views.Product_details.as_view() , name='product_details'),
  path('category/<slug:cat>/', views.Category.as_view() , name='category'),
  path('add_to_cart/', views.Add_to_cart.as_view() , name='add_to_cart'),
  path('cart/', views.CartView.as_view() , name='cart'),
  path('logout/', views.Logout.as_view(), name='logout'),
  path('registration/', views.Registration.as_view(), name='registration'),
  path('accounts/login/', views.Login.as_view(), name='login'),
  path('edit_profile/', views.EditProfile.as_view(), name='edit_profile'),
  path('profile/', views.Profileview.as_view(), name='profile'),
  path('address/', views.AddAddress.as_view(), name='address'),
  path('update_address/<int:id>/', views.UpdateAddress.as_view(), name='update_address'),
  path('delete_address/<int:id>/', views.DeleteAddress.as_view(), name='delete_address'),
  path('checkout/', views.Checkout.as_view(), name='checkout'),
  path('confirmation/', views.Confirmation.as_view(), name='confirmation'),
  path('plusqty/', views.plusqty, name='plusqty'),
  path('minusqty/', views.minusqty, name='minusqty'),
  path('delete/<int:id>/', views.DeleteCart.as_view(), name='delete_cart'),

]
