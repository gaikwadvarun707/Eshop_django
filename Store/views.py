from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .models import Product,Category,Customer,Order
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
from Store.middlewares.auth import auth_middleware,auth_checkout
from django.utils.decorators import method_decorator


class home(View):
    def post(s,request):
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1
                else:
                    cart[product]=quantity+1
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1
        
        request.session['cart']=cart
        # print(request.session['cart'])
        return redirect("/")

    def get(s,request):
        cart=request.session.get('cart')
        if not cart:
            request.session['cart']={}
        product=Product.objects.all()
        category=Category.objects.all()
        d={'product':product,'category':category}
        return render(request,"index.html",d)        

def category(request,cid):
    category=Category.objects.all()

    categor=Category.objects.get(pk=cid)
    
    product=Product.objects.filter(category=categor)

    d={'product':product,'category':category}
    return render(request,"index.html",d)

class signup(View):
    def get(s,request):
        return render(request,"signup.html")
    def post(s,request):
        postData=request.POST
        first_name=postData.get('firstname')
        last_name=postData.get('lastname')
        phone=postData.get('phone')
        email=postData.get('email')
        password=postData.get('password')
        value={'first_name':first_name,'last_name':last_name,'phone':phone,'email':email}

        #validation
            
        c=Customer(first_name=first_name,last_name=last_name,phone=phone,email=email,password=password)
        error_message=s.validatecustomer(c)
            
        #Saving 
        if not error_message:
            c.password=make_password(c.password)
            c.save()
            return redirect("/")
        else:
            d={'error':error_message,'values':value}          
            return render(request,"signup.html",d)
        
    def validatecustomer(s,c):
        error_message=None
        if not c.first_name:
            error_message="First Name Required !!"
        elif len(c.first_name)<4:
            error_message="First Name must be 4 character long or more"
        elif not c.last_name:
            error_message = 'Last Name Required'
        elif len(c.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not c.phone:
            error_message = 'Phone Number required'
        elif len(c.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif not c.password:
            error_message="password is Required !!"
        elif len(c.password) < 6:
            error_message = 'Password must be 6 char long'
        elif not c.email:
            error_message="email is required !!"
        elif len(c.email) < 5:
            error_message = 'Email must be 5 char long'
        elif c.isExists():
            error_message='Email address already registered..'
        return error_message

class login(View):
    return_url=None
    def get(s,request):
        login.return_url=request.GET.get('return_url')
        return render(request,"login.html")

    def post(s,request):
        email=request.POST.get('email')
        password=request.POST.get('password')
        customer=Customer.get_customer_by_email(email)
        error_message=None
        if customer:
            flag =check_password(password,customer.password)
            if flag:
                request.session['customer']=customer.id
                if login.return_url:
                    return HttpResponseRedirect(login.return_url)
                else:
                    login.return_url=None
                    return redirect("/")
            else:
                error_message="Email or Password invalid !!"
        else:
            error_message="Email or Password invalid !!"
        print(customer)
        return render(request,"login.html",{'error':error_message})

def logout(request):
    request.session.clear()
    return redirect("/login")

class cart(View):
    def get(s,request):
        ids=list(request.session.get('cart').keys())
        products=Product.get_product_by_id(ids)
        print(products)
        d={'products':products}
        return render(request,"cart.html",d)

class checkOut(View):
    @method_decorator(auth_checkout)
    def post(s,request):
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        customer=request.session.get('customer')
        cart=request.session.get('cart')
        products=Product.get_product_by_id(list(cart.keys()))

        for product in products:
            order=Order(customer=Customer(id=customer),product=product,price=product.price,address=address,phone=phone,quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart']={}
        return redirect("/cart")

class orders(View): 

    @method_decorator(auth_middleware)
    def get(s,request):
        customer=request.session.get('customer')
        orders=Order.get_orders_by_customer(customer)
        d={'orders':orders}
        return render(request,"orders.html",d)
