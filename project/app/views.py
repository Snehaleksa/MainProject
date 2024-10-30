from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import auth
from .models import CustomUser,User,Company,Product,Cart,Order

# Create your views here.
def index(request):
    return render(request,'index.html')
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
                'message':"Invalid credentiala"

            } 
            return render(request,'login.html',context)
    else:
        return render(request,'login.html')   


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
    return render(request,'userhome.html')    

    

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
    data=Product.objects.all()
    return render(request,'userproductview.html',{'data':data})

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
    if request.method=='POST':
        name=request.POST['name']
        image=request.FILES['image']
        description=request.POST['description']
        price=request.POST['price']
        
        data1=Product.objects.create(product_id=data,name=name,image=image,description=description,price=price)
        data1.save()
        return HttpResponse("success")
    else:
        return  render(request,'addproduct.html')
    

def viewproduct(request):
    company = Company.objects.get(company_id=request.user.id)
    products = Product.objects.filter(product_id=company)
    return render(request, 'viewproduct.html', {'products': products, 'company': company})



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




def viewproductdetails(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'viewproductdetails.html', {'product': product})




def addtocart(request,id):
    product = Product.objects.get( id=id)
    user=User.objects.get( user_id=request.user.id)
    if Cart.objects.filter(product_id=product, user_id=user).exists():
        return HttpResponse("Product already exist")
    else:
       cart_item=Cart.objects.create(product_id=product, user_id=user)
       cart_item.save()
       return HttpResponse("success") 

 




def viewcart(request):
    user = User.objects.get( user_id=request.user.id)
    data= Cart.objects.filter(user_id=user)
    return render(request, 'viewcart.html', {'data': data})

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


def Cash(request,id):
    data=Cart.objects.get(id=id)
    data1=data.product_id
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,'cash.html',{'data':data,'data1':data1,'user':user})

def placeorder(request):
    return render(request,'order.html')


# views.py

def debit_card_payment(request, id):
    user = User.objects.get(user_id=request.user.id)  
    cart_item = Cart.objects.get(id=id, user_id=user) 

    if request.method == 'POST':
        
        total_payment = cart_item.product_id.price * cart_item.quantity
        
        # Create an order with the required fields
        data=Order.objects.create(
            user_id=user,
            cart_id=cart_item,
            payment=total_payment,
            paymentmethod='Debit Card'
        )
        data.save()

        # Render confirmation page
        return render(request, 'order_confirmation.html', {
            'message': "Order placed successfully with Debit Card payment."
        })

    # If GET request, render the debit card payment form
    return render(request, 'debit_card_payment.html', {
        'cart_item': cart_item,
    })








