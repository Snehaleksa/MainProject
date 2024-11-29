from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import auth
from .models import CustomUser,User,Company,Product,Cart,Order,Whishlist,Category
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import random
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.

def send_otp(email):
    otp = random.randint(100000,999999)
    send_mail(
        'Your OTP Code',
        f'Your OTP code is: {otp}',
        'snehaleksa2016@gmail.com',
        [email],
        fail_silently=False,
    )
    return otp

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = send_otp(email)

            context = {
                        "email": email,
                        "otp": otp,
            }
            return render(request,'verify_otp.html',context)
        
        except User.DoesNotExist:
            messages.error(request,'Email address not found.')
    else:
        return render(request,'password_reset.html')
    return render(request,'password_reset.html') 

def verify_otp(request):
    if request.method == 'POST':
        email =request.POST.get('email')
        otpold = request.POST.get('otpold')
        otp = request.POST.get('otp')

        if otpold==otp :
            context = {
                'otp' : otp,
                'email': email
            }
            return render(request,'set_new_password.html',context)
        else:
            messages.error(request,"Invalid OTP")
    return render(request,'verify_otp.html') 

def set_new_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password==confirm_password:
            try:
                data = User.objects.get(email=email)
                user=CustomUser.objects.get(id=data.user_id.id)
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password has been reset successfully')
                return redirect(Login)
            except User.DoesNotExist:
                messages.error(request,'Password doesnot match')
        return render(request,'set_new_password.html',{'email':email})               
    return render(request,'set_new_password.html',{'email':email})
def index(request):
    products=Product.objects.all()
    return render(request,'index.html',{'products':products})
def Login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user =authenticate(username=username,password=password)
        admin_user=authenticate(request,username=username,password=password)
        if admin_user is not None and admin_user.is_staff:
            login(request,admin_user)
            return redirect(admin)
        

        if user is not None:
            login(request,user)
            if user.user_type=="user" :
                return redirect(Userhome)
            elif user.user_type=="company" and user.status=="accepted":
                return redirect(Companyhome)
            else:
                return render(request,'login.html',{'message':"admin not aproved"})
        else:
            context={
                'message':"Invalid credentials"

            } 
            return render(request,'login.html',context)
    else:
        return render(request,'login.html')   
    

def Logout(request):
    auth.logout(request)
    return redirect(Login)    


def admin(request):
    return render(request,'admin.html')


def adminhome(request):
    user=Company.objects.all()   
    return render(request,'adminhome.html',{'user':user}) 

def adminuseraccept(request,id):
    data=Company.objects.get(id=id)
    if request.method=='POST':                                   
        status =request.POST.get('status')
        if status=='accepted':
            data.company_id.status='accepted'
        elif status=='rejected':
            data.company_id.status='rejected'
        data.company_id.save()
        return redirect(admin)
    else:
        return redirect(admin)


def userdetails(request):
    data=User.objects.all()
    return render(request,'userdetails.html',{'data':data})

def Companydetails(request):
    data=Company.objects.all()
    return render(request,'companydetails.html',{'data':data})

def Viewallproduct(request):
    data=Company.objects.all()
    data1=Product.objects.all()
    return render(request,'allproduct.html',{'data':data,'data1':data1})

 


#User

def Register(request):
    if request.method=='POST':
        name=request.POST['name']
        username=request.POST['username']
        password=request.POST['password']
        image=request.FILES['image']
        address=request.POST['address']
        email=request.POST['email']
        phone=request.POST['phone']
        data=CustomUser.objects.create_user(username=username,password=password,user_type='user')
        data1=User.objects.create(user_id=data,name=name,image=image,address=address,email=email,phone=phone)
        data1.save()
        return HttpResponse("success")
    else:
        return render(request,"userregister.html")
    

def Userhome(request):
    data=CustomUser.objects.get(id=request.user.id)
    data1=User.objects.get(user_id=data)
    cartnumber=Cart.objects.filter(user_id=data1).count
    data2=Product.objects.all()
    return render(request,'userhome.html',{'data1':data1,'data2':data2,'cartnumber':cartnumber})    

    

def Profileview(request):
    data=CustomUser.objects.get(id=request.user.id)
    data1=User.objects.get(user_id=data)
    return render(request,'profileview.html',{'data1':data1})

def edit(request,id):
    data=User.objects.get(id=id)
    if request.method=='POST':
        data.name=request.POST['name']
        if 'image' in request.FILES:
            data.image=request.FILES['image']
        data.address=request.POST['address']
        data.email=request.POST['email']
        data.phone=request.POST['phone']
        data.save()
        return redirect(Profileview)
    else:
        return render(request,'edit.html',{'data':data})





def Userproductview(request):
    id=CustomUser.objects.get(id=request.user.id)
    user = User.objects.get( user_id=id)
    data=Product.objects.all()
    wishlist=Whishlist.objects.filter(user_id=user).values_list('product_id',flat=True)
    return render(request,'userproductview.html',{'data':data,'wishlist':wishlist})

def searchproduct(request):
    if request.method=='POST':
        search=request.POST.get('search')
        data=Product.objects.filter(name__icontains=search)
        return render(request,'userproductview.html',{'data':data})



#Company
def companyregister(request):
    if request.method=='POST':
        name=request.POST['name']
        username=request.POST['username']
        password=request.POST['password']
        address=request.POST['address']
        contactnumber=request.POST['contactnumber']
        email=request.POST['email']
        data=CustomUser.objects.create_user(username=username,password=password,user_type='company')
        data1=Company.objects.create(company_id=data,name=name,address=address,contactnumber=contactnumber,email=email)
        data1.save()
        return HttpResponse("success")
    
    else:
        return render(request,"companyregister.html")
    
def Companyhome(request):
    return render(request,'companyhome.html')    
    
def Companyprofile(request):
    data=CustomUser.objects.get(id=request.user.id)    
    data1=Company.objects.get(company_id=data)
    return render(request,'companyprofile.html',{'data1':data1})

def companyedit(request,id):
    data=Company.objects.get(id=id)
    if request.method=='POST':
        data.name=request.POST['name']
        data.address=request.POST['address']
        data.contactnumber=request.POST['contactnumber']
        data.email=request.POST['email']
        data.save()
        return redirect(Companyprofile)
    else:
        return render(request,'companyedit.html',{'data':data})




#Product
def addproduct(request):
    data=Company.objects.get(company_id=request.user.id)
    data1=Category.objects.all()

    if request.method=='POST':
        name=request.POST['name']
        image=request.FILES['image']
        description=request.POST['description']
        price=request.POST['price']
        category =request.POST['category']
        product_quantity=request.POST['product_quantity']
        data2=Category.objects.get(id=category)
        data1=Product.objects.create(product_id=data,name=name,image=image,description=description,price=price,category=category,product_quantity=product_quantity)
        
    
        data1.save()
        return redirect(Companyhome)
    else:
        return  render(request,'addproduct.html',{'data1':data1})
    

def viewproduct(request):
    company = Company.objects.get(company_id=request.user.id)
    products = Product.objects.filter(product_id=company)
    items_per_page=2
    paginator=Paginator(products,items_per_page)
    page=request.GET.get('page',1)

    try:
        products=paginator.page(page)
    except PageNotAnInteger:
        products=paginator.page(1)
    except EmptyPage:
        products=paginator.page(paginator.num_pages) 
    context={
        'products':products,
        'company':company
    }      
    return render(request, 'viewproduct.html',context)



def editproduct(request, id):
    
    data = Product.objects.get(id=id)


    if request.method == 'POST':
        data.name = request.POST['name']
        data.description = request.POST['description']
        data.price = request.POST['price']
        if 'image' in request.FILES:
            data.image = request.FILES['image']
        data.save() 
        return redirect(viewproduct) 
    return render(request, 'editproduct.html', {'data': data})


def delete(request,id):
    data=Product.objects.get(id=id)
    data.delete()
    return redirect(viewproduct)    


def get_product(request):
    data=Product.objects.all()
    return render(request,'userhome.html',{'data':data})    




def viewproductdetails(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'viewproductdetails.html', {'product': product})




def addtocart(request,id):
    product = Product.objects.get( id=id)
    user=User.objects.get( user_id=request.user.id)
    if Cart.objects.filter(product_id=product, user_id=user).exists():
        return redirect(Userproductview)
    else:
       cart_item=Cart.objects.create(product_id=product, user_id=user)
       cart_item.save()
       return redirect(Userproductview) 

 




def viewcart(request):
    user = User.objects.get( user_id=request.user.id)
    data= Cart.objects.filter(user_id=user)
    total_price=0
    for i in data:
        total_price= total_price+i.product_id.price

    items_per_page=2
    paginator=Paginator(data,items_per_page)
    page=request.GET.get('page',1)

    try:
        data=paginator.page(page)
    except PageNotAnInteger:
        data=paginator.page(1)
    except EmptyPage:
        data=paginator.page(paginator.num_pages) 
    context={
        'data':data,
        'total_price':total_price
    }  
    return render(request, 'viewcart.html',context)

def deletecart(request,id):
    data=Cart.objects.get(id=id)
    data.delete()
    return redirect(viewcart)

def editcart(request,id):
    data=Cart.objects.get(id=id)
    if request.method=='POST':
        data.quantity=request.POST['quantity'] 
        data.save()  
        return redirect(viewcart)
    else:
        return render(request,'editcart.html',{'data':data})
    

def buyproduct(request,id):
    data=Cart.objects.get(id=id)
    data1=data.product_id
    totalprice = data1.price * data.quantity
    
    return render(request,'buyproduct.html',{'data':data,'data1':data1,'totalprice':totalprice}) 

#order
def Cash_payment(request,id):
    data=Cart.objects.get(id=id)
    data1=data.product_id
    user=User.objects.get(user_id=request.user.id)
    total_payment=data1.price*data.quantity
    if request.method=='POST':
        order=Order.objects.create(user_id=user,cart_id=data,payment=total_payment,paymentmethod='Cash',status='order send')
        order.save()
        data.product_id.product_quantity=data.product_id.product_quantity-data.quantity
        data.save()
        return render(request,'order.html',{'data':data,'data1':data1,'user':user,'total_payment':total_payment})
    else:
        return render(request,'cash.html',{'data':data,'user':user,'total_payment':total_payment,'data.product_id.product_quantity':data.product_id.product_quantity})





def debit_card_payment(request, id):
    user = User.objects.get(user_id=request.user.id) 
    data= Cart.objects.get(id=id) 
    total_payment=data.product_id.price* data.quantity
    if request.method == 'POST':
       
        data1=Order.objects.create(user_id=user,cart_id=data,payment=total_payment,paymentmethod='Debitcard',status='order send')
        data1.save()    
        return render(request, 'order_confirmation.html')
    else:
       return render(request, 'debit_card_payment.html', {'data': data,'total_payment':total_payment})
        





def allorders(request):
    data=CustomUser.objects.get(id=request.user.id)
    compani=Company.objects.get(company_id=data)
    order=Order.objects.filter(cart_id__product_id__product_id=compani)
    return render(request,'allorders.html',{'orders':order})

def vieworder(request):
    user = User.objects.get(user_id=request.user.id) 
    orders = Order.objects.filter(user_id=user)
    return render(request, 'userorder.html', {'orders': orders})


def deleteorders(request, id):
    
    data = Order.objects.get(id=id)
    data.delete()
    return redirect('vieworder')
    



def confirmorder( request,id):
    order = Order.objects.get( id=id)
    if order.status == 'order send':
        order.status = 'order confirmed'
        order.save()
    return redirect(allorders)


#Whislist
def whishlist(request,id):
    product = Product.objects.get(id=id)
    user = User.objects.get(user_id=request.user.id)
    wishlist = Whishlist.objects.filter(product_id=product, user_id=user)
    if wishlist.exists():
       wishlist.delete()
    else:
        Whishlist.objects.create(product_id=product, user_id=user)
    return redirect(Userproductview)

   

def removefromwhishlist(request, id):
    
    product = Product.objects.get( id=id)
    user = User.objects.get(user_id=request.user.id)
    Whishlist.objects.filter(product_id=product, user_id=user).delete()
    
    return redirect(Userproductview)


def viewwishlist(request):
    user=User.objects.get(user_id=request.user.id)
    data=Whishlist.objects.filter(user_id=user)
    return render(request,'whishlist.html',{'data':data})


def viewproducts(request):
    data=Product.objects.all()
    return render(request,'viewallproducts.html',{'data':data})

def products(request):
    data=Product.objects.all()
    return render(request,'products.html',{'data':data})


def buyproducts(request,id):
    product = Product.objects.get(id=id)
    
    total_payment=product.price
    return render(request,'buyproducts.html',{'product':product,'total_payment':total_payment}) 


def Cashpayemt2(request,id):
    data=Product.objects.get(id=id)
    user=User.objects.get(user_id=request.user.id)
    total_payment=data.price
    if request.method=='POST':
        order=Order.objects.create(user_id=user,product_id=data,payment=total_payment,paymentmethod='Cash',status='order send')
        order.save()
        #data.product_id.product_quantity=data.product_id.product_quantity-data.quantity
        #data.save()
        return render(request,'order.html',{'data':data,'user':user,'total_payment':total_payment})
    else:
        return render(request,'cash2.html',{'data':data,'user':user,'total_payment':total_payment})
    
def debit_card_payment2(request, id):
    user = User.objects.get(user_id=request.user.id) 
    data= Product.objects.get(id=id) 
    total_payment=data.price
    if request.method == 'POST':
       
        data1=Order.objects.create(user_id=user,product_id=data,payment=total_payment,paymentmethod='Debitcard',status='order send')
        data1.save()    
        return render(request, 'order_confirmation.html')
    else:
       return render(request, 'debit_card_payment2.html', {'data': data,'total_payment':total_payment})    



def add_category(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        data=Category.objects.create(name=category_name)
        data.save()
            
    return render(request, 'add_category.html')

def category_list(request):
    data = Category.objects.all()
    return render(request, 'category_list.html', {'data': data})

def delete_category(request,id):
    data=Category.objects.get(id=id)
    data.delete()
    return redirect(category_list)

