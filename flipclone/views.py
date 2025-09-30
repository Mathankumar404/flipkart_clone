from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse;
from .models import Products,Cart;
import json;
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import traceback
# Create your views here.

def index(request):
    products = Products.objects.all() 
    
    return render(request,"index.html",{'products':products})

def detail(request,product_id):
    product = Products.objects.get(pk=product_id)
    return render(request,'ProductDetail.html',{"product":product})

def cart(request):
    cartitems=Cart.objects.all()
    return render(request,'cart.html',{"cart_items":cartitems})

def add_to_cart(request, product_id):
    product = Products.objects.get(pk=product_id)

    # Check if the product already exists in cart
    cart_item, created = Cart.objects.get_or_create(product=product)
    
    if not created:
        cart_item.quantity += 1  # increment quantity
        cart_item.save()
    else:
        cart_item.save()  # first time adding

    return redirect('cart') 

def cart_view(request):
    cart_items = Cart.objects.all()  # fetch all cart items
    
    return render(request, 'cart.html', {'cart_items': cart_items})

def remove_product(request):
    if request.method == "POST":
        try:
            # Parse raw body into dict
            data = json.loads(request.body.decode("utf-8"))
            
            # Extract product_id and convert to int
            product_id = int(data.get("product_id"))

            # Fetch and delete cart item
            cart_item = get_object_or_404(Cart, id=product_id)
            cart_item.delete()

            return JsonResponse({"success": True, "id": product_id})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False}, status=405)

@csrf_exempt
def search_products(request):
  
    if request.method == 'POST':
        query = request.POST.get("query", "").strip()  # or use json.loads(request.body) if JS sends JSON
        if query:
            products = Products.objects.filter(
                Q(title__icontains=query) |
                Q(brand__icontains=query)
            )
        else:
            products = Products.objects.all()

        # Convert QuerySet to list of dicts
        results = [
            {
                "id": p.id,
                "title": p.title,
                "brand": p.brand,
                "price": str(p.price),
                "offer": p.offer,
                "img": p.img,  # make sure this is a full URL or relative path
            }
            for p in products
        ]

        return render(request,"searchedProducts.html",{"products":results})

