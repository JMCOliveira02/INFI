import sys
import traceback
import datetime
import time
from itertools import groupby
import threading

from modules.communications.plc_communications import PLCCommunications
from modules.communications.database import Database
from modules.mes.production_order import ProductionOrder
from modules.mes.scheduling import Scheduling
from modules.mes.transformations import generateGrahps
from modules.shopfloor.gen_cin import GenCin
from modules.shopfloor.recipes import Recipe
from utils import *



class Manager():
    '''
    Classe que gere as ordens de produção
    '''
    def __init__(self, client_connection, max_n_recipes: int = 12):
        self.max_n_recipes = max_n_recipes
        self.cur_n_recipes = 0

        # inicialização do cliente OPC-UA
        self.client = PLCCommunications(client_connection)

        # Conecta ao cliente OPC-UA
        try:
            self.client.clientConnect()
        except Exception as e:
            print(traceback.format_exc())
            sys.exit()

        # gerar grafos e grafo simples
        self.G, self.G_simple = generateGrahps()

        self.cin = GenCin(self.client)

        self.schedule = Scheduling(self.client, self.G, self.G_simple)
        
        # self.database = database

        # guarda as ordens de produção
        self.orders = []

        # guarda as receitas associadas a cada ordem de produção
        self.recipes = []

        # guarda as receitas
        self.active_recipes = [None] * self.max_n_recipes # receitas que estão em produção e a circular pelo shopfloor. recipe_id != None (entre 0 e max_n_recipes-1)
        self.stashed_recipes = [] # receitas que foram geradas, mas por motivo de otimização encontram-se paradas nos armazéns. recipe_id = None, in_production = false, piece_in != None, end = True
        self.waiting_recipes = [] # receitas que estão à espera de serem geradas. recipe_id = None, piece_in = None
        self.terminated_recipes = [] # receitas que terminaram todas as transformações. recipe_id = None, in_production = false, piece_in = target_piece, end = True

        self.stop_cin_thread = False
        self.stop_orders_thread = False
        self.stop_recipes_thread = False

        self.state = 0
        self.new_state = 0
        self.got_orders = False
        self.order_finished = False
        self.recipes_generated = False
        self.some_recipe_finished = False



    def disconnect(self):
        '''
        Função para desconectar o cliente OPC-UA

        args:
            None
        return:
            None
        '''
        self.client.clientDisconnect()



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



    def printProductionOrders(self):
        '''
        Função que imprime as ordens de produção

        args:
            None
        return:
            None
        '''
        for order in self.orders:
            print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} Summary of production order {bcolors.BOLD+bcolors.UNDERLINE+str(order.order_id)+bcolors.ENDC+bcolors.ENDC}:')
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Piece type: {order.target_piece}")
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Quantity: {order.quantity}")
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Start Date: {order.start_date}")



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
                print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Recipe ID: {recipe.global_id if recipe.global_id is not None else 'None':<10}", end="")
                print(f"Machine ID: {recipe.machine_id if recipe.machine_id is not None else 'None':<10}", end="")
                print(f"Piece In: {recipe.piece_in if recipe.piece_in is not None else 'None':<10}", end="")
                print(f"Piece Out: {recipe.piece_out if recipe.piece_out is not None else 'None':<10}", end="")
                print(f"Target Piece: {recipe.target_piece:<10}", end="")
                print(f"Tool: {recipe.tool if recipe.tool is not None else 'None':<10}", end="")
                print(f"Time: {recipe.time if recipe.time is not None else 'None':<10}", end="")
                print(f"Transformation: ({recipe.current_transformation[0] if recipe.current_transformation is not None else '-':<2},{recipe.current_transformation[1] if recipe.current_transformation is not None else '-':<2})", end="  ")
                print(f"Sended date: {str(recipe.sended_date) if recipe.sended_date is not None else 'None'}", end=" -> ")
                print(f"Finished date: {str(recipe.finished_date) if recipe.finished_date is not None else 'None'}")
                # print(f"Producing: {str(recipe.in_production):<10}")

    

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
        max_length = max(len(active_list), len(self.stashed_recipes), len(self.waiting_recipes), len(self.terminated_recipes))

        # Iterar sobre as listas simultaneamente
        print(f"\t{bcolors.UNDERLINE}Active{bcolors.ENDC}    {bcolors.UNDERLINE}Stashed{bcolors.ENDC}   {bcolors.UNDERLINE}Waiting{bcolors.ENDC}   {bcolors.UNDERLINE}Terminated{bcolors.ENDC}")
        for i in range(max_length):
            # Verificar se há elementos válidos para imprimir nesta linha
            has_elements = False
            if i < len(active_list) and active_list[i] is not None:
                has_elements = True
            if i < len(self.stashed_recipes) and self.stashed_recipes[i] is not None:
                has_elements = True
            if i < len(self.waiting_recipes) and self.waiting_recipes[i] is not None:
                has_elements = True
            if i < len(self.terminated_recipes) and self.terminated_recipes[i] is not None:
                has_elements = True
            # Se houver elementos válidos, imprima esta linha
            if has_elements:
                active_index = active_list[i].global_id if i < len(active_list) and active_list[i] is not None else ''
                stashed_index = self.stashed_recipes[i].global_id if i < len(self.stashed_recipes) else ''
                waiting_index = self.waiting_recipes[i].global_id if i < len(self.waiting_recipes) else ''
                terminated_index = self.terminated_recipes[i].global_id if i < len(self.terminated_recipes) else ''

                print(f"\t {active_index if active_index is not None else '':<10} {stashed_index if stashed_index is not None else '':<10} {waiting_index if waiting_index is not None else '':<10} {terminated_index if terminated_index is not None else '':<10}")



    def getProductionsOrders(self):
        '''
        Função que obtém todas as ordens de produção ordenadas por quantidade de peças a produzir

        return: 
            None
        '''
        self.orders = [ProductionOrder(1, [4, 2, "2021-06-01 00:00:00"])] # simulação obtenção de ordens de produção
        for order in self.orders:
            krecipes = len(self.recipes)
            for i in range(order.quantity):
                recipe_index = krecipes + i
                self.recipes.append(Recipe(order.order_id, recipe_index, order.target_piece))
                # self.waiting_recipes.append(recipe_index)
                self.updateRecipesWaiting("add", self.recipes[-1])



    def getActiveRecipeIndex(self):
        '''
        Função que obtém o índice de uma receita ativa a None

        args:
            None
        return:
            int -> índice da receita ativa a None. None se não existir nenhuma receita ativa a None
        '''
        index_ = None
        for index, recipe in enumerate(self.active_recipes):
            if recipe is None:
                index_ = index
                break
        return index_ 



    def updateRecipesActive(self, operation: str, recipe_id: int, recipe: Recipe):
        '''
        Função que atualiza as receitas ativas. Atualiza também a receita no argumento.

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
        elif operation == "remove" and isinstance(recipe, Recipe):
            self.terminated_recipes.remove(recipe)


    
    def generateRecipes(self, is_even: bool = True):
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
        if len([x for x in self.active_recipes if x is not None]) == self.max_n_recipes:
            return
        
        # Definir a lista de receitas a serem verificadas
        recipes_to_check = self.stashed_recipes + self.waiting_recipes

        # Verificar as receitas geradas e que não estão em produção
        for recipe_to_check in recipes_to_check:
            # buscar um indíce livre para a receita
            free_recipe = self.getActiveRecipeIndex()
            if free_recipe is None:  
                break
            else:
                status = "stashed" if recipe_to_check in self.stashed_recipes else "waiting"
                recipe_to_check = self.schedule.schedule(recipe_to_check, status, is_even)
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
        schedule = self.schedule.schedule(recipe, "active", True) # tentar primeiro máquinas pares
        if isinstance(schedule, int):
            schedule = self.schedule.schedule(recipe, "active", False) # tentar máquinas impares
            if isinstance(schedule, int):
                return -1
        return schedule



    def waitSomeTransformation(self):
        '''
        Função que aguarda o fim de alguma transformação. Se não existir nenhuma receita ativa, vai continuamente tentar
        gerar receitas com base naquelas que se encontram em stash ou waiting. Assim que seja gerada uma receita,
        além de colocar a receita em produção, vai estar paralelamente a tentar gerar novas receitas, não ultrapassando o máximo
        de receitas ativas permitido.

        args:
            None
        return:
            None
        '''
        current_date = datetime.datetime.now()
        sleep_time = 0
        while not self.stop_recipes_thread:
            # if len([x for x in self.active_recipes if x is not None]) != 0:
            if any(self.active_recipes):
                if date_diff_in_Seconds(datetime.datetime.now(), current_date) >= sleep_time:
                    current_date = datetime.datetime.now() # buscar a hora atual
                    sleep_time = float('inf') # tempo de espera antes de verificar novamente os estados das receitas
                    for recipe in self.active_recipes:
                        if recipe is not None: # receita válida
                            self.client.getRecipeState(recipe) # obter o estado da receita
                            if recipe.end and recipe.piece_out == recipe.target_piece and recipe.piece_in != recipe.piece_out: # enviar receita para armazém inferior
                                recipe.machine_id = -1
                                recipe.piece_in = recipe.piece_out
                                recipe.end = False
                                recipe.finished_date = current_date + datetime.timedelta(seconds=0.5)
                                self.client.sendRecipe(recipe)
                            elif recipe.end and recipe.piece_out == recipe.target_piece and recipe.piece_in == recipe.target_piece: # receita terminou todas as transformações
                                recipe.finished_date = current_date
                                self.updateRecipesActive("remove", recipe.recipe_id, recipe)
                                self.updateRecipesTerminated("add", recipe)
                                self.printRecipesStatus()
                            elif recipe.end and recipe.piece_out != recipe.target_piece: # receita terminou transformação intermédia
                                recipe.finished_date = current_date
                                result = self.generateSingleRecipe(recipe)
                                if result == -1: # não foi possível gerar a receita
                                    self.updateRecipesActive("remove", recipe.recipe_id, recipe)
                                    self.updateRecipesStash("add", recipe)
                                else:
                                    recipe = result
                                    self.printAssociatedRecipes()
                                    self.client.sendRecipe(recipe)
                            # calcular o tempo de espera antes de verificar novamente os estados das receitas
                            recipe_time = date_diff_in_Seconds(recipe.finished_date, current_date)
                            if recipe_time <= sleep_time and recipe_time > 0:
                                sleep_time = recipe_time
                            else:
                                sleep_time = 0
            self.generateRecipes()
            self.generateRecipes(False)
            
                     

    def updateState(self):
        if self.state == 0 and self.got_orders:
            self.new_state = 1
            self.got_orders = False
        elif self.state == 1 and self.recipes_generated:
            self.new_state = 2
        
        if self.state != self.new_state:
            self.state = self.new_state



    def stateOperations(self):
        if self.state == 0:
            self.getProductionsOrders()
            self.printProductionOrders()
            self.printAssociatedRecipes()
            self.printRecipesStatus()
            self.got_orders = True
        elif self.state == 1:
            self.generateRecipes()
            self.generateRecipes(False)
            self.printRecipesStatus()
            self.recipes_generated = True
        pass



    def spin(self):
        '''
        Função que faz o lançamento das máquinas de estados de cada ordem de produção
        '''
        try:
            # lançar thread para cin
            # lançar thread para ordens de produção
            # lançar thread para receitas
            # lançar thread para excluir ordens de produção
            self.getProductionsOrders()
            self.printProductionOrders()
            self.printAssociatedRecipes()
            self.printRecipesStatus()
            spin_thread = threading.Thread(target=self.waitSomeTransformation)
            spin_thread.start()
            while True:
                pass
        except KeyboardInterrupt:
            self.printAssociatedRecipes()
            print(emoji.emojize(f'\n{bcolors.BOLD+bcolors.WARNING}[MES]{bcolors.ENDC + bcolors.ENDC} :warning:  Closing MES... :warning:'))
            self.stop_recipes_thread = True
            spin_thread.join()
            self.disconnect()
            sys.exit()
        except Exception as e:
            self.printAssociatedRecipes()
            print(emoji.emojize(f'\n{bcolors.BOLD+bcolors.WARNING}[MES]{bcolors.ENDC + bcolors.ENDC} :warning:  Closing MES... :warning:'))
            self.stop_recipes_thread = True
            print(traceback.format_exc())
            spin_thread.join()
            self.disconnect()
            sys.exit()