class Order(object):
    def __init__(self, OrderID, OrderNumber, DateOrdered, CustomerName, CustomerAddress):
        self.OrderID = OrderID
        self.OrderNumber = OrderNumber
        self.DateOrdered = DateOrdered  
        self.CustomerName = CustomerName
        self.CustomerAddress = CustomerAddress