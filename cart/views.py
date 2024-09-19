from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .cart import Cart
from store.models import Product
from .models import City, Province, Address, Order, OrderItem
from .forms import AddressForm


# Create your views here.


@require_POST
def add_to_cart(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product)

        json_response = {'item_count': len(cart)}
        return JsonResponse(json_response)
    except:
        return JsonResponse({'error': 'invalid request'})


def cart_detail(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'cart/cart_detail.html', context)


def update_quantity(request):
    action = request.POST.get('action')
    item_id = request.POST.get('item_id')
    cart = Cart(request)
    if action and item_id:
        try:
            product = get_object_or_404(Product, id=item_id)
            if action == 'decrease':
                cart.decrease(product)
            elif action == 'add':
                cart.add(product)
            else:
                raise ValueError('invalid action')

            context = {
                'item_count': len(cart),
                'quantity': cart.cart[str(product.id)]['quantity'],
                'total_price': cart.get_final_price(),
                'success': True,
            }
            return JsonResponse(context)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


def remove_item(request):
    product_id = request.POST.get('item_id')
    cart = Cart(request)
    try:
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        context = {
            'post_price': cart.get_post_price(),
            'final_price': cart.get_final_price(),
            'item_count': len(cart),
            'success': True,
        }
        return JsonResponse(context)
    except:
        return JsonResponse({'success': False, 'error': 'invalid request'})


# view for address


def load_cities(request):
    province_id = request.GET.get('province_id')
    cities = City.objects.filter(province_id=province_id).order_by('name')
    return JsonResponse(list(cities.values('id', 'name')), safe=False)


@login_required
def add_address(request):  # view for address and create Order
    cart = Cart(request)
    if request.method == 'POST':
        form = AddressForm(data=request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            # Create a new Order object

            order = Order.objects.create(
                buyer=request.user,
                address=address,
            )

            for item in cart:
                OrderItem.objects.create(
                    orders=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    weight=item['weight'],
                )

            # End create a new Order object

            cart.clear()
            return redirect('store:products')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'recipient_phone': request.user.phone
        }
        form = AddressForm(initial=initial)
    return render(request, 'address/address.html', {'form': form})


def order_list(request):
    user = request.user
    order = Order.objects.filter(buyer=user)
    return render(request, 'order/order_list.html', {'orders': order})


def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    if request.user != order.buyer:
        raise Http404("You do not have permission to view this order.")
    time_since_order = timezone.now() - order.created
    time_since_order = time_since_order.days
    context = {
        'order': order,
        'time_since_order': time_since_order
    }
    return render(request, 'order/order_detail.html', context=context)

