from django.db import models
 
class Photo(models.Model):
    path = models.CharField("Path", max_length=250)
    title = models.CharField("Title", max_length=250)


##############################
# Global tables
##############################

# Note: all global table names must be kept static (using Meta override)

# Franchise table: Store
# Contains store information such as name, description, and active status
class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True) # Required
    desc = models.TextField(blank=True, default='')
    phone = models.CharField(blank=True, default='', max_length=14)
    active = models.IntegerField(blank=True, default=0)
    
    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "Store" 

# Franchise table: Category
# Contains all possible categories for menu items
class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=250, unique=True) # Required

    def __unicode__(self):
        return self.cat_name

    class Meta:
        db_table = "Category"

# Franchise table: Menu
# Contains all menu products and their respective categories
class Menu(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=200, unique=True) # Required
    cat = models.ForeignKey(Category) # Required
    #op = models.ManyToManyField(Option)
    price = models.DecimalField(max_digits=6, decimal_places=2) # Required
    img_path = models.CharField(blank=True, default='', max_length=300) # Path to image file
    desc = models.CharField(blank=True, default='', max_length=500)

    def __unicode__(self):
        return self.prod_name

    class Meta:
        db_table = "Menu"

# Franchise table: Option
# Contains all possible options for menu items
class Option(models.Model):
    op_id = models.AutoField(primary_key=True)
    prod = models.ForeignKey(Menu) # Required
    # Note: op_name can be blank for cases where there really are no options
    op_name = models.CharField(blank=True, default='', max_length=250)
    price = models.DecimalField(blank=True, default=0, max_digits=6, decimal_places=2)

    def __unicode__(self):
        return self.op_name

    class Meta:
        db_table = "Option"
        unique_together = ["prod", "op_name"]

# Customer Table: Customer
# Contains customer information
class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100) # Required
    lname = models.CharField(max_length=100) # Required
    email = models.CharField(max_length=254, unique=True) # Required, used as user login
    # Encryption lengths: bcrypt max 76, sha256 max 64, sha512 max 128
    passhash = models.CharField(max_length=128) # Required
    store = models.ForeignKey(Store, blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.fname, self.lname)

    class Meta:
        db_table = "Customer"


##############################
# App specific tables
##############################

# Note: all app specific table names are dynamic according to app name

# Store table: Inventory
# Contains product stock levels, price and active status
class Inventory(models.Model):
    prod = models.ForeignKey(Menu) # required
    store = models.ForeignKey(Store) # required
    stock = models.IntegerField(blank=True, default=0)
    # discount multiplier (80% price = 0.8)
    discount = models.DecimalField(blank=True, default=1, max_digits=5, decimal_places=2)
    # 1 for active. Only active products will be displayed to customers
    active = models.IntegerField(blank=True, default=0)

    def __unicode__(self):
        return self.prod.prod_name

    class Meta:
        db_table = "Inventory"
        unique_together = ["prod", "store"]


# Store table: Order
# Contains order ID and timestamp of order.
class Order(models.Model):
    # each order ID corresponds to a paid shopping cart group
    ord_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store)
    cust = models.ForeignKey(Customer)
    # note, order creation is done only by cloud after payment confirmed
    time = models.DateTimeField()

    class Meta:
        db_table = "Order"

# Store table: OrderDetail
# Contains all items details corresponding to an order ID
class OrderDetail(models.Model):
    ord = models.ForeignKey(Order)
    prod = models.ForeignKey(Menu)
    op = models.ForeignKey(Option)
    active = models.IntegerField(blank=True, default=1)

    class Meta:
        db_table = "OrderDetail"


