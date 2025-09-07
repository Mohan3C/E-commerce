from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

from .admin import Category,Product,Order,OrderItem
from .admin_forms import *
# Create your views here.

# def home(request):
#   data = {}
#   data["categories"] = Category.objects.all()
#   data["products"] = Product.objects.all()
#   return render(request,'main.html',data)


def home(request):
  categories = Category.objects.all()
  products = Product.objects.all()
  pagination = Paginator(products,per_page=8)
  page_number = request.GET.get('page')
  page_obj = pagination.get_page(page_number)

  return render(request, "main.html",{"page_obj":page_obj,"categories":categories})

def viewproduct(request,id):
  data = {}
  data["product"] = Product.objects.get(id = id)

  return render (request,"view_product.html",data)



def registeruser(request):
  form = UserCreationForm(request.POST or None)

  if request.method == "POST":
    if form.is_valid():
      form.save()
      return redirect("login")  
  else:
    form = UserCreationForm()

  return render(request,"registration/registration.html",{"form":form})

def filter_product(request,cat_id):
  categories = Category.objects.all()
  products = Product.objects.filter(category_id = cat_id)
  paging = Paginator(products,8)
  page_number = request.GET.get('page')
  page_obj = paging.get_page(page_number)
  
  return render(request,"main.html",{"categories":categories,"page_obj":page_obj})

@login_required
def addtocart(request,product_id):
  product = get_object_or_404(Product,id = product_id)
  
  orders = Order.objects.filter(user=request.user, isordered = False)

  if orders.exists():
    order = orders[0]
    existorderitem = OrderItem.objects.filter(user=request.user,isordered=False,product_id=product,order_id=order).exists()

    if existorderitem:
      existoi = OrderItem.objects.get(user=request.user,isordered=False,product_id=product,order_id=order)
      existoi.qty += 1
      existoi.save()
    else:
      oi = OrderItem()
      oi.user = request.user
      oi.isordered = False
      oi.product_id = product
      oi.order_id = order
      oi.save()
  else:
    o = Order()
    o.user = request.user
    o.save()

    oi = OrderItem()
    oi.user = request.user
    oi.isordered = False
    oi.product_id = product
    oi.order_id = o
    oi.save()

  return redirect("cart")

@login_required()
def cart(request):
  order = Order.objects.filter(user=request.user,isordered = False).first()
  orderitems = OrderItem.objects.filter(order_id=order,user=request.user)
  form = CouponCartForm(request.POST or None)
  return render(request,"cart.html",{"order":order,"orderitems":orderitems,"form":form})


# @login_required()
# def ordercomplete(request):
#   order = Order.objects.filter(user=request.user,isordered = False).first()
  
#   if order:
#     orderitems = OrderItem.objects.filter(order_id=order,user=request.user,isordered = True)
#     orderitems.delete()
  

#   return render(request,"ordercomplete.html",{"order":order})



@login_required
def removefromcart(request,product_id):
  product = get_object_or_404(Product,id = product_id)
  
  orders = Order.objects.filter(user=request.user, isordered = False)

  if orders.exists():
    order = orders[0]
    existorderitem = OrderItem.objects.filter(user=request.user,isordered=False,product_id=product,order_id=order).exists()

    if existorderitem:
      existoi = OrderItem.objects.get(user=request.user,isordered=False,product_id=product,order_id=order)

      if existoi.qty >1:
        existoi.qty -= 1
        existoi.save()
      else:
        existoi.delete()

  return redirect("cart")


@login_required
def deletefromcart(request,product_id):
  product = get_object_or_404(Product,id = product_id)
  
  orders = Order.objects.filter(user=request.user, isordered = False)

  if orders.exists():
    order = orders[0]
    existorderitem = OrderItem.objects.filter(user=request.user,isordered=False,product_id=product,order_id=order).exists()

    if existorderitem:
      existoi = OrderItem.objects.get(user=request.user,isordered=False,product_id=product,order_id=order)

      existoi.delete()

  return redirect("cart")


@login_required
def ordercomplete(request):
  
  orders = Order.objects.filter(user=request.user, isordered = False).first()

  if orders:
    orders.isordered = True
    orders.save()
   
    order_items = OrderItem.objects.filter(user= request.user,order_id=orders,isordered=False)
    for item in order_items:
      item.isordered = True
      item.save()

  return render(request,"ordercomplete.html")


@login_required()
def addCoupon(request):
  if request.method == "POST":
    code = request.POST.get("code")
    coupon  = Coupon.objects.filter(code=code)
    if coupon:
        order = Order.objects.get(user=request.user, isordered=False)
        if order.getpayableamount() > coupon[0].amount:
          order.coupon_id = coupon[0]
          order.save()
        else:
          messages.add_message(request,messages.ERROR,  message="this Coupon is not applicable in this Order Amount")
    else:
      messages.add_message(request, messages.ERROR, message="This coupon is invalid or Expired")
  return redirect(cart)             

        
@login_required()
def RemoveCoupon(request, coupon_id):
  coupon  = Coupon.objects.get(id=coupon_id)
  if coupon:
    order = Order.objects.get(user=request.user, isordered=False)
    order.coupon_id = None
    order.save()
    return redirect(cart) 
  

