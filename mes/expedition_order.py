




class ExpeditionOrder():
    def __init__(self, expedition_order: list[tuple[int, int, int, int, int]]):
        '''
        Construtor da classe ExpeditionOrder

        args:
            expedition_order (list[tuple[int, int, int, int, int]]): lista com a ordem de expedição. 
            Cada elemento é uma tupla com a order id, client id, peça a expedir, a quantidade e a data de expedição
        '''
        # atributos da expedition order
        self.PENDING = "pending"
        self.SENDING = "sending"
        self.DONE = "done"
        self.order_id = expedition_order[0]
        self.client_id = expedition_order[1]
        self.target_piece = expedition_order[2]
        self.quantity = expedition_order[3]
        self.expedition_date = expedition_order[4]
        self.status = self.PENDING
        '''
        - producing: ordem de expedição está sendo produzida
        - finished: ordem de expedição foi concluída. Esperar pela data de entrega
        - sending: ordem de expedição está sendo enviada para cliente
        - done: ordem de expedição foi concluída. Enviar status para base de dados e eliminar ordem de expedição
        '''
