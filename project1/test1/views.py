from django.shortcuts import render, HttpResponse , redirect

# Pagination
from django.core.paginator import Paginator

#  Render HTML Products, Contact Page
from .models import Product, Contact_Query

# Authentication to login, logout site
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

# Authentication Forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def home(request):
  # fetch data from database
  product_info = Product.objects.all()
  print(product_info)
  return render(request, 'test1/home.html', {'product_info': product_info})

def findproduct(request):
  if request.method == "POST":
    x = request.POST.get("prod_search")
    print(x)
    data_object = Product.objects.filter(Q(product_id__contains=x) | Q(product_name__contains=x) | Q(product_category__contains=x))
    print(data_object)
    if data_object:
      return render(request, "test1/home.html", {'product_info': data_object})
    else:
      return render(request, "test1/home.html", {'warning': 'Product not found'}, status=404)
  
    

def contact(request):
  return HttpResponse("<h1>Contact Page</h1>")

def about(request):
  return HttpResponse("<h1>About Page</h1>")
@login_required(login_url='loginuser')
def products(request):
  all_products = Product.objects.all()
  paginator = Paginator(all_products, 3)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, "test1/products.html", {'page_obj': page_obj})

def contact(request):
  if request.method == "GET":
    return render(request, "test1/contact.html")
  else:
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    
    new_data = Contact_Query(name=name, email=email, message=message)
    new_data.save()
    return render(request, "test1/contact.html", {'x': 'Message sent successfully. Thank you for your message'})

def loginuser(request):
  if request.method == "GET":
    return render(request, "test1/loginuser.html", {'form': AuthenticationForm()})
  else:
    a = request.POST.get('username')
    b = request.POST.get('password')
    user = authenticate(request, username=a, password=b)
    if user is None:
      return render(request, 'test1/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username or Password is incorrect.'})
    else:
      login(request, user)
      return redirect("home")
  
def signupuser(request):
  if request.method == "GET":
    return render(request, "test1/signupuser.html", {'form': UserCreationForm()})
  else:
    a = request.POST.get('username')
    b = request.POST.get('password1')
    c = request.POST.get('password2')
    if b == c:
      # check if user exists
      if (User.objects.filter(username = a)):
        return render(request, "test1/signupuser.html", {'form': UserCreationForm(), 'error': 'Username already exists'})
      else:
        user = User.objects.create_user(username=a, password=b)
        user.save()
        login(request, user)
        return redirect("home")
    else:
      return render(request, "test1/signupuser.html", {'form': UserCreationForm(), 'error': 'Password does not match'})  
     
  
def logoutuser(request):
  if request.method == "GET":
    logout(request)
    return redirect("home")