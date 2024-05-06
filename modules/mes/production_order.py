


class ProductionOrder():
    def __init__(self, order_id: int, production_order: list[tuple[int, int, str]]):
        # atributos da ordem de produção
        self.order_id = order_id
        self.target_piece = production_order[0]
        self.quantity = production_order[1]
        self.start_date = production_order[2]
        self.quantity_done = 0 # assim que uma peça for concluída, incrementa-se este valor