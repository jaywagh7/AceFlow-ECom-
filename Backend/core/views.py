from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from core.models import Product, Post, Testimonial, Subscription, Team, Contact, Order, OrderItem, OrderBilling, \
    OrderShipping, Coupon


# Create your views here.

def home_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        page = request.GET.get('page')
        if not Subscription.objects.filter(email=email).exists():
            Subscription.objects.create(email=email, name=name)
        if page:
            return redirect(page)

    context = {
        'products': Product.objects.all().order_by('-id')[:3],
        'posts': Post.objects.select_related('author').all().order_by('-created_at')[:3],
        'testimonials': Testimonial.objects.select_related('user').all()
    }
    return render(request, 'core/index.html', context)


def about_view(request):
    context = {
        'teammates': Team.objects.select_related('user').all(),
        'testimonials': Testimonial.objects.select_related('user').all()
    }
    return render(request, 'core/about.html', context)


def shop_view(request):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'core/shop.html', context)


def service_view(request):
    context = {
        'products': Product.objects.all().order_by('-id')[:3],
        'testimonials': Testimonial.objects.select_related('user').all()
    }
    return render(request, 'core/services.html', context)


def blog_view(request):
    context = {
        'posts': Post.objects.select_related('author').all().order_by('-created_at'),
        'testimonials': Testimonial.objects.select_related('user').all()
    }
    return render(request, 'core/blog.html', context)


def contact_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        message = request.POST.get('text')
        Contact.objects.create(email=email, first_name=first_name, last_name=last_name, message=message)
    return render(request, 'core/contact.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if user.exists():
            if user.first().check_password(password):
                login(request, user.first())
                return redirect('home')
            return redirect('login')
        return redirect('login')
    return render(request, 'auth/login.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, first_name=name)
            user.set_password(password)
            user.save()
            return redirect('login')
        return redirect('register')
    return render(request, 'auth/register.html')


@login_required(login_url='/login/')
def cart_view(request):
    product_id = request.GET.get('product_id')
    user = request.user
    action = request.GET.get('action')
    order_item_id = request.GET.get('item_id')
    act = request.GET.get('act')
    order = Order.objects.filter(user=request.user).order_by('-id').first()
    if act and order_item_id:
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        order_item.delete()
    if product_id:
        product_id = int(product_id)
        order = Order.objects.filter(user=user).first()

        if not order:
            order = Order.objects.create(user=user, billing=None)

        order_item = OrderItem.objects.filter(order=order, product_id=product_id).first()

        if order_item:
            if action == 'minus':
                order_item.quantity -= 1
                if order_item.quantity <= 0:
                    order_item.delete()
                else:
                    order_item.save()
            elif action == 'plus':
                order_item.quantity += 1
                order_item.save()
        else:
            if action == 'plus':
                OrderItem.objects.create(order=order, product_id=product_id, quantity=1)
    context = {
        "order_items": OrderItem.objects.select_related('order', 'product').filter(order__user=user),
        "order" : order,
    }

    return render(request, 'core/cart.html', context)


@login_required(login_url='/login/')
def order_view(request):
    if request.method == "POST":

        country = request.POST.get('country')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        shipping_account = request.POST.get('ship_different') == "on"
        order_notes = request.POST.get('order_notes')
        if shipping_account:
            sh_country = request.POST.get('sh_country')
            sh_first_name = request.POST.get('sh_first_name')
            sh_last_name = request.POST.get('sh_last_name')
            sh_company_name = request.POST.get('sh_company')
            sh_address = request.POST.get('sh_address')
            sh_state = request.POST.get('sh_state')
            sh_zip = request.POST.get('sh_zip')
            sh_email = request.POST.get('sh_email')
            sh_phone = request.POST.get('sh_phone')
            order_shipping = OrderShipping.objects.create(
                country=sh_country,
                first_name=sh_first_name,
                last_name=sh_last_name,
                company_name=sh_company_name,
                street_address=sh_address,
                state=sh_state,
                zip=sh_zip,
                email=sh_email,
                phone=sh_phone)
        else:
            order_shipping = OrderShipping.objects.create(
                country=country,
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                street_address=address,
                state=state,
                zip=zip,
                email=email,
                phone=phone
            )
        order_billing = OrderBilling.objects.create(
            country=country,
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            street_address=address,
            state=state,
            zip=zip,
            email=email,
            phone=phone,
            shipping_account=shipping_account,
            order_notes=order_notes,
            order_shipping=order_shipping,
        )
        order = Order.objects.filter(user=request.user, billing__isnull=True).first()

        if not order:
            order = Order.objects.create(user=request.user, billing=order_billing)
        else:
            order.billing = order_billing
        order.save()
        OrderItem.objects.filter(order=order).delete()
        return redirect('thank-you')
    order_items = OrderItem.objects.select_related('order', 'product' ).filter(order__user=request.user)
    single_order = Order.objects.filter(user=request.user).order_by('-id').first()
    context = {
        "order_items": order_items,
        "order" : single_order,
    }

    return render(request, 'core/checkout.html', context)


def coupon_view(request):
    page = request.GET.get('page')
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        coupon_code = request.POST.get('coupon_code')
        try:
            if order_id and coupon_code:
                order = Order.objects.get(id=order_id, user=request.user)
                coupon = Coupon.objects.get(code=coupon_code)
                order.coupon = coupon
                order.save()
        except:
            return redirect(page)
        return redirect(page)



def thank_view(request):
    return render(request, 'core/thankyou.html')

def logout_view(request):
    return render(request, 'auth/logout.html')

def logging_out(request):
    logout(request)
    return redirect('login')