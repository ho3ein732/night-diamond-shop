from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import get_object_or_404, redirect, render
from account.models import NightDimondUser
from store.models import Product
from .forms import ReturnItemForm, ReturnImageFormset, ReturnImage
from .models import ReturnedItem


# create return item
@login_required
def create_returned_item(request, user_id, product_id):
    user = get_object_or_404(NightDimondUser, id=user_id)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        returned_item_form = ReturnItemForm(request.POST)
        formset = ReturnImageFormset(request.POST, request.FILES, queryset=ReturnImage.objects.none())
        if returned_item_form.is_valid() and formset.is_valid():
            returned_item = returned_item_form.save(commit=False)
            returned_item.user = user
            returned_item.product = product
            returned_item.save()
            for form in formset:
                return_image = form.save(commit=False)
                return_image.return_item = returned_item
                return_image.save()
            return redirect('store:products')
    else:
        returned_item_form = ReturnItemForm()
        formset = ReturnImageFormset(queryset=ReturnImage.objects.none())
    context = {'formset': formset, 'returned_item_form': returned_item_form}
    return render(request, 'returnitem/return_item.html', context)


# list return items
@login_required
def list_returned_goods(request):
    goods = ReturnedItem.objects.filter(user=request.user)
    return render(request, 'returnitem/list_goods.html', {'goods': goods})


# detail return items
@login_required
def details_returned_goods(request, item_id):
    item = ReturnedItem.objects.get(id=item_id)
    return render(request, 'returnitem/detail.html', {'item': item})
