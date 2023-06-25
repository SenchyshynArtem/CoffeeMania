from basket.models import ProductInBasket
from ordering.views import is_user_registered


def product_count(request):
    session_key = request.session.session_key
    if is_user_registered(session_key):
        user = is_user_registered(session_key)
        products_in_basket = len(ProductInBasket.objects.filter(user=user))
    else: 
        products_in_basket = len(ProductInBasket.objects.filter(session_key=session_key))
    return {'product_count': products_in_basket}