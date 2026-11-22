from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .forms import SignupForm
from .models import Category, Product, Order, OrderItem

def home(request):
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(available=True).select_related("category")[:8]
    return render(request, "shop/home.html", {"categories": categories, "products": products})

def collections(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, "shop/collections.html", {"categories": categories})

def product_list(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, available=True)
    sort = request.GET.get("sort")
    if sort == "low":
        products = products.order_by("price")
    elif sort == "high":
        products = products.order_by("-price")
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(name__icontains=query)
    return render(request, "shop/product_list.html", {"category": category, "products": products, "query": query})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, "shop/product_detail.html", {"product": product})

def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("home")
    return render(request, "shop/signup.html", {"form": form})

def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("home")
    product = get_object_or_404(Product, pk=product_id, available=True)
    cart = request.session.get("cart", {})
    key = str(product.id)
    cart[key] = int(cart.get(key, 0)) + 1
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your bag.")
    return redirect(request.META.get("HTTP_REFERER", "home"))

def cart_view(request):
    cart = request.session.get("cart", {})
    items, total = [], Decimal("0.00")
    for product_id, quantity in cart.items():
        product = Product.objects.filter(pk=product_id, available=True).first()
        if product:
            qty = int(quantity)
            line_total = product.price * qty
            items.append({"product": product, "quantity": qty, "line_total": line_total})
            total += line_total
    return render(request, "shop/cart.html", {"items": items, "total": total})

@login_required
@transaction.atomic
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.info(request, "Your shopping bag is empty.")
        return redirect("cart")
    products = []
    total = Decimal("0.00")
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id, available=True)
        qty = int(quantity)
        if qty < 1 or product.stock < qty:
            messages.error(request, f"Not enough stock for {product.name}.")
            return redirect("cart")
        products.append((product, qty))
        total += product.price * qty
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        pincode = request.POST.get("pincode", "").strip()
        if not all([full_name, email, phone, address, city, pincode]):
            messages.error(request, "Please complete all delivery details.")
        else:
            order = Order.objects.create(user=request.user, full_name=full_name, email=email, phone=phone,
                address=address, city=city, pincode=pincode, total_amount=total,
                payment_method=request.POST.get("payment_method", "COD"))
            for product, qty in products:
                OrderItem.objects.create(order=order, product=product, product_name=product.name,
                    unit_price=product.price, quantity=qty)
                product.stock -= qty
                product.save(update_fields=["stock"])
            request.session["cart"] = {}
            send_mail(
                subject=f"Your Myntra demo order #{order.pk} is confirmed",
                message=f"Hello {order.full_name},\n\nThank you for your order.\nOrder ID: #{order.pk}\nTotal: ₹{order.total_amount}\nPayment: {order.payment_method}\n\nWe will share further updates when the order status changes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                fail_silently=True,
            )
            return redirect("order_success", order_id=order.pk)
    return render(request, "shop/checkout.html", {"items": products, "total": total})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, "shop/order_success.html", {"order": order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "shop/my_orders.html", {"orders": orders})
