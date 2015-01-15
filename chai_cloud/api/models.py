from django.db import models
 
class Photo(models.Model):
    path = models.CharField("Path", max_length=250)
    title = models.CharField("Title", max_length=250)


##############################
# Global tables
##############################

# Note: all global table names must be kept static

# Franchise table: Stores
# Contains store information such as name, description, and active status
class Stores(models.Model):
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True) # required
    desc = models.TextField(blank=True, default='')
    phone = models.CharField(blank=True, default='', max_length=12)
    active = models.IntegerField(blank=True, default=0)
    
    class Meta:
        db_table = "Stores" 

# Franchise table: Category
# Contains all possible categories for menu items
class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=250)

    class Meta:
        db_table = "Category"

# Franchise table: Option
# Contains all possible options for menu items
class Option(models.Model):
    op_id = models.AutoField(primary_key=True)
    op_name = models.CharField(blank=True, default='', max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = "Option"

# Franchise table: Menu
# Contains all menu products and their respective categories
class Menu(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=200, unique=True) # required
    cat = models.ForeignKey(Category)
    op = models.ManyToManyField(Option)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    img_path = models.CharField(blank=True, default='', max_length=300) # path to image file
    desc = models.CharField(blank=True, default='', max_length=500)

    class Meta:
        db_table = "Menu"

# Customer Table: Customer
# Contains customer information
class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=254)
    passhash = models.CharField(max_length=128) # bcrypt max 76, sha256 max 64, sha512 max 128
    store = models.ForeignKey(Stores)

    class Meta:
        db_table = "Customer"


##############################
# App specific tables
##############################

# Note: all app specific table names are dynamic according to app name

# Store table: Inventory
# Contains product stock levels, price and active status
class Inventory(models.Model):
    prod = models.ForeignKey(Menu)
    stock = models.IntegerField(blank=True, default=0) # required
    # discount multiplier (80% price = 0.8)
    discount = models.DecimalField(blank=True, default=1, max_digits=5, decimal_places=2)
    # 1 for active. Only active products will be displayed to customers
    active = models.IntegerField(blank=True, default=0)

# Store table: Order
# Contains order ID and timestamp of order.
class Order(models.Model):
    # each order ID corresponds to a paid shopping cart group
    ord_id = models.AutoField(primary_key=True)
    cust = models.ForeignKey(Customer)
    total_sale = models.DecimalField(max_digits=6, decimal_places=2)
    # note, order creation is done only by cloud after payment confirmed
    time = models.DateTimeField(auto_now_add=True)

# Store table: OrderDetail
# Contains all items details corresponding to an order ID
class OrderDetail(models.Model):
    ord = models.ForeignKey(Order)
    prod = models.ForeignKey(Inventory)

