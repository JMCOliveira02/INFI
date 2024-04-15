import csv

class Order:
    def __init__(self, id, number, quantity, dueDate, latePen, earlyPen, clientId, workpiece,):
        self.id = id
        self.number = number
        self.workpiece = workpiece
        self.quantity = quantity
        self.dueDate = dueDate
        self.latePen = latePen
        self.earlyPen = earlyPen
        self.clientId = clientId

def parseOrderCSV(order_csv):
        for row in order_csv:
            order = Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            #print(order.id, order.number, order.workpiece, order.quantity, order.dueDate, order.latePen, order.earlyPen, order.clientId)
        return order