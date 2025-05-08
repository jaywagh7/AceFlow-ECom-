from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='products/')
    short_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    def price_in_rupees(self):
        return f"₹{self.price}"

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    job = models.CharField(max_length=50)
    review = models.TextField()
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    def __str__(self):
        return f"{self.id} {self.user.username}"

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='posts/')
    def __str__(self):
        return self.title

class Team(models.Model):
    class Meta:
        verbose_name_plural = "Teammates"
    image = models.ImageField(upload_to='teams/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')
    job = models.CharField(max_length=50)
    short_description = models.TextField()
    def __str__(self):
        return f"{self.user.username} - {self.job}"

class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"

class Subscription(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Coupon(models.Model):
    code = models.CharField(max_length=255, unique=True)
    percent_off = models.IntegerField()
    def __str__(self):
        return self.code

class Order(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders') #
    billing = models.ForeignKey('OrderBilling', on_delete=models.CASCADE, related_name='order_billings', unique=True, null=True, blank=True) #

    @property
    def total_price(self):
        total = sum(Decimal(item.product.price) * Decimal(item.quantity) for item in self.order_items.all())
        return total

    @property
    def coupon_discount(self):
        if self.coupon:
            discount = (self.total_price * Decimal(self.coupon.percent_off)) / Decimal(100)
            return discount
        return Decimal(0)

    @property
    def final_price(self):
        return self.total_price - self.coupon_discount

class OrderBilling(models.Model):
    country = models.CharField(max_length=100)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    shipping_account = models.BooleanField(default=False)
    order_notes = models.TextField(null=True, blank=True) #
    order_shipping = models.ForeignKey('OrderShipping', on_delete=models.CASCADE, related_name='order_billings', unique=True) #

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(default=1)

class OrderShipping(models.Model):
    country = models.CharField(max_length=100)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)