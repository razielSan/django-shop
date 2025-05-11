from shop.models import Product, OrderProduct, Order, Customer


class CartForAuthenticatedUser:
    """ " Логика Корзины"""

    def __init__(self, request, product_id=None, action=None):
        self.user = request.user
        if product_id and action:
            self.add_or_delete(product_id, action)

    def get_cart_info(self):
        """Получение информации о корзине"""
        customer, created = Customer.objects.get_or_create(user=self.user)
        order, created = Order.objects.get_or_create(customer=customer)
        order_products = order.ordered.all()
        cart_total_quantity = order.get_cart_total_quantity
        cart_total_price = order.get_cart_total_price

        return {
            "order": order,
            "order_products": order_products,
            "cart_total_quantity": cart_total_quantity,
            "cart_total_price": cart_total_price,
        }
