from abc import ABC, abstractmethod
from collections import namedtuple
Customer = namedtuple("Customer", "name, fidelity")
class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
    def total(self):
        return self.price * self.quantity


class Order:  # 上下文
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion
    
    def total(self):
        if not hasattr(self, "__total"):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total
    
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount
    
    def __repr__(self):
        fmt = "<Order total: {:.2f} due: {:.2f}>"
        return fmt.format(self.total(), self.due())


class Promotion(ABC):
    @abstractmethod
    def discount(self, order):
        pass


class BulkItemPromo(Promotion):
    """单个商品为20个或以上时提供10%折扣"""
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * 0.1
        return discount


class FideliltPromo(Promotion):
    """为积分1000以上的提供5%折扣"""
    def discount(self, order):
        return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0


class LargeOrderPromo(Promotion):
    """订单中的不同商品达到10个或以上，享受7%折扣"""
    def discount(self, order):
        discount_item = {item.product for item in order.cart}
        if len(discount_item) >= 10:
            return order.total() * 0.07
        return 0


def main():
    joe = Customer("john", 0)
    ann = Customer("ann", 1000)
    cart = [LineItem("apple", 4, .5), LineItem("a1", 10, 1.5), LineItem("a3", 5, 5.0)]
    print(Order(joe, cart, FideliltPromo()))
    print(Order(ann, cart, FideliltPromo()))


if __name__ == "__main__":
    main()

# https://jamal-jiang.github.io/2018/02/18/Python%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F-%E7%AD%96%E7%95%A5%E6%A8%A1%E5%BC%8F/