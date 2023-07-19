from django.db import models
#import User table
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
#to provide dropdown facility
DIVISION_CHOICE = (
    ('Dhaka', 'Dhaka'), #(front_view, backend_view)
    ('Rangpur', 'Rangpur'),
    ('Khulna', 'Khulna'),
    ('Barisal', 'Barisal'),
    ('Chattogram', 'Chattogram'),
    ('Cumilla', 'Cumilla'),
    ('Mymensing', 'Mymensing'),
    ('Syhlet', 'Syhlet'),
)
#for Customer Table(one to many)
#on_delete: models.CASCADE: if we del any row of customer tabel, it will delete the relatioship of correspoding row of user table
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    division = models.CharField(choices= DIVISION_CHOICE, max_length=50)
    district = models.CharField(max_length=200)
    thana = models.CharField(max_length=50)
    villorroad = models.CharField(max_length=50)
    zipcode = models.IntegerField()

    #method helps to produce unique ID for each customer
    def __str__(self):
        return str(self.id)

#Product Table    
#category tuples for dropdown
#set abbriviation for corresponding category
CATEGORY_CHOICES =(
    ('AB', 'Audio Book'), #(frontend_view, backend_view)
    ('EB', 'Ebook'),
    ('HB', 'Hover Board'),
    ('SP', 'Smartphone'),
    ('AC', 'Action Camera'),
    ('VR', 'Virtual Reality'),
)

#Product Table
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length = 3)
    #to store the image in define the path of Product Image Directory[evenif we upload it from other dir]
    product_image = models.ImageField(upload_to='productPhoto')

    def __str__(self):
        return str(self.id)
       

#Cart Table
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    #add additional property for checkout page for item wise total cost
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
    #to include individual shipping amount in checkout page
    @property
    def shipping_cost(self):
        return (self.quantity * self.product.discounted_price*1)/100
    
    #total saving
    def total_saving(self):
        return((self.quantity * self.product.selling_price) - (self.quantity * self.product.discounted_price))
        
    
#OrderPlaced Table(one to Many)
#OrderPlace Dropdown

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Reached at Warehouse', 'Reached at Warehouse'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)
#OrderPlaced Tableone to Many)
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending')
    
    #item wise totalcost additional variable
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

#to make the table, use terminal in virtual env
#python manage.py makemigrations
#python manage.py migrate

