from django.contrib import admin
from django.utils import html

from core.models import *

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "formatted_price",
        "short_description",
        "product_image",
    )
    list_filter = (
        "name",
        "price",
    )

    def product_image(self, obj):
        if obj.image:
            return html.format_html("<img width=40 height=40 src='{}'>", obj.image.url)
        return ""

    def formatted_price(self, obj):
        return f"₹{obj.price:,.2f}"
    formatted_price.short_description = 'Price'


# Post Admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "created_at",
        "post_image",
    )
    list_filter = (
        "title",
        "created_at",
    )

    def post_image(self, obj):
        if obj.image:
            return html.format_html("<img width=40 height=40 src='{}'>", obj.image.url)
        return ""


# Testimonial Admin
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "last_name",
        "job",
        "testimonial_image",
    )
    list_filter = (
        "job",
    )
    search_fields = (
        "first_name",
        "last_name",
        "user__username",
        "job",
    )

    def testimonial_image(self, obj):
        if obj.image:
            return html.format_html("<img src='{}' width='40' height='40' style='border-radius: 50%; object-fit: cover;'>", obj.image.url)
        return "-"
    testimonial_image.short_description = "Image"


# Team Admin
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "job",
        "team_image",
    )
    list_filter = (
        "job",
    )

    def team_image(self, obj):
        if obj.image:
            return html.format_html("<img width=40 height=40 src='{}'>", obj.image.url)
        return ""


# Contact Admin
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
    )
    list_filter = (
        "first_name",
        "last_name",
        "email",
    )


# Subscription Admin
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email"
    )


# Coupon Admin
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "percent_off"
    )
    list_filter = (
        "percent_off",
        "code"
    )


# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "coupon",
        "user",
        "billing",
    )
    list_filter = (
        "coupon",
        "user__username",
        "billing",
    )


# OrderBilling Admin
@admin.register(OrderBilling)
class OrderBillingAdmin(admin.ModelAdmin):
    list_display = (
        "country",
        "first_name",
        "company_name",
        "state",
        "email",
    )
    list_filter = (
        "country",
        "first_name",
        "last_name",
        "company_name",
        "street_address",
        "state",
        "zip",
        "email",
        "phone",
        "shipping_account",
    )


# OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "quantity",
        "item_price",
    )
    list_filter = (
        "order__user",
        "product",
        "quantity",
    )

    def item_price(self, obj):
        return f"₹{obj.product.price:,.2f}"
    item_price.short_description = 'Price'


# OrderShipping Admin
@admin.register(OrderShipping)
class OrderShippingAdmin(admin.ModelAdmin):
    list_display = (
        "country",
        "first_name",
        "last_name",
        "company_name",
        "street_address",
        "state",
        "zip",
        "email",
        "phone",
    )
    list_filter = (
        "country",
        "first_name",
        "company_name",
        "state",
        "email",
    )
