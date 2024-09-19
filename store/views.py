from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import *
from .forms import SearchForm
from .models import ProductFeatures


# Create your views here.


class ProductList(ListView):
    model = Product
    template_name = 'store/list.html'
    context_object_name = 'products'


def post_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    product_feature = ProductFeatures.objects.filter(features=product)
    if FavoriteProduct.objects.filter(product=product):
        saved = True
    else:
        saved = False
    return render(request, 'store/post_detail.html', {'product': product, 'saved': saved,
                                                      'features': product_feature})


# Favorite products views
def add_to_favorite(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    saved = None

    favorite = FavoriteProduct.objects.filter(user=request.user, product=product).first()

    if favorite:
        saved = False
        favorite.delete()
    else:
        saved = True
        FavoriteProduct.objects.create(product=product, user=request.user)

    return JsonResponse({'saved': saved, 'success': True})


def favorite_products(request):
    user = request.user
    products = FavoriteProduct.objects.filter(user=user)
    return render(request, 'favorite/favorite_products.html', {'products': products})


@login_required
def remove_favorite(request, id, slug):
    if request.method == 'POST':
        FavoriteProduct.objects.filter(user=request.user, product_id=id, product__slug=slug).delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def contact_us(request):
    return render(request, 'contact_us/contact_us.html')


# product Search
def product_search(request):
    if 'query' in request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']

            first_result = Product.objects.annotate(similarity=TrigramSimilarity('name', query)).filter(
                similarity__gt=0.1
            )
            second_result = Product.objects.annotate(similarity=TrigramSimilarity('description', query)).filter(
                similarity__gt=0.1
            )

            main_result = (first_result | second_result).order_by('-similarity')

            context = {
                'query': query,
                'result': main_result,
            }
            return render(request, 'search/search.html', context)

