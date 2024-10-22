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
    path('userhome',views.Userhome),
    path('companyhome',views.Companyhome),
    path('edit/<int:id>',views.edit,name='edit'),
    path('admin',views.admin),
    path('addproduct',views.addproduct,name='addproduct'),
    path('adminuseraccept/<int:id>',views.adminuseraccept,name='adminuseraccept'),
    path('viewproduct',views.viewproduct,name='viewproduct'),
]


if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
