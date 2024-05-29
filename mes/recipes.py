'''
Class responsável por representar uma receita de produção. Assim como
enviá-las para o PLC
'''
class Recipe():
    def __init__(self, order_id: int, global_id: int, target_piece: int):
        self.order_id = order_id
        self.global_id = global_id # id único da receita
        self.recipe_id = None # o manager atribui um id único a cada receita. Se None, significa que a receita ainda não foi lançada para o shopfloor nem foi considerada para escalonamento
        self.machine_id = None # preenchido pelo escalonamento
        self.piece_in = None # preeenchido pelo escalonamento
        self.piece_out = None # preenchido pelo escalonamento
        self.target_piece = target_piece # peça a produzir
        self.tool = None # preenchido pelo escalonamento
        self.time = None # preenchido pelo escalonamento
        self.inactive = False # se True, PLC não conclui transformação devido a máquina ficar inativa
        self.end = False # indica se a receita foi terminada pelo PLC
        self.current_transformation = None # indica a transformação atual. Por exemplo, para uma target_piece=3, a primeira transformação é 1->2, a segunda 2->3. Preenchido pelo escalonamento
        #self.in_production = False # indica se a receita está em produção, ou seja, que foi lançada para o shopfloor
        self.sended_date = None
        self.finished_date = None
        # self.current_date = None
        # self.tolerance = 0 # tolerância após verificar estado da receita no PLC tendo passado o tempo de transformação. 
                           # Se a receita não estiver terminada, é necessário esperar mais tempo, ou seja, tolerência aumenta