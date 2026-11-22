def cart_summary(request):
    cart = request.session.get("cart", {})
    return {"cart_count": sum(int(qty) for qty in cart.values())}
