from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
from django.shortcuts import render, get_object_or_404,redirect
from .models import Product,CartItem,Order, OrderItem
from .forms import ProductForm

@staff_member_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Change this to your desired URL
    else:
        form = ProductForm()
    return render(request, 'store/create-product.html', {'form': form})

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_details.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after signup
            return redirect('home')  # Change to your homepage
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def custom_logout_view(request):
    print("Inside inside logout ")
    logout(request)
    return redirect('login')

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')  # Show cart after adding

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def update_cart_quantity(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    if request.method == 'POST':
        new_qty = int(request.POST.get('quantity'))
        if new_qty > 0:
            item.quantity = new_qty
            item.save()
            messages.success(request, "Quantity updated.")
        else:
            item.delete()
            messages.info(request, "Item removed as quantity set to 0.")
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.info(request, "Your cart is empty.")
        return redirect('cart')

    total = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        # create order
        order = Order.objects.create(user=request.user, total_amount=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()  # clear the cart
        messages.success(request, "Your order has been placed successfully!")
        return redirect('order-confirmation', order.pk)

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def order_confirmation(request, pk):
    order = Order.objects.get(pk=pk, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})