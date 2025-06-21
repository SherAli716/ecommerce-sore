from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404,redirect
from .models import Product
from .forms import ProductForm

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


