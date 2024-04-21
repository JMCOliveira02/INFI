import csv

'''
Classe que representa um pedido
'''
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
    '''
    Função que lê um ficheiro csv com os pedidos e devolve uma lista de objetos Order

    args:
        order_csv: ficheiro csv com os pedidos
    '''
    for row in order_csv:
        order = Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        #print(order.id, order.number, order.workpiece, order.quantity, order.dueDate, order.latePen, order.earlyPen, order.clientId)
    return order


def printOrder(order):
    '''
    Função que imprime um pedido

    args:
        order: objeto Order
    '''
    print('---------------------------------')
    print(f"Order ID: {order.id}")
    print(f"Order Number: {order.number}")
    print(f"Workpiece: {order.workpiece}")
    print(f"Quantity: {order.quantity}")
    print(f"Due Date: {order.dueDate}")
    print(f"Late Penalty: {order.latePen}")
    print(f"Early Penalty: {order.earlyPen}")
    print(f"Client ID: {order.clientId}")
    print("\n")