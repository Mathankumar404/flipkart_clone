from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse;
from .models import Products,Cart,User;
import json;
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
from .forms.signupform import SignupForm
from .forms.loginform import loginform
from django.contrib import messages

# Create your views here.

def index(request):
    products = Products.objects.all() 
    user_id = request.session.get("user_id")
    username = request.session.get("username")
    print("Session username:", username, "user_id:", user_id)
    
    # Pass a dict as 'user' so templates can access user.username
    user = {"id": user_id, "username": username} if user_id else None

    return render(request, "index.html", {'products': products, "user": user})
def detail(request,product_id):
    product = Products.objects.get(pk=product_id)
    return render(request,'ProductDetail.html',{"product":product})

def cart(request):
    if not request.session.get("user_id"):
        messages.error(request, "Please login to add products to cart")
        return redirect("login")
    user_id = request.session["user_id"]
    user = get_object_or_404(User, pk=user_id)
    cartitems = Cart.objects.filter(user=user)
    return render(request,'cart.html',{"cart_items":cartitems})

def add_to_cart(request, product_id):
    if not request.session.get("user_id"):
        messages.error(request, "Please login to add products to cart")
        return redirect("login")
    user_id = request.session["user_id"]
    user = get_object_or_404(User, pk=user_id)
    product = Products.objects.get(pk=product_id)

    # Check if the product already exists in cart
    cart_item, created = Cart.objects.get_or_create(user=user,product=product)
    
    if not created:
        cart_item.quantity += 1  # increment quantity
        cart_item.save()
    else:
        cart_item.save()  # first time adding

    return redirect('cart') 

def cart_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        messages.error(request, "Please login to view cart")
        return redirect("login")
    user = get_object_or_404(User, pk=user_id)
    cart_items = Cart.objects.filter(user=user).select_related("product")
    
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

@csrf_exempt
def login_page(request):
    if request.method=="POST":
        form=loginform(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"].strip()

            password = form.cleaned_data["password"]
            try:
                # Try finding user by username or phone_no
                user = User.objects.get(username=identifier)  # first try username
            except User.DoesNotExist:
                try:
                    user = User.objects.get(phone_no=identifier)  # then try phone_no
                except User.DoesNotExist:
                    user = None
            if user:
                if check_password(password, user.password):
                    request.session["user_id"] = user.id
                    request.session["username"] = user.username
                    messages.success(request, "Login successful!")
                    return redirect("index")
                else:
                    messages.error(request, "Invalid password")
            else:
                messages.error(request, "User not found")
    else:
        form = loginform()
    return render(request, "login.html", {"form": form})
    


@csrf_exempt
def signup_page(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "signup.html", {"success": "Account created!"})
        else:
            return render(request, "signup.html", {"form": form})
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})

@csrf_exempt
def logout_page(request):
    # Get user ID from session
    user_id = request.session.get("user_id")
    print("Session contents:", request.session.items())
# print to console / terminal

    # Clear the session
    request.session.flush()  

    messages.success(request, "Logged out successfully")
    return redirect("login")
