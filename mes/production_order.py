


class ProductionOrder():
    def __init__(self, production_order: list[tuple[int, int, int, int, int]]):
        '''
        Construtor da classe ProductionOrder
        Args:
            order_id (int): id da ordem de produção
            production_order (list[tuple[int, int, int, int, int]]): lista com a ordem de produção. Cada elemento é uma tupla com a order id, client id, peça a produzir, a quantidade e a data de início
        '''
        # atributos da ordem de produção
        self.PENDING = "pending"
        self.PRODUCING = "producing"
        self.FINISHED = "finished"
        self.order_id = production_order[0]
        self.client_id = production_order[1]
        self.target_piece = production_order[2]
        self.quantity = production_order[3]
        self.start_date = production_order[4]
        self.quantity_done = 0 # assim que uma peça for concluída, incrementa-se este valor
        self.status = self.PENDING
        '''
        status possíveis:
        - pending: ordem de produção ainda não foi iniciada
        - producing: ordem de produção está sendo produzida
        - finished: ordem de produção foi concluída. Enviar status para base de dados e eliminar ordem de produção.
        '''