from django.shortcuts import redirect,render,get_object_or_404
from .admin_forms import *
from .models import *

def admindashboard(request):
    return render (request,'admin/admin_dashboard.html')


def managecategory(request):
    form = CategoryForm(request.POST or None)
    categories = Category.objects.all()

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("managecategory")
        
    return render(request,"admin/manage_category.html",{'form':form,'category':categories})

def delete(request,id):
    data = Category.objects.get(id = id)

    data.delete()
    return redirect("managecategory")


def manageproduct(request):
    products = Product.objects.all()
    return render(request,'admin/manage_product.html',{'products':products})


def insertproduct(request):
    form = ProductForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("manageproduct")

    return render(request,"admin/insert_product.html",{'form':form})

def deleteproduct(request,id):
    data = Product.objects.get(id = id)

    data.delete()
    return redirect("manageproduct")

def editproduct(request,id):
    product = get_object_or_404(Product,id = id)

    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES,instance = product)
        if form.is_valid():
            form.save()
            return redirect("manageproduct")
    else:
        form = ProductForm(instance = product)


    return render (request,"admin/insert_product.html",{"form":form})



def manageCoupons(req):
    coupon_form = CouponForm(req.POST or None)
    coupons = Coupon.objects.all()
    
    if req.method == "POST":
        if coupon_form.is_valid():
            coupon_form.save()
            return redirect(manageCoupons)
    return render(req, "admin/manage_coupons.html", {"coupons":coupons, "form":coupon_form})



def delete_coupon(request,id):
    data = get_object_or_404(Coupon,id=id)

    data.delete()
    return redirect("manageCoupons")
