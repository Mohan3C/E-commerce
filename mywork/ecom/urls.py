from django.urls import path


from .views import *
from .admin_view import *

urlpatterns = [
    path("",home,name="homepage"),
    path("product/<int:id>/",viewproduct,name="viewproduct"),
    path("accounts/registration/",registeruser,name="registration"),
    path("filter/<int:cat_id>/",filter_product,name="filter"),
    path("cart/",cart,name="cart"),
    path("order/<int:product_id>/add-to-cart/",addtocart,name="addtocart"),
    path("order/<int:product_id>/remove-from-cart/",removefromcart,name="removefromcart"),
    path("order/<int:product_id>/delete-from-cart/",deletefromcart,name="deletefromcart"),
    path("order/complete/",ordercomplete,name="ordercomplete"),
    path("addCoupon/", addCoupon, name="addCoupon"),
    path("RemoveCoupon/<int:coupon_id>/", RemoveCoupon, name="RemoveCoupon"),


    # admin urls

    path("admin/dashboard/",admindashboard,name="admindashboard"),
    path("admin/category/",managecategory,name="managecategory"),
    path("admin/delete/<int:id>/",delete,name="admindelete"),
    path("admin/product/insert",insertproduct,name="insertproduct"),
    path("admin/product",manageproduct,name="manageproduct"),
    path("admin/product/<int:id>/delete",deleteproduct,name="deleteproduct"),
    path("admin/product/<int:id>/edit",editproduct,name="editproduct"),
    path("admin/coupons", manageCoupons, name="manageCoupons"),
    path("admin/coupons/<int:id>/delete/", delete_coupon, name="deletecoupon"),
]
