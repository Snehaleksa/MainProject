from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    status_choice=(('accepted','accepted'),('rejected','rejected'))
    user_type=models.CharField(max_length=100)
    status=models.CharField(choices=status_choice,default='pending',max_length=100)


class User(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    image=models.FileField(upload_to='media')
    address=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.IntegerField()


    def __str__(self):
        return self.name


class Company(models.Model):
    company_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE) 
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    contactnumber=models.IntegerField(null=True,blank=True)
    email= models.CharField(max_length=100)  

    def __str__(self):
        return self.name
    
class Size(models.Model):
    name=models.CharField(max_length=100)


    def __str__(self):
        return self.name
    

class Color(models.Model):
    name=models.CharField(max_length=100) 


    def __str__(self):
        return self.name   

class Product(models.Model):
    product_id=models.ForeignKey(Company,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    image=models.FileField(upload_to='media')
    description=models.CharField(max_length=100)
    price=models.IntegerField()
    category=models.CharField(null=True,blank=True,max_length=100)
    product_quantity=models.IntegerField(null=True,blank=True)
    color = models.ManyToManyField(Color)
    size = models.ManyToManyField(Size)
    
    
    



class Cart(models.Model):
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    
    quantity=models.IntegerField(default=1,null=True,blank=True)
    size=models.CharField(max_length=100,null=True,blank=True)
    


class Order(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    payment=models.IntegerField()
    paymentmethod=models.CharField(max_length=100)
    status=models.CharField(null=True,blank=True,max_length=100)

class Whishlist(models.Model):
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)        




class Category(models.Model):
    name = models.CharField(max_length=100)

    
