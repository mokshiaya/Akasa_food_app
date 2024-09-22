# akasa/views.py
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, UserLoginForm  
from django.contrib.auth.decorators import login_required  
from .models import CartItem, Order, Item
import uuid
from django.http import HttpResponseRedirect
from django.contrib import messages

# Login view
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home after login
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


# Register view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

def browse_items(request, category=None):
    search_query = request.GET.get('category', None)

    if search_query:
        items = Item.objects.filter(category__icontains=search_query)
    elif category == "all" or category is None:
        items = Item.objects.all()
    else:
        items = Item.objects.filter(category=category)

    categories = ['All', 'Fruits', 'Vegetables', 'Non-veg', 'Breads']  
    return render(request, 'browse_items.html', {
        'items': items,
        'categories': categories,
        'selected_category': category,
        'search_query': search_query
    })






@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if item.stock <= 0:
        messages.error(request, f"{item.name} is out of stock.")
        return redirect('browse_items')
    
    # Check if CartItem already exists for this user and item
    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()

    return redirect('browse_items')

@login_required
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(user=request.user, item__id=item_id)
        cart_item.delete()  # Remove the item from the cart
        messages.success(request, f"{cart_item.item.name} has been removed from your cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")

    return redirect('view_cart')  # Redirect to the cart page

# @login_required
# def add_to_cart(request, item_id):
#     item = get_object_or_404(Item, id=item_id)

#     if item.stock <= 0:
#         messages.error(request, f"{item.name} is out of stock.")
#         return redirect('browse_items') 
    
#     cart_items = request.session.get('cart', [])
    
#     if not any(cart_item['id'] == item.id for cart_item in cart_items):
#         cart_items.append({'id': item.id, 'quantity': 1}) 
#     else:
#         for cart_item in cart_items:
#             if cart_item['id'] == item.id:
#                 cart_item['quantity'] += 1 
#                 break
    
#     request.session['cart'] = cart_items  
    
#     return redirect(request.META.get('HTTP_REFERER', '/')) 
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = 0
    for cart_item in cart_items:
        subtotal = cart_item.item.price * cart_item.quantity
        cart_item.subtotal = subtotal 
        total_amount += subtotal

    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_amount': total_amount})


# @login_required
# def view_cart(request):
#     cart_items = request.session.get('cart', [])
#     total_amount = 0
#     for cart_item in cart_items:
#         item = Item.objects.get(id=cart_item['id'])  # Get item from the database
#         subtotal = item.price * cart_item['quantity']
#         cart_item['subtotal'] = subtotal
#         total_amount += subtotal

#     return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_amount': total_amount})


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    print(f"Cart items for user {request.user.username}: {list(cart_items)}")  # Debugging
    
    # Check if the cart is empty
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')
    
    total_amount = 0
    for cart_item in cart_items:
        total_amount += cart_item.item.price * cart_item.quantity

    order_id = str(uuid.uuid4())[:8]
    
    try:
        order = Order.objects.create(
            user=request.user,
            order_id=order_id,
            total_amount=total_amount
        )
    except Exception as e:
        messages.error(request, "There was an error creating your order.")
        print(f"Order creation error: {e}")
        return redirect('view_cart')

    for cart_item in cart_items:
        item = cart_item.item
        item.stock -= cart_item.quantity  # Update stock
        item.save()  # Save updated stock
        order.items.add(cart_item)  # Link CartItem to Order

    cart_items.delete()  # Clear cart after checkout
    return render(request, 'checkout_success.html', {'order_id': order_id, 'total_amount': total_amount})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_details = []

    for order in orders:
        total_items = sum(cart_item.quantity for cart_item in order.items.all())
        order_items = order.items.all()  
        print(f"Order ID: {order.order_id}, Total Items: {total_items}")

        order_details.append({
            'order': order,
            'total_items': total_items,
            'order_items': order_items  
        })
    
    return render(request, 'order_history.html', {'order_details': order_details})

# @login_required
# def order_history(request):
#     orders = Order.objects.filter(user=request.user).order_by('-created_at')
#     order_details = []

#     for order in orders:
#         total_items = sum(cart_item.quantity for cart_item in order.items.all())
#         order_items = order.items.all()  
#         print(f"Order ID: {order.order_id}, Total Items: {total_items}")

#         order_details.append({
#             'order': order,
#             'total_items': total_items,
#             'order_items': order_items  
#         })
    
#     return render(request, 'order_history.html', {'order_details': order_details})
