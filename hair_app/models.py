from django.db import models

# Create your models here.


class login_table(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    type=models.CharField(max_length=20)


class user_table(models.Model):
    LOGINID = models.ForeignKey(login_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    phone=models.BigIntegerField()
    gender=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    photo=models.FileField()
    dob=models.DateField()

class employee_table(models.Model):
    loginid = models.ForeignKey(login_table, on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    phone = models.BigIntegerField()
    photo = models.FileField()
    experience =models.CharField(max_length=10)
    Employee_type=models.CharField(max_length=80)
    language = models.CharField(max_length=50)

class services_table(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    cost = models.IntegerField()
    photo = models.FileField(upload_to='services/')
    category = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    Duration = models.CharField(max_length=30)

class BookingMaster(models.Model): # Order
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    EMPLOYEE=models.ForeignKey(employee_table,on_delete=models.CASCADE,blank=True,null=True)
    date = models.DateField()
    amount = models.IntegerField()
    From_time=models.TimeField(blank=True,null=True,default=None)
    To_time=models.TimeField(blank=True,null=True,default=None)
    status = models.CharField(max_length=30)

class BookingSub(models.Model): #Order Items
    BOOKING_MASTER = models.ForeignKey(BookingMaster, on_delete=models.CASCADE)
    SERVICE = models.ForeignKey(services_table, on_delete=models.CASCADE)
    price = models.IntegerField()
    status = models.CharField(max_length=30)

class Cart(models.Model):
    BOOKING_SUB = models.ForeignKey(BookingSub,on_delete=models.CASCADE)
    EMPLOYEE = models.ForeignKey(employee_table, on_delete=models.CASCADE,blank=True,null=True)
    from_time = models.TimeField()
    to_time = models.TimeField()
    status = models.CharField(max_length=30)



class Payment_table(models.Model):
    date=models.CharField(max_length=100)
    time=models.CharField(max_length=100)
    ORDER=models.ForeignKey(BookingMaster,on_delete=models.CASCADE)
    status=models.CharField(max_length=100)


class Feedbacks(models.Model):
    date=models.CharField(max_length=100)
    EMPLOYEE=models.ForeignKey(employee_table,on_delete=models.CASCADE)
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    rating=models.FloatField()
    feedback=models.CharField(max_length=100)


class Complaint(models.Model):
    date=models.CharField(max_length=100)
    BOOKING=models.ForeignKey(BookingMaster,on_delete=models.CASCADE)
    Complaint=models.CharField(max_length=100)
    Reply=models.CharField(max_length=100)

