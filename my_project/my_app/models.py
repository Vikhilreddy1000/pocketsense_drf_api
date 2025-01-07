from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, date


# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True )
    semester = models.IntegerField(blank=True, null=True)
    default_payment_methods = models.CharField(max_length=255, blank=True, null=True)
    otp = models.CharField(max_length=100, default="") 
    otp_verification = models.BooleanField(default=False) 
    # otp_sent_time = models.DateTimeField(blank=True, null=True)
    phone_no = models.CharField(max_length=100, default="") 
    country_code = models.CharField(max_length=17, default="") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    # accept_terms_and_conditions = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.name
    
#Group
class Group(models.Model):
    GROUP_TYPE = [ 
        ('HOSTEL_ROOMMATES', 'Hostel Roommates'), 
        ('PROJECT_TEAMS', 'Project Teams'), 
        ('TRIP_GROUPS', 'Trip Groups') 
    ]
    name = models.CharField(max_length=255, choices=GROUP_TYPE, default=None )
    members = models.ManyToManyField(CustomUser, related_name='member_groups')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

#Expense
class Expense(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    receipt_image = models.ImageField(upload_to='media/', null=True, blank=True)
    SPLIT_TYPE_CHOICES = [ 
        ('EQUAL', 'Equal'), 
        ('PERCENTAGE', 'Percentage'), 
        ('RATIO', 'Ratio') 
    ]
    split_type = models.CharField(max_length=20, choices=SPLIT_TYPE_CHOICES, default=None)
    group = models.ForeignKey(Group, related_name='expenses', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Settlement(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'), 
        ('COMPLETED', 'Complted')
    ]
    SETTLEMENT_METHOD = [
        ('CASH', 'Cash'), 
        ('ONLINE', 'Online')
    ]
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS, blank=True, null=True) 
    settlement_method = models.CharField(max_length=255, choices=SETTLEMENT_METHOD, blank=True, null=True) 
    due_date = models.DateField(auto_now_add=True)
    expense = models.ForeignKey(Expense, related_name='settlements', on_delete=models.CASCADE)
    settled_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True) 


#friendship
# class Friendship(models.Model):
#     user = models.ForeignKey(CustomUser, related_name="user", on_delete=models.CASCADE)
#     friend = models.ForeignKey(CustomUser, related_name="friend", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)

    




