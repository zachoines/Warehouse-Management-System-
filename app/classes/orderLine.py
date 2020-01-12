class OrderLine(object):
    def __init__(self, OrderLineID, OrderID, ProductID, QTY):
        self.OrderLineID = OrderLineID
        self.OrderID = OrderID
        self.ProductID = ProductID
        self.QTY = QTY