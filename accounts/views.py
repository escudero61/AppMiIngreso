from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import CreateUserForm
from .forms import OrderForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,   login,  logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        contex = {'form': form}
        return render(request, 'accounts/register.html', contex)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        contex = {}
        return render(request, 'accounts/login.html', contex)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url ='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending}

    return render(request,'accounts/dashboard.html',context)

@login_required(login_url ='login')
def products(request):
    products = Products.objects.all()
    return render(request,'accounts/products.html', {'products': products})

@login_required(login_url ='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    context = {'custumer':customer,'orders': orders, 'order_count': order_count}
    return render(request, 'accounts/Customer.html',context)

@login_required(login_url ='login')
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        #print('printing POST:', request.POST)
        form = OrderForm(request.POST)
        if  form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html',context)

@login_required(login_url ='login')
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html',context)

@login_required(login_url ='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html',context)