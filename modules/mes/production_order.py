from modules.communications.plc_communications import PLCCommunications
from modules.shopfloor.recipes import Recipe
from utils import bcolors



'''
Classe que representa um pedido de produção.
O pedido é consituído por:
- piece: tipo de peça a produzir
- quantity: quantidade de peças a produzir
- start_date: data de início da produção

Tem associado um estado de produção que pode ser:
- Not Started
- In Progress
- Finished
'''
class ProductionOrder(Recipe):
    def __init__(self, production_order: list, client_opcua: PLCCommunications):
        super().__init__(client_opcua)
        self.piece = production_order[0]
        self.quantity = production_order[1]
        self.start_date = production_order[2]
        self.production_status = "Not Started"



    def printProductionOrder(self):
        '''
        Função que imprime um pedido de produção

        args:
            None
        return:
            None
        '''
        print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC}: Summary of production order:')
        print(f"\tPiece type: {self.piece}")
        print(f"\tQuantity: {self.quantity}")
        print(f"\tStart Date: {self.start_date}")


    
    def generateRecipes(self, cur_n_recipes: int, max_n_recipes: int):
        '''
        Função que gera as receitas associadas a um pedido de produção

        args:
            None
        return:
            None
        '''

        pass