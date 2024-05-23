from mes import sys
from mes import traceback
from mes import groupby

from mes import Database
from mes import Clock
from mes import ProductionOrder
from mes import ExpeditionOrder
from mes import Suplier
from mes import Scheduling
from mes import PLCCommunication
from mes import generateGrahps
from mes import GenCin
from mes import Recipe
from mes import emoji, bcolors, CONSTANTS




# Número de peças para cada tipo disponíveis no armazém superior
cur_pieces_bottom_wh = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
    6: None,
    7: None,
    8: None,
    9: None
}





class Manager():
    '''
    Classe que gere as ordens de produção
    '''
    def __init__(self, client_connection, max_n_recipes: int = 12):
        self.max_n_recipes = max_n_recipes
        self.cur_n_recipes = 0

        # inicialização do cliente OPC-UA
        self.client = PLCCommunication(client_connection)

        # Conecta ao cliente OPC-UA
        try:
            self.client.clientConnect()
        except Exception as e:
            print(traceback.format_exc())
            sys.exit()

        try:
            self.verifyCodesysVerison()
        except Exception as e:
            self.client.clientDisconnect()
            sys.exit()

        # inicialização da base de dados
        try:
            self.db = Database()
        except Exception as e:
            print(traceback.format_exc())
            self.client.clientDisconnect()
            sys.exit()

        # gerar grafos e grafo simples
        self.G, self.G_simple = generateGrahps()

        self.cin = GenCin(self.client)

        self.schedule = Scheduling(self.client, self.G, self.G_simple)

        # Data
        self.clock = Clock()
        self.prev_day = -1
        self.bottom_updated = False

        # receção de encomendas do fornecedor
        self.last_supplier_order_id = 1
        self.supplier_orders = []
        self.completed_suplier_orders = []

        # guarda as ordens de produção
        self.last_prod_order_id = 1
        self.orders = []
        self.completed_orders = []

        # guarda as ordens de expedição
        self.last_exp_order_id = 1
        self.deliveries = []
        self.completed_deliveries = []

        # guarda as receitas associadas a cada ordem de produção
        self.recipes = []

        # guarda as receitas
        self.active_recipes = [None] * self.max_n_recipes # receitas que estão em produção e a circular pelo shopfloor. recipe_id != None (entre 0 e max_n_recipes-1)
        self.stashed_recipes = [] # receitas que foram geraestás das, mas por motivo de otimização encontram-se paradas nos armazéns. recipe_id = None, in_production = false, piece_in != None, end = True
        self.waiting_recipes = [] # receitas que estão à espera de serem geradas. recipe_id = None, piece_in = None
        self.terminated_recipes = [] # receitas que terminaram todas as transformações. recipe_id = None, in_production = false, piece_in = target_piece, end = True



    def verifyCodesysVerison(self):
        '''
        Função que verifica a versão do Codesys

        args:
            None
        
        return:
            None
        '''
        version = self.client.getCodesysVersion()
        if version != CONSTANTS["codesys_version_compatible"]:
            print(emoji.emojize(f'\n{bcolors.BOLD}Codesys version found:{bcolors.ENDC} {bcolors.UNDERLINE + version + bcolors.ENDC} :cross_mark:'))
            print(emoji.emojize(f':warning:  {bcolors.WARNING}This Codesys version is not compatible with this MES version - {CONSTANTS["mes_version"]}. Make sure you are running Codesys {bcolors.UNDERLINE}{CONSTANTS["codesys_version_compatible"]}{bcolors.ENDC}{bcolors.WARNING} program {bcolors.ENDC} :warning:'))
            print(f'{bcolors.FAIL}Aborting...{bcolors.ENDC}')
            raise Exception()
        else:
            print(emoji.emojize(f'\n{bcolors.BOLD}Codesys version found:{bcolors.ENDC} {bcolors.UNDERLINE + version + bcolors.ENDC} :OK_button:'))



    def groupRecipes(self):
        '''
        Função que agrupa as receitas por order id

        args:
            None
        return:
            None
        '''
        # ordenar a lista de receitas por order_id
        list_recipes_ordered = sorted(self.recipes, key=lambda x: x.order_id)
        # agrupar por order_id
        groups = groupby(list_recipes_ordered, key=lambda x: x.order_id)
        return [(order_id, list(recipes)) for order_id, recipes in groups]


    def printExpeditionOrders(self):
        '''
        Função que imprime as ordens de expedição

        args:
            None
        return:
            None
        '''
        if len(self.deliveries) == 0:
            print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} No expedition orders available!')
            return
        for delivery in self.deliveries:
            print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} Summary of expedition order {bcolors.BOLD+bcolors.UNDERLINE+str(delivery.order_id)+bcolors.ENDC+bcolors.ENDC}:')
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Client ID: {delivery.client_id}")
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Piece type: {delivery.target_piece}")
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Quantity: {delivery.quantity}")
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Expedition Date: {delivery.expedition_date}")
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Status: {delivery.status}")
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Current day: {self.clock.curr_day}")
            # print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Quantity done: {delivery.quantity_done}")



    def printProductionOrders(self):
        '''
        Função que imprime as ordens de produção

        args:
            None
        return:
            None
        '''
        if len(self.orders) == 0:
            print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} No production orders available!')
            return
        for order in self.orders:
            print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} Summary of production order {bcolors.BOLD+bcolors.UNDERLINE+str(order.order_id)+bcolors.ENDC+bcolors.ENDC}:')
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Client ID: {order.client_id}")
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Piece type: {order.target_piece}")
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Quantity: {order.quantity}")
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Start Date: {order.start_date}")
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Status: {order.status}")
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Quantity done: {order.quantity_done}")



    def printAssociatedRecipes(self):
        '''
        Função que imprime as receitas associadas a cada peça de uma ordem de produção

        args:
            None
        return:
            None
        '''
        if(len(self.recipes) == 0):
            print(emoji.emojize(f'\n{bcolors.BOLD+bcolors.WARNING}[MES]{bcolors.ENDC + bcolors.ENDC}:warning:  No recipes associated with production orders'))
            return
        recipes_grouped = self.groupRecipes()
        for order_id, recipes in recipes_grouped:
            print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} Recipes associated with production order {bcolors.BOLD+bcolors.UNDERLINE+str(order_id)+bcolors.ENDC+bcolors.ENDC}:')
            for recipe in recipes:
                print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Recipe ID: {recipe.global_id if recipe.global_id is not None else '-':<5}", end="")
                print(f"Machine ID: {recipe.machine_id if recipe.machine_id is not None else '-':<5}", end="")
                print(f"Piece In: {recipe.piece_in if recipe.piece_in is not None else '-':<5}", end="")
                print(f"Piece Out: {recipe.piece_out if recipe.piece_out is not None else '-':<5}", end="")
                print(f"Target Piece: {recipe.target_piece:<5}", end="")
                print(f"Tool: {recipe.tool if recipe.tool is not None else '-':<5}", end="")
                print(f"Time: {recipe.time if recipe.time is not None else '-':<10}", end="")
                print(f"Transformation: ({recipe.current_transformation[0] if recipe.current_transformation is not None else '-':<2},{recipe.current_transformation[1] if recipe.current_transformation is not None else '-':<2})", end="  ")
                print(f"Sended date: {str(recipe.sended_date) if recipe.sended_date is not None else '-'}", end=" -> ")
                print(f"Finished date: {recipe.finished_date if recipe.finished_date is not None else '-'}")

    

    def printRecipesStatus(self):
        '''
        Função que imprime o estado das receitas. Stashed, active, waiting e terminated    
        
        args:
            None
        return:
            None
        '''
        print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} Recipes status (ID):')
        # Determinar o número máximo de elementos em qualquer uma das listas
        active_list = [x for x in self.active_recipes if x is not None]
        active_list.sort(key=lambda x: x.global_id)
        stashed_list = sorted(self.stashed_recipes, key=lambda x: x.global_id)
        waiting_list = sorted(self.waiting_recipes, key=lambda x: x.global_id)
        terminated_list = sorted(self.terminated_recipes, key=lambda x: x.global_id)
        max_length = max(len(active_list), len(stashed_list), len(waiting_list), len(terminated_list))

        # Iterar sobre as listas simultaneamente
        print(f"\t{bcolors.UNDERLINE}Active{bcolors.ENDC}    {bcolors.UNDERLINE}Stashed{bcolors.ENDC}   {bcolors.UNDERLINE}Waiting{bcolors.ENDC}   {bcolors.UNDERLINE}Terminated{bcolors.ENDC}")
        for i in range(max_length):
            # Verificar se há elementos válidos para imprimir nesta linha
            has_elements = False
            if i < len(active_list) and active_list[i] is not None:
                has_elements = True
            if i < len(stashed_list) and stashed_list[i] is not None:
                has_elements = True
            if i < len(waiting_list) and waiting_list[i] is not None:
                has_elements = True
            if i < len(terminated_list) and terminated_list[i] is not None:
                has_elements = True
            # Se houver elementos válidos, imprima esta linha
            if has_elements:
                active_index = active_list[i].global_id if i < len(active_list) and active_list[i] is not None else ''
                stashed_index = stashed_list[i].global_id if i < len(stashed_list) else ''
                waiting_index = waiting_list[i].global_id if i < len(waiting_list) else ''
                terminated_index = terminated_list[i].global_id if i < len(terminated_list) else ''

                print(f"\t {active_index if active_index is not None else '':<10} {stashed_index if stashed_index is not None else '':<10} {waiting_index if waiting_index is not None else '':<10} {terminated_index if terminated_index is not None else '':<10}")



    def parseProductionOrder(self, production_order: list):
        '''
        Função para fazer o parse da production order recebido do erp.

        args:
            production_order (list): lista recebida do erp

        returns:
            parsed_production_order (list): lista de produção com parse
        '''
        parsed_production_order = []
        parsed_production_order.append(production_order[0]) # order id
        parsed_production_order.append(production_order[1]) # client id
        parsed_production_order.append(int(production_order[2])) # tipo de peça
        parsed_production_order.append(production_order[3]) # quantidade
        parsed_production_order.append(production_order[4]) # data de inicio
        return parsed_production_order
    


    def parseExpeditionOrder(self, expedition_order: list):
        '''
        Função para fazer o parse da expedition order recebido do erp.

        args:
            expedition_order (list): lista recebida do erp

        returns:
            parsed_expedition_order (list): lista de produção com parse
        '''
        parsed_expedition_order = []
        parsed_expedition_order.append(expedition_order[0]) # order id
        parsed_expedition_order.append(expedition_order[1]) # client id
        parsed_expedition_order.append(int(expedition_order[2])) # tipo de peça
        parsed_expedition_order.append(expedition_order[3]) # quantidade
        parsed_expedition_order.append(expedition_order[4]) # data de expedição
        return parsed_expedition_order


    
    def parseSupplierOrder(self, supplier_order: tuple):
        '''
        Função para fazer o parse da supplier order recebido do erp.

        args:
            supplier_order (tuple): lista recebida do erp

        returns:
            parsed_supplier_order (list): lista de produção com parse
        '''
        parsed_supplier_order = []
        parsed_supplier_order.append(supplier_order[0]) # supplier order id
        parsed_supplier_order.append(supplier_order[1]) # day
        parsed_supplier_order.append([int(supplier_order[2]), int(supplier_order[3])]) # quantidade de peças
        return parsed_supplier_order




    def getProductionsOrders(self):
        '''
        Função que obtém todas as ordens de produção ordenadas por quantidade de peças a produzir

        return: 
            None
        '''
        production_orders = self.db.get_production_order_by_id(self.last_prod_order_id)
        for production_order in production_orders:
            production_order = self.parseProductionOrder(production_order)
            self.orders.append(ProductionOrder(production_order))
            self.last_prod_order_id += 1



    def getExpedictionOrders(self):
        '''
        Função que obtém todas as ordens de expedição

        return:
            None
        '''
        expedition_orders = self.db.get_expedition_order_by_id(self.last_exp_order_id)
        for expedition_order in expedition_orders:
            expedition_order = self.parseExpeditionOrder(expedition_order)
            self.deliveries.append(ExpeditionOrder(expedition_order))
            self.last_exp_order_id += 1
        return



    def getSupplierOrders(self):
        '''
        Função que obtém todas as ordens de produção ordenadas por quantidade de peças a produzir

        return: 
            None
        '''
        supplier_orders = self.db.get_supply_orders_by_id(self.last_supplier_order_id)
        for supplier_order in supplier_orders:
            supplier_order = self.parseSupplierOrder(supplier_order)
            self.supplier_orders.append(Suplier(supplier_order[0], supplier_order[1], supplier_order[2]))
            self.last_supplier_order_id += 1
        return



    def getActiveRecipeIndex(self):
        '''
        Função que obtém o índice de uma receita ativa a None

        args:
            None
        return:
            int -> índice da receita ativa a None. None se não existir nenhuma receita ativa a None
        '''
        try:
            index = self.active_recipes.index(None)
        except ValueError:
            return None
        return index 



    def updateRecipesActive(self, operation: str, recipe_id: int, recipe: Recipe):
        '''
        Função que atualiza as receitas ativas. Atualiza também a receita no argumento e 
        o status da ordem de produção associada à receita para "producing".

        args:
            operation: str -> operação a realizar (add, remove). 
            add, adiciona a receita à lista e atualiza o ID da receita.
            remove, remove a receita da lista e atualiza o ID da receita.
            recipe_id: int -> ID da receita a adicionar/remover
            recipe: Recipe -> receita a adicionar/remover
        
        return:
            None
        '''
        if operation == "add" and recipe_id is not None and isinstance(recipe, Recipe):
            self.active_recipes[recipe_id] = recipe
            recipe.recipe_id = recipe_id
            # for order in self.orders:
            #     if order.order_id == recipe.order_id:
            #         order.status = order.PRODUCING
            #         break
        elif operation == "remove" and recipe_id is not None and isinstance(recipe, Recipe):
            self.active_recipes[recipe_id] = None
            recipe.recipe_id = None



    def updateRecipesStash(self, operation: str, recipe: Recipe):
        '''
        Função que atualiza o stash das receitas.

        args:
            operation: str -> operação a realizar (add, remove)
            recipe: Recipe -> receita a adicionar/remover
        return:
            None
        '''
        if operation == "add" and isinstance(recipe, Recipe):
            self.stashed_recipes.append(recipe)
        elif operation == "remove" and isinstance(recipe, Recipe):
            self.stashed_recipes.remove(recipe)



    def updateRecipesWaiting(self, operation: str, recipe: Recipe):
        '''
        Função que atualiza as receitas em espera.

        args:
            operation: str -> operação a realizar (add, remove)
            recipe: Recipe -> receita a adicionar/remover
        
        return:
            None
        '''
        if operation == "add" and isinstance(recipe, Recipe):
            self.waiting_recipes.append(recipe)
        elif operation == "remove" and isinstance(recipe, Recipe):
            self.waiting_recipes.remove(recipe)



    def updateRecipesTerminated(self, operation: str, recipe: Recipe):
        '''
        Função que atualiza as receitas terminadas.

        args:
            operation: str -> operação a realizar (add, remove)
            recipe: Recipe -> receita a adicionar/remover
        
        return:
            None
        '''
        if operation == "add" and isinstance(recipe, Recipe):
            self.terminated_recipes.append(recipe)
            for order in self.orders:
                if order.order_id == recipe.order_id:
                    order.quantity_done += 1
                    break
        elif operation == "remove" and isinstance(recipe, Recipe):
            self.terminated_recipes.remove(recipe)


    
    def generateRecipes(self):
        '''
        Função que gera as receitas para as máquinas pares ou ímpares. 
        Ordem de prioridade:
        - Receita tem ID, mas não está a sofrer nenhuma transformação e não terminou todas as transformações
        - Receita não tem ID e não está em produção

        args:
            is_even (bool): Indica se a máquina é par (True) ou ímpar (False)
        return:
            None
        '''
        try:
            free_recipe = self.active_recipes.index(None)
        except ValueError:
            return
        
        # Definir a lista de receitas a serem verificadas
        recipes_to_check = self.stashed_recipes + self.waiting_recipes

        # Verificar as receitas geradas e que não estão em produção
        if len(recipes_to_check) > 0:
            recipe_to_check = recipes_to_check[0]
            status = "stashed" if recipe_to_check in self.stashed_recipes else "waiting"
            recipe_to_check = self.schedule.schedule(self.clock, recipe_to_check, status, self.active_recipes, self.stashed_recipes)
            if not isinstance(recipe_to_check, int):
                self.updateRecipesStash("remove", recipe_to_check if status == "stashed" else None)
                self.updateRecipesWaiting("remove", recipe_to_check if status == "waiting" else None)
                self.updateRecipesActive("add", free_recipe, recipe_to_check)
                self.client.sendRecipe(self.active_recipes[free_recipe])
                self.printAssociatedRecipes()
                self.printRecipesStatus()
                


    def generateSingleRecipe(self, recipe: Recipe):
        '''
        Função que gera uma receita

        args:
            recipe: Recipe -> receita a gerar
            is_even (bool): Indica se a máquina é par (True) ou ímpar (False)
        return:
            recipe: Recipe -> receita gerada
            -1: Não foi possível gerar a receita
        '''
        schedule = self.schedule.schedule(self.clock, recipe, "active", self.active_recipes, self.stashed_recipes) # tentar primeiro máquinas pares
        if isinstance(schedule, int):
            return -1
        return schedule



    def checkOrderComplete(self, recipe: Recipe):
        '''
        Função que verifica se a ordem de produção está completa com base na receita. Se sim, atualiza o estado da ordem de produção
        na base de dados e remove a ordem de produção da lista de ordens de produção. Adiciona a ordem de produção à lista de ordens completas.
        Atualiza o número de peça produzidas para um determinado cliente.

        args:
            recipe: Recipe -> receita a verificar
        return:
            None
        '''
        for order in self.orders:
            if order.order_id == recipe.order_id:
                if order.quantity_done == order.quantity:
                    order.status = order.FINISHED
                    print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} Updating status of Production Order {bcolors.UNDERLINE}{order.order_id}{bcolors.ENDC} in database...', end=" ", flush=True)
                    if self.db.insert_production_status(order.order_id, self.clock.curr_day):
                        # correu tudo ok. Remover ordem de produção da lista de ordens de produção e adicionar à lista de ordens completas
                        self.completed_orders.append(order)
                        self.orders.remove(order)
                        print(emoji.emojize(f'{bcolors.OKGREEN}ok{bcolors.ENDC}'))
                    else:
                        print(emoji.emojize(f'{bcolors.FAIL}fail{bcolors.ENDC}'))
                    break
                    
        return



    def waitSomeTransformation(self):
        '''
        Função que aguarda o fim de alguma transformação. Se não existir nenhuma receita ativa, vai continuamente tentar
        gerar receitas com base naquelas que se encontram em stash ou waiting. Assim que seja gerada uma receita,
        além de colocar a receita em produção, vai estar a tentar gerar novas receitas, não ultrapassando o máximo
        de receitas ativas permitido.

        args:
            None
        return:
            None
        '''
        for recipe in self.active_recipes:
            if recipe is not None: # receita válida
                self.client.getRecipeState(recipe) # obter o estado da receita
                if recipe.end and recipe.piece_out == recipe.target_piece and recipe.piece_in != recipe.piece_out and recipe.machine_id != -1 and recipe.machine_id != -2: # enviar receita para armazém inferior
                    recipe.machine_id = -1
                    recipe.piece_in = recipe.piece_out
                    recipe.end = False
                    self.client.sendRecipe(recipe)
                elif recipe.end and recipe.piece_out == recipe.target_piece and recipe.piece_in == recipe.target_piece: # receita terminou todas as transformações
                    recipe.finished_date = self.clock.get_time()
                    self.updateRecipesActive("remove", recipe.recipe_id, recipe)
                    self.updateRecipesTerminated("add", recipe)
                    self.checkOrderComplete(recipe)
                    # self.printRecipesStatus()
                elif recipe.end and recipe.piece_in != recipe.target_piece and recipe.machine_id == -2: # receita terminou transformação intermédia e foi enviada para armazém superior
                    recipe.finished_date = self.clock.get_time()
                    self.updateRecipesActive("remove", recipe.recipe_id, recipe)
                    self.updateRecipesStash("add", recipe)
                    # self.printRecipesStatus()
                elif recipe.end and recipe.piece_out != recipe.target_piece: # receita terminou transformação intermédia
                    recipe.finished_date = self.clock.get_time()
                    result = self.generateSingleRecipe(recipe)
                    if result == -1: # não foi possível gerar a receita
                        recipe.machine_id = -2 # enviar para armazém superior
                        self.client.sendRecipe(recipe)
                    else:
                        recipe = result
                        self.printAssociatedRecipes()
                        self.client.sendRecipe(recipe)
        # self.generateRecipes()
        return
        


    def waitCompleteProductionOrder(self):
        '''
        Função que verifica e faz o envio se a ordem de produção estiver completa

        args:
            None
        return:
            None
        '''
        if len(self.completed_orders) > 0: # uma ordem de produção terminou
            # atualizar estado da ordem de produção na base de dados
            print()

        
        if len(self.completed_orders) > 0: # uma ordem de produção terminou
            ## OLHAR PARA A DATA DE ENTREGA ###########################################################################################################
            ################################################################################################################
            if self.completed_orders[0].status != self.completed_orders[0].SENDING:
                self.completed_orders[0].status = self.completed_orders[0].SENDING
                # enviar order
                print(emoji.emojize(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} :delivery_truck:  Sending order {bcolors.UNDERLINE}{self.completed_orders[0].order_id}{bcolors.ENDC}... :delivery_truck:'))
                self.client.sendDelivery(self.completed_orders[0])
            else:
                status_delivery = self.client.getDeliveryState(self.completed_orders[0])
                if status_delivery:
                    print(emoji.emojize(f'\n{bcolors.BOLD+bcolors.OKGREEN}[MES]{bcolors.ENDC + bcolors.ENDC} :grinning_face_with_big_eyes:  Order {bcolors.UNDERLINE}{self.completed_orders[0].order_id}{bcolors.ENDC} delivered successfully at {self.clock.get_time_pretty()}! :check_mark_button:'))
                    # remover receitas associadas a esta ordem de produção
                    for recipe in self.recipes:
                        if recipe.order_id == self.completed_orders[0].order_id:
                            self.updateRecipesTerminated("remove", recipe)
                            self.recipes.remove(recipe)
                    # remover ordem de produção
                    self.orders.remove(self.completed_orders[0])
                    # remover ordem de produção da lista de ordens completas
                    self.completed_orders.pop(0)
                    # self.printProductionOrders()
        return
          


    def waitCompleteExpeditonOrder(self):
        '''
        Função que verifica e faz o envio se a ordem de expedição estiver completa

        args:
            None
        return:
            None
        '''
        if self.deliveries[0].status == self.deliveries[0].SENDING:
            status_delivery = self.client.getDeliveryState(self.deliveries[0])
            print("Print Status delivery: ", status_delivery)
            if status_delivery:
                print(emoji.emojize(f'\n{bcolors.BOLD+bcolors.OKGREEN}[MES]{bcolors.ENDC + bcolors.ENDC} :grinning_face_with_big_eyes:  Order {bcolors.UNDERLINE}{self.deliveries[0].order_id}{bcolors.ENDC} delivered successfully at {self.clock.get_time_pretty()}! :check_mark_button:'))
                # # remover receitas associadas a esta ordem de produção
                for recipe in self.recipes:
                    if recipe.order_id == self.deliveries[0].order_id:
                        self.updateRecipesTerminated("remove", recipe)
                        self.recipes.remove(recipe)
                # atualizar base de dados sobre estado da expedicão
                self.db.expedition_production_status(self.deliveries[0].order_id, self.clock.curr_day)
                # remover ordem de expedição e adicionar à lista de ordens completas
                self.completed_deliveries.append(self.deliveries[0])
                self.deliveries.pop(0)
                return

        # verificar se dia de expedição corresponde ao atual
        if self.deliveries[0].expedition_date > self.clock.curr_day:
            return
        # verificar se número de peças da ordem de expedição existe no armazém
        self.updatePiecesBottomWh()
        if cur_pieces_bottom_wh[self.deliveries[0].target_piece] != self.deliveries[0].quantity:
            return
        print("entrei")
        # verificar expedições do dia
        if self.deliveries[0].status == self.deliveries[0].PENDING: # enviar ordem de expedição
            self.deliveries[0].status = self.deliveries[0].SENDING
            # enviar order
            print(emoji.emojize(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} :delivery_truck:  Sending order {bcolors.UNDERLINE}{self.deliveries[0].order_id}{bcolors.ENDC}... :delivery_truck:'))
            self.client.sendDelivery(self.deliveries[0])



    def waitCompleteSupplierOrder(self):
        '''
        Função que verifica se existe alguma encomenda do fornecedor e realiza a receção da mesma

        args:
            None
        
        return:
            None
        '''
        if len(self.supplier_orders) > 0:
            # receção de encomenda do fornecedor
            self.cin.spawnPieces(self.supplier_orders[0].num_pieces)
            self.completed_suplier_orders.append(self.supplier_orders[0])
            self.supplier_orders.pop(0)



    def updatePiecesBottomWh(self):
        '''
        Função para verificar a existência de peças no armazém superior.
        Args:
            client (PLCCommunication): objecto cliente OPC-UA

        Return:
            None
        '''
        for i, piece in enumerate(cur_pieces_bottom_wh):
            cur_pieces_bottom_wh[piece] = self.client.getPieceBottomWH(i+1) # As peças não têm tipo 0, mas sim de 1 a 9



    def dailyUpdateFromDB(self):
        '''
        Função que obtém as ordens de produção e expedição da base de dados
        ao início de cada dia. Durante os segundos 2 e 5 de cada dia, vai
        requisitar à base de dados novas informações a cada segundo.

        args:
            None
        return:
            None
        '''
        # entre os segundos 2 e 5 de cada dia, requisitar à base de dados a cada segundo
        print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} Day: {self.clock.curr_day}')
        self.getProductionsOrders()
        self.getExpedictionOrders()
        self.getSupplierOrders()
        self.cleanLists()
        
        # verificar produções do dia
        for order in self.orders:
            if order.start_date == self.clock.curr_day and order.status == order.PENDING:
                order.status = order.PRODUCING # passa a estado de produção e gera receitas
                krecipes = len(self.recipes)
                for i in range(order.quantity):
                    recipe_index = krecipes + i
                    self.recipes.append(Recipe(order.order_id, recipe_index, order.target_piece))
                    self.updateRecipesWaiting("add", self.recipes[-1]) # adicionadas à fila de espera. Serão enviadas para produção assim que possível
            
            self.printProductionOrders()
            self.printExpeditionOrders()
            self.printAssociatedRecipes()
            self.printRecipesStatus()
        return



    def cleanLists(self):
        '''
        Função que limpa as listas de ordens de produção, expedição e fornecedor completadas.

        args:
            None
        
        return:
            None
        '''
        self.completed_orders.clear()
        self.completed_deliveries.clear()
        self.completed_suplier_orders.clear()



    def handle_exit(self, error_message=None):
        self.printAssociatedRecipes()
        self.printRecipesStatus()
        self.printProductionOrders()
        if error_message:
            print(error_message)
        print(emoji.emojize(f'\n{bcolors.BOLD+bcolors.WARNING}[MES]{bcolors.ENDC + bcolors.ENDC} :warning:  Closing MES... :warning:'))



    def stateMachine(self):
        '''
        Máquina de estados 
        '''
        # atualização da base de dados no final do dia para o stock de peças no armazém inferior
        if ((self.clock.curr_time_seconds >= 55) and
            (self.clock.curr_time_seconds <= 59) and
            (not self.bottom_updated)):
            self.updatePiecesBottomWh()
            self.db.insert_bottom_stock(self.clock.curr_day, cur_pieces_bottom_wh)
            self.bottom_updated = True
        # atualização da base de dados para o novo dia
        if ((self.clock.curr_time_seconds >= 3) and
            (self.clock.curr_time_seconds <= 5) and
            (self.prev_day != self.clock.curr_day)):
            self.dailyUpdateFromDB()
            self.prev_day = self.clock.curr_day
            self.bottom_updated = False
        if isinstance(self.active_recipes.index(None), int):
            self.generateRecipes()
        # verifica se existem encomendas do fornecedor
        if len(self.supplier_orders) > 0:
            self.waitCompleteSupplierOrder()
        # verifica se existem receitas ativas
        if any(self.active_recipes):
            self.waitSomeTransformation()
        # verifica se existem expedições
        if len(self.deliveries) > 0:
            self.waitCompleteExpeditonOrder()



    def spin(self):
        '''
        Função que faz o lançamento das máquinas de estados de cada ordem de produção
        '''
        while True:
            try:
                self.stateMachine()
                self.clock.update_time()
            except KeyboardInterrupt:
                self.handle_exit()
                self.client.clientDisconnect()
                self.db.disconnect()
                sys.exit()
            except Exception as e:
                self.handle_exit(traceback.format_exc())
                self.client.clientDisconnect()
                self.db.disconnect()
                sys.exit()
            # finally:
            #     self.client.clientDisconnect()
            #     break