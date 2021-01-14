from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import LedgerForm, DealerForm, RoadExpenseForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.core.paginator import Paginator, EmptyPage

#LEDGER
@login_required(login_url='loginuser')
@admin_only
def home(request):
    #this edit to solve the MultiValueDictKeyError
    query = request.POST.get('query', False)

    alldealers = Dealer.objects.filter(name__icontains=query)
    context = {'alldealers':alldealers}
    return render(request, 'ledger/home.html', context)

@login_required(login_url='loginuser')
@allowed_users(allowed_roles=['admin'])
def ledger(request, pk):
    dealer = Dealer.objects.get(id=pk)
    form = LedgerForm(initial={"dealer":dealer},instance=dealer)
    if request.method == 'GET':
        return render(request, 'ledger/ledger.html', {'form':form})
    else:
        form = LedgerForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            return redirect('dealer', pk)

@login_required(login_url='loginuser')
@allowed_users(allowed_roles=['admin'])
def dealer(request, pk):
    dealer = Dealer.objects.get(id=pk)
    ledgers = dealer.ledger_set.all()
    orderedledger = ledgers.order_by('-date')

    #paginating
    p = Paginator(orderedledger, 2)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context = {'dealer':dealer, 'ledgers':ledgers,'orderedledger':page }
    return render(request, 'ledger/dealer.html', context)

@login_required(login_url='loginuser')
@allowed_users(allowed_roles=['admin'])
def dealerform(request):
    if request.method == 'GET':
        return render(request, 'ledger/dealerform.html', {'form':DealerForm()})
    else:
        form = DealerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

@login_required(login_url='loginuser')
def userpage(request):
    userobjects = ViewDealer.objects.get(user=request.user)
    dealerallowed = userobjects.dealer.all()
    ledger_list = []
    for i in dealers.all():
        ledger = Ledger.objects.filter(dealer=i)
        ledger_list.append(ledger)
        print(i.name, i.mob_num)
    print(ledger_list)
    # ledgers = dealerallowed.dealer
    # print("Ledgers", dealerallowed.user.username)
    # print(ledgers)
    # print("Loop")

    context = {'dealerallowed':dealerallowed}
    return render(request, 'ledger/user.html', context)

def roadexpense(request):
    if request.method == 'GET':
        return render(request, 'ledger/expense.html', {'form':RoadExpenseForm()})
    else:
        form = RoadExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

# AUTHENTICATION FUNCTIONS

@unauthenticated_user
def loginuser(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'ledger/home.html', {'form':AuthenticationForm(), 'error': 'Username or Password did not match'})
        else:
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'ledger/login.html', {'form':AuthenticationForm()})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')