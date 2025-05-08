
from django.urls import path
from core.views import *
urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('shop/', shop_view, name='shop'),
    path('services/', service_view, name='services'),
    path('blog/', blog_view, name='blog'),
    path('contact/', contact_view, name='contact'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('cart/', cart_view, name='cart'),
    path('order/', order_view, name='order'),
    path('thank-you/', thank_view, name='thank-you'),
    path('coupon/', coupon_view, name='coupon'),
    path('logout/', logout_view, name='logout'),
    path('logging_out/', logging_out, name='logging_out'),
]
