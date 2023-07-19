from django.shortcuts import render
from django.views import View
#import models/DB from models.py
from .models import Customer, Product, Cart, OrderPlaced
#import forms for Registration
from .forms import CustomerRegistrationForm, CustomerProfileForm
#to show message
from django.contrib import messages
#import redirect for  add_to_cart
from django.shortcuts import redirect
#import java and Q for +/-/remove product
from django.db.models import Q
from django.http import JsonResponse
#decorator for class based views(for stop accessing link without login)
from django.utils.decorators import method_decorator
#decorator for function based views(for stop accessing link without login)
from django.contrib.auth.decorators import login_required
# Create your views here.
#product sliding
class ProductView(View):
    def get(self, request):
        ebook = Product.objects.filter(category = 'EB')
        hoverboard = Product.objects.filter(category = 'HB')
        smartphone = Product.objects.filter(category = 'SP')
        actioncamera = Product.objects.filter(category = 'AC')
        virtualreality = Product.objects.filter(category = 'VR')

        return render(request, 'Shop/home-2.html', {'ebook' : ebook,
                    'hoverboard' : hoverboard, 'smartphone' : smartphone, 
                    'actioncamera' : actioncamera, 'virtualreality' : virtualreality})

#previous product page for add-to-cart
class ProductDetailView(View):
    def get(self, request, pk):
        products = Product.objects.get(pk = pk)
        return render(request, 'Shop/productdetails.html', {'products' : products})

#customized product page   
class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        products = Product.objects.get(pk = pk)
        #apply condition same product already added in cart, it will not add individual section during next adding
        #build-in function of django
        item_already_in_cart = False
        if request.user.is_authenticated:
            #Cart: model name
            totalitem = len(Cart.objects.filter(user = request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=products.id) & Q(user = request.user)).exists()
        return render(request, 'Shop/productdetails.html', {'products' : products, 'item_already_in_cart' : item_already_in_cart})
    
    
    
#brandwise product for action camera

def actioncamera(request, data = None):
    #for no data and model: Product and variable names are from that model(category, brand, discounted_price)
    if data == None:
        actioncameras = Product.objects.filter(category = 'AC') 

    elif data == 'GoPro' or data == 'Ricoh-Theta-Z1' or data == 'Xiaomi':
        actioncameras = Product.objects.filter(category = 'AC').filter(brand = data)
    #for less than and equal (__lte)
    elif data == 'below':
        actioncameras = Product.objects.filter(category = 'AC').filter(discounted_price__lte =  24000)
    #for greater than (__gt)
    elif data == 'above':
        actioncameras = Product.objects.filter(category = 'AC').filter(discounted_price__gt = 24000)

    return render(request, 'Shop/category-page/actioncamera.html', {'actioncameras': actioncameras})
    
    
#forms.py: CustomerRegistrationForm
#create view for Registraion Class 
class CustomerRegistrationView(View):
    #self: to call attributes
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'Shop/customerregistration.html',{'form' : form})
    
    #create POST method not to show the user details on url
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        #check validation
        if form.is_valid():
            # to generate message after registration 
            messages.success(request,"Registred Successfully")
            # save the data in DB
            form.save()
        return render(request, 'Shop/customerregistration.html',{'form' : form})
        #else form will not save
    
#Customer Profile Form view
#decorator for class based views to limit access without login
@method_decorator(login_required, name = 'dispatch')
class profileview(View):
    #for class based view
    def get(self, request):
        #from forms.py
        form = CustomerProfileForm()
        #'active': 'btn-success'--for active selection
        return render(request, 'Shop/profile.html', {'form' : form, 'active': 'btn-success'})
    #to generate clean data after submission
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            division = form.cleaned_data['division']
            district = form.cleaned_data['district']
            thana = form.cleaned_data['thana']
            villorroad = form.cleaned_data['villorroad']
            zipcode = form.cleaned_data['zipcode']
            
            #Customer: model name
            reg = Customer(user = user, name = name, division = division, district = district,
                           thana = thana, villorroad = villorroad, zipcode = zipcode)
            reg.save()
            messages.success(request, 'Congrations! You have successfully completed your profile')
            return render(request, 'Shop/profile.html', {'form' : form, 'active': 'btn-success'})

            
#for address
#decorator for function based views to limit access without login
@login_required
def address(request):
    #call all the attributes of customer's table/model and filtering respect login user corresponding address
    add = Customer.objects.filter(user = request.user)
    return render(request, 'Shop/address.html', {'add':add, 'active':'btn-success'})

    
#shopping-cart
#decorator for function based views to limit access without login
@login_required
def add_to_cart(request):
    #curent user
    user = request.user
    #request.GET works as dictionary
    product_id = request.GET.get('prod_id')
    products = Product.objects.get(id=product_id)
    #user, product as per name of Cart model
    Cart(user=user, product=products).save()
    return redirect('/cart')
    
#show cart
#decorator for function based views to limit access without login
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        amount = 0.0
        shipping_amount =  (amount*1)/100
        totalamount = amount + shipping_amount
        #use short hand property/list comprehension for dynamic cart and product pricing
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                #as per Cart model attribute 
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                shipping_amount =  (amount*1)/100
                totalamount = amount + shipping_amount
            cart = Cart.objects.filter(user = user)
            return render(request, 'Shop/addtocart.html',{'carts' : cart, 'amount' : amount,
                                                      'totalamount' : totalamount, 
                                                      'shipping_amount' : shipping_amount })
        #for empty card
        else:
            return render(request, 'Shop/emptycard.html')

#plus-quantity
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        #call Cart table/model and attributes name should be as like as Cart model
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        #initail value 1 and incremental
        c.quantity +=1 
        c.save()
        amount = 0
        shipping_amount = (amount*1)/100
        #condition for authentic user
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            #as per Cart model attribute 
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            shipping_amount =  (amount*1)/100
            totalamount = amount + shipping_amount
        data = {
            'quantity': c.quantity,
            'amount' : amount,
            'shipping_amount': shipping_amount,
            'totalamount' : totalamount
        }
        
        return JsonResponse(data)
#minus-quantity
#plus-quantity
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        #call Cart table/model and attributes name should be as like as Cart model
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        #initail value 1 and incremental
        c.quantity -=1 
        c.save()
        amount = 0
        shipping_amount = (amount*1)/100
        #condition for authentic user
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            #as per Cart model attribute 
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            shipping_amount =  (amount*1)/100
            totalamount = amount + shipping_amount
        data = {
            'quantity': c.quantity,
            'amount' : amount,
            'shipping_amount': shipping_amount,
            'totalamount' : totalamount
        }
        
        return JsonResponse(data)

#remove cart
def remove_item(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        #call Cart table/model and attributes name should be as like as Cart model
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        #to delete item
        c.delete()
        amount = 0
        shipping_amount = (amount*1)/100
        #condition for authentic user
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            #as per Cart model attribute 
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            shipping_amount =  (amount*1)/100
            totalamount = amount + shipping_amount
        
        #update the below details once we remove any item
        data = {
            'amount' : amount,
            'shipping_amount': shipping_amount,
            'totalamount' : totalamount
        }
        
        return JsonResponse(data)
    
def buy_now(request):
    return render(request, 'Shop/buynow.html')


def login(request):
     return render(request, 'Shop/login.html')

#def customerregistration(request):
    #return render(request, 'Shop/customerregistration.html')

#checkout page
#decorator for function based views to limit access without login
@login_required
def checkout(request):
    
    #currently login user
    user = request.user
    #filter coresponding user from all user for address details
    add = Customer.objects.filter(user=user)
    #filter coresponding user from all user for cart_items
    cart_items = Cart.objects.filter(user=user)
    amount = 0
    shipping_amount = (amount*1)/100
    savings = 0
    #condition for authentic user
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            #as per Cart model attribute connects with product model
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            shipping_amount =  (amount*1)/100
        totalamount = amount + shipping_amount
        
        #total amount of savings after discount
        for p in cart_product:
            #as per Cart model attribute connects with product model
            tempamount = (p.quantity * p.product.discounted_price)
            tempprice = (p.quantity * p.product.selling_price)
            tempsavings = tempprice - tempamount
            savings += tempsavings
        totalsavings = savings

    
    return render(request, 'Shop/checkout.html', {'add' : add, 'totalamount' : totalamount, 'shipping_amount': shipping_amount, 'cart_items': cart_items, 'totalsavings' : totalsavings})
#order page
#decorator for function based views to limit access without login
@login_required
def orders(request):
    #filter the objects from OrderPlaced DB based on Current user
    op = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'Shop/orders.html', {'order_placed' : op})

#payment_done
#decorator for function based views to limit access without login
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    
    #Customer model/DB
    customer = Customer.objects.get(id = custid)
    #Cart model/DB
    cart = Cart.objects.filter(user = user)
    for c in cart:
        #OrderPlaced Model/DB
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
        
    #details of checkout will be stored in class OrderPlaced model/DB and delete from Cart DB

    return redirect("orders")
        
    

#def change_password(request):
 #return render(request, 'Shop/changepassword.html')


#categorywise product page
def virtualreality(request, data = None):
    #for no data and model: Product and variable names are from that model(category, brand, discounted_price)
    if data == None:
        virtualrealities = Product.objects.filter(category = 'VR') 

    elif data == 'BNEXT' or data == 'HTC' or data == 'OIVO' or data == 'Oculus' or data == 'Others':
         virtualrealities = Product.objects.filter(category = 'VR').filter(brand = data)
    #for less than and equal (__lte)
    elif data == 'below':
         virtualrealities = Product.objects.filter(category = 'VR').filter(discounted_price__lte =  24000)
    #for greater than (__gt)
    elif data == 'above':
         virtualrealities = Product.objects.filter(category = 'VR').filter(discounted_price__gt = 24000)

    return render(request, 'Shop/category-page/virtualreality.html', {'virtualrealities':  virtualrealities})

#categorywise product page
def hoverboard(request, data = None):
    #for no data and model: Product and variable names are from that model(category, brand, discounted_price)
    if data == None:
        hoverboards = Product.objects.filter(category = 'HB') 

    elif data == 'Titan-Electric' or data == 'Tomoloo' or data == 'Segway' or data == 'Swagtron' or data == 'Others':
         hoverboards = Product.objects.filter(category = 'HB').filter(brand = data)
    #for less than and equal (__lte)
    elif data == 'below':
         hoverboards = Product.objects.filter(category = 'HB').filter(discounted_price__lte =  24000)
    #for greater than (__gt)
    elif data == 'above':
         hoverboards = Product.objects.filter(category = 'HB').filter(discounted_price__gt = 24000)

    return render(request, 'Shop/category-page/hoverboard.html', {'hoverboards':  hoverboards})


#categorywise product page
def smartphone(request, data = None):
    #for no data and model: Product and variable names are from that model(category, brand, discounted_price)
    if data == None:
        smartphones = Product.objects.filter(category = 'SP') 

    elif data == 'One-Plus' or data == 'Xiaomi' or data == 'Apple' or data == 'Others':
         smartphones = Product.objects.filter(category = 'SP').filter(brand = data)
    #for less than and equal (__lte)
    elif data == 'below':
         smartphones = Product.objects.filter(category = 'SP').filter(discounted_price__lte =  35000)
    #for greater than (__gt)
    elif data == 'above':
         smartphones = Product.objects.filter(category = 'SP').filter(discounted_price__gt = 35000)

    return render(request, 'Shop/category-page/smartphone.html', {'smartphones':  smartphones})

#categorywise product page
def ebook(request, data = None):
    #for no data and model: Product and variable names are from that model(category, brand, discounted_price)
    if data == None:
        ebooks = Product.objects.filter(category = 'EB') 

    elif data == 'Kotobee' or data == 'Kindle' or data == 'Others':
         ebooks = Product.objects.filter(category = 'EB').filter(brand = data)
    #for less than and equal (__lte)
    elif data == 'below':
         ebooks = Product.objects.filter(category = 'EB').filter(discounted_price__lte = 350)
    #for greater than (__gt)
    elif data == 'above':
         ebooks = Product.objects.filter(category = 'EB').filter(discounted_price__gt = 350)

    return render(request, 'Shop/category-page/ebook.html', {'ebooks':  ebooks})

#categorywise product page
def audiobook(request, data = None):
    #for no data and model: Product and variable names are from that model(category, brand, discounted_price)
    if data == None:
        audiobooks = Product.objects.filter(category = 'AB') 

    elif data == 'Hachette' or data == 'Macmillan' or data == 'Audible' or data == 'Others':
         audiobooks = Product.objects.filter(category = 'AB').filter(brand = data)
    #for less than and equal (__lte)
    elif data == 'below':
         audiobooks = Product.objects.filter(category = 'AB').filter(discounted_price__lte = 3250)
    #for greater than (__gt)
    elif data == 'above':
         audiobooks = Product.objects.filter(category = 'AB').filter(discounted_price__gt = 3250)

    return render(request, 'Shop/category-page/audiobook.html', {'audiobooks':  audiobooks})