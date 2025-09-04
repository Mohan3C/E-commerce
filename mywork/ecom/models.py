from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    



class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    discount_price = models.FloatField(default=None)
    image = models.ImageField(upload_to="productimage/")
    description = models.TextField()

    def __str__(self):
        return self.title
    



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isordered = models.BooleanField(default=False)

    coupon_id = models.ForeignKey("Coupon",on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username
    

    def gettotalamount(self):
        total = 0
        for item in OrderItem.objects.filter(order_id=self.id):
            total += item.total_price()
        return total
    
    def gettotaldiscountamount(self):
        total_discount = 0
        for item in OrderItem.objects.filter(order_id=self.id):
            total_discount += item.total_discount_price()
        return total_discount
    
    def gettotaldiscount(self):
        return self.gettotalamount()-self.gettotaldiscountamount()

    def totaltax(self):
        return self.gettotaldiscountamount()*0.18
    
   
    def getpayableamount(self):
        if self.coupon_id:
            return self.gettotaldiscountamount() - self.coupon_id.amount + self.totaltax()
        else:
            return self.gettotaldiscountamount() + self.totaltax()

    
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    isordered = models.BooleanField(default=False)


    def __str__(self):
        return self.product_id.title
    

    def total_price(self):
        return self.product_id.price*self.qty
    
    def total_discount_price(self):
        return self.product_id.discount_price*self.qty
    
    def getpercentage(self):
        return(self.total_price()-self.total_discount_price())/self.total_price()*100
    

class Coupon(models.Model):
    code = models.CharField(max_length=200)
    amount = models.FloatField(blank=False,null=False)

    def __str__(self):
        return self.code
    