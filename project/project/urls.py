"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('userregister',views.Register),
    path('companyregister',views.companyregister),
    path('login',views.Login),
    path('userhome',views.Userhome,name='userhome'),
    path('profileview',views.Profileview,name='profileview'),
    path('companyhome',views.Companyhome,name='companyhome'),
    path('companyprofile',views.Companyprofile,name='companyprofile'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('companyedit/<int:id>',views.companyedit,name='companyedit'),
    path('admin',views.admin),
    path('addproduct',views.addproduct,name='addproduct'),
    path('adminuseraccept/<int:id>',views.adminuseraccept,name='adminuseraccept'),
    path('viewproduct',views.viewproduct,name='viewproduct'),
    path('editproduct/<int:id>',views.editproduct,name='editproduct'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('userdetails',views.userdetails,name='userdetails'),
    path('userviewproduct',views.Userproductview,name='userviewproduct'),
    path('search',views.searchproduct),
    path('companydetails',views.Companydetails,name='companydetails'),
    path('viewproductdetails/<int:id>',views.viewproductdetails,name='viewproductdetails'),
    path('addtocart/<int:id>/',views.addtocart, name='addtocart'),
    path('viewcart',views.viewcart,name='viewcart'),
    path('deletecart/<int:id>',views.deletecart,name='deletecart'),
    path('editcart/<int:id>',views.editcart,name='editcart'),
    path('buyproduct/<int:id>',views.buyproduct,name='buyproduct'),
    path('cash/<int:id>',views.Cash_payment,name='cash'),
   
    path('debit_card_payment/<int:id>', views.debit_card_payment, name='debit_card_payment'),
    path('logout',views.Logout,name='logout'),
    path('allorders',views.allorders,name='allorders'),
    path('vieworder',views.vieworder,name='vieworder'),
    path('viewallproduct',views.Viewallproduct,name='viewallproduct'),
    path('confirmorder/<int:id>',views.confirmorder,name='confirmorder'),
    path('addtowhishlist/<int:id>',views.whishlist,name='addtowhishlist'),
    path('viewproducts',views.viewproducts,name='viewproducts'),
    path('products',views.products,name='products'),
    path('vieww',views.viewwishlist,name='vieww'),
    path('removefromwishlist/<int:id>',views.removefromwhishlist,name='removefromwishlist'),
    path('password_reset',views.password_reset_request,name='password_reset'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('set_new_password',views.set_new_password,name='set_new_password'),
    path('deleteorder/<int:id>/', views.deleteorders, name='deleteorder'),
    path('buyproducts/<int:id>',views.buyproducts,name='buyproducts'),
    path('category_list', views.category_list, name='category_list'),
    path('add_category', views.add_category, name='add_category'),
    path('delete_category/<int:id>',views.delete_category,name='delete_category'),
    path('cash2/<int:id>',views.Cashpayemt2,name='cash2'),
    path('debit_card_payment2/<int:id>', views.debit_card_payment2, name='debit_card_payment2'),
    path('search2',views.searchproduct2),
    
    
    
]

    


    





if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

