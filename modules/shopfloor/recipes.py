import modules.communications.plc_communications as PLCCommunications


'''
Class responsável por representar uma receita de produção. Assim como
enviá-las para o PLC
'''
class Recipe():
    def __init__(self, client: PLCCommunications):
        self.client = client
        self.recipe_id = None
        self.machine_id = None
        self.piece_in = None
        self.tool = None
        self.time = None

    

    def sendRecipe(self):
        '''
        Função que envia a receita para o PLC

        args:
            None
        return:
            None
        '''
        self.client.sendRecipe(self)

    