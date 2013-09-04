# Create your views here.
from crm.models import Product, ComputingTax
from django.http.response import HttpResponse

def get_product(request):
#     print request.POST['product_id']
    id=request.GET.get("product_id")
    product = Product.objects.get(id=int(id))
    print product.price
    print product.costprice
    print product.otherFee
    return HttpResponse(product.to_json())

def get_computingTax(request):
    id=request.GET.get("id")
    tax=ComputingTax.objects.get(id=int(id))
    print id
    print tax.expression
    return HttpResponse(tax.expression)
