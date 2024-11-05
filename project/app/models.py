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
    


class Product(models.Model):
    product_id=models.ForeignKey(Company,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    image=models.FileField(upload_to='media')
    description=models.CharField(max_length=100)
    price=models.IntegerField()
    catogory=models.CharField(null=True,blank=True,max_length=100)
    



class Cart(models.Model):
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1,null=True,blank=True)


class Order(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    cart_id=models.ForeignKey(Cart,on_delete=models.CASCADE)
    payment=models.IntegerField()
    paymentmethod=models.CharField(max_length=100)
    status=models.CharField(null=True,blank=True,max_length=100)
    

        