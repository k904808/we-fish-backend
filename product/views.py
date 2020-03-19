import json

from order.models import Order
from .models      import (
    Category,
    Theme,
    Review,
    Product,
    ThemeProduct,
    Section
)

from django.views import View
from django.http  import HttpResponse, JsonResponse

class CategoryView(View):
    def get(self, request):
        category_data = Category.objects.filter(is_real_category=True).values()

        return JsonResponse({'category_list' : list(category_data)}, status = 200)

class ReviewView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            order_number = request.GET['order_number']
            order        = Order.objects.get(order_number = order_number)

            Review(
                product_id = data['product_id'],
                user_id    = data['user_id'],
                order_id   = order,
                rate       = data['rate'],
                content    = data['content'],
                image_url  = data['image_url']
            ).save()

            return HttpResponse(status = 200)
        except Order.DoesNotExist:
            return JsonResponse({"message":"INVALID_KEY"}, status = 404)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

    def get(self, request, product_id):
        data = Review.objects.all()

        return JsonResponse({"review":list(data)}, status = 200)

class DetailView(View):
    def get(self, request, product_id):
        try:
            return JsonResponse({'product' : Product.objects.get(id=product_id).values()}, status = 200)
        except Order.DoesNotExist:
            return HttpResponse(status = 404)

class ProductListView(View):
    def get(self, request):
        category_id  = request.GET.get('category_id', None)
        order_by     = request.GET.get('order_by', 'price')
        product_data = Product.objects.prefetch_related('category').filter(category__id = category_id).order_by(order_by)
        product_list = [{
            'id'    : product.id,
            'image' : product.image_url,
            'name'  : product.name,
            'price' : product.price
        } for product in product_data]

        return JsonResponse({"data" : product_list}, status = 200)

class SearchView(View):
    def get(self, request, keyword):
        search_data = Product.objects.filter(name__icontains=search).values('id', 'name', 'price', 'image_url')
        return JsonResponse({"search_results":list(search_data)}, status = 200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEY"}, status = 400)

class HoneyView(View):
    def get(self, request):
        section_id = request.GET.get('section_id', None)
        section    = Section.objects.get(id = section_id)
        honey_view = {
            'id'     : section.id,
            'name'   : section.name,
            'theme' : [{
                'id'        : theme.id,
                'name'      : theme.name,
                'tagline'   : theme.tagline,
                'image_url' : theme.image_url,
                'start_at'  : theme.start_at,
                'end_at'    : theme.end_at,
                'product'   : [{
                    'id'        : product.product.id,
                    'name'      : product.product.name,
                    'price'     : product.product.price,
                    'image_url' : product.product.image_url
                } for product in ThemeProduct.objects.select_related('product', 'theme').filter(theme__id = theme.id)]
            } for theme in Theme.objects.filter(section_id = section.id)]}

        return JsonResponse({"section_data" : honey_view}, status = 200)
