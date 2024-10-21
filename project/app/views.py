from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import auth
from .models import CustomUser,User,Company

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
            if user.user_type=="user" and user.status=="accepted":
                return redirect(Userhome)
            elif user.user_type=="company":
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
    return render(request,'userhome.html',{'data1':data1})

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
        return redirect(Userhome)
    else:
        return render(request,'edit.html',{'data':data})

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
    data=CustomUser.objects.get(id=request.user.id)    
    data1=Company.objects.get(company_id=data)
    return render(request,'companyhome.html',{'data1':data1})
    