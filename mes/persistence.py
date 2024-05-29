from mes import Database
from mes import ExpeditionOrder
from mes import Supplier
from mes import ProductionOrder
from mes import Recipe


class Persistence:
    def __init__(self, db: Database):
        self.db = db

    def parseSuppliersOrdersFromDB(self, suppliers_orders: list):
        suppliers_orders_parsed = []
        for order in suppliers_orders:
            order_parsed = Supplier(order[0], order[1], order[2]) # id, day, num_pieces
            suppliers_orders_parsed.append(order_parsed)
        return suppliers_orders_parsed



    def getLastSupplierOrderIdFromDB(self):
        return self.db.get_last_supplier_order_id()



    def getSupplierOrdersFromDB(self):
        supplier_orders_db = self.db.get_supplier_orders()
        return self.parseSuppliersOrdersFromDB(supplier_orders_db)



    def getCompletedSupplierOrdersFromDB(self):
        pass



    def getCarriersOccupiedFromDB(self):
        carriers_db = self.db.get_carriers_occupied()
        return carriers_db[0]


    def getLastProductionOrderIdFromDB(self):
        return self.db.get_last_production_order_id()



    def getOrdersFromDB(self):
        orders_db = self.db.get_production_orders()
        orders_parsed = []
        for order in orders_db:
            init = order[:5]
            # init.append(order[0])
            # init.append(order[1])
            # init.append(order[2])
            # init.append(order[3])
            # init.append(order[4])
            order_ = ProductionOrder(init) # order_id, client_id, target_piece, quantity, start_date
            order_.quantity_done = order[5]
            order_.status = order[6]
            orders_parsed.append(order_)
        return orders_parsed



    def getCompletedOrdersFromDB(self):
        pass



    def getLastExpeditionOrderIdFromDB(self):
        return self.db.get_last_expedition_order_id()



    def getDeliveriesFromDB(self):
        deliveries_db = self.db.get_expedition_orders()
        deliveries_parsed = []
        for delivery in deliveries_db:
            init = delivery[:5]
            delivery_ = ExpeditionOrder(init) # order_id, client_id, target_piece, quantity, expedition_date
            delivery_.quantity_sent = delivery[5]
            delivery_.status = delivery[6]
            deliveries_parsed.append(delivery_)
        return deliveries_parsed


    def getCompletedDeliveriesFromDB(self):
        pass



    def getRecipesFromDB(self):
        recipes_db = self.db.get_recipes()
        recipes_parsed = []
        for recipe in recipes_db:
            init = recipe[:2] + [recipe[6]]
            recipe_ = Recipe(init) # order_id, global_id, target_piece
            recipe_.recipe_id = recipe[2]
            recipe_.machine_id = recipe[3]
            recipe_.piece_in = recipe[4]
            recipe_.piece_out = recipe[5]
            recipe_.tool = recipe[7]
            recipe_.time = recipe[8]
            recipe_.end = recipe[9]
            recipe_.current_transformation = (recipe[10][0], recipe[10][1])
            recipe_.sended_date = (recipe[11][0], recipe[11][1])
            recipe_.finished_date = (recipe[12][0], recipe[12][1])
            recipe_.inactive = recipe[13]
            recipes_parsed.append(recipe_)
        return recipes_parsed



    def getActiveRecipesFromDB(self):
        recipes_db = self.db.get_active_recipes()
        recipes_db_parsed = []
        for recipe in recipes_db:
            init = recipe[:2] + [recipe[6]]
            recipe_ = Recipe(init) # order_id, global_id, target_piece
            recipe_.recipe_id = recipe[2]
            recipe_.machine_id = recipe[3]
            recipe_.piece_in = recipe[4]
            recipe_.piece_out = recipe[5]
            recipe_.tool = recipe[7]
            recipe_.time = recipe[8]
            recipe_.end = recipe[9]
            recipe_.current_transformation = (recipe[10][0], recipe[10][1])
            recipe_.sended_date = (recipe[11][0], recipe[11][1])
            recipe_.finished_date = (recipe[12][0], recipe[12][1])
            recipe_.inactive = recipe[13]
            recipes_db_parsed.append(recipe_)
        return recipes_db_parsed



    def getStashedRecipesFromDB(self):
        recipes_db = self.db.get_stashed_recipes()
        recipes_db_parsed = []
        for recipe in recipes_db:
            init = recipe[:2] + [recipe[6]]
            recipe_ = Recipe(init) # order_id, global_id, target_piece
            recipe_.recipe_id = recipe[2]
            recipe_.machine_id = recipe[3]
            recipe_.piece_in = recipe[4]
            recipe_.piece_out = recipe[5]
            recipe_.tool = recipe[7]
            recipe_.time = recipe[8]
            recipe_.end = recipe[9]
            recipe_.current_transformation = (recipe[10][0], recipe[10][1])
            recipe_.sended_date = (recipe[11][0], recipe[11][1])
            recipe_.finished_date = (recipe[12][0], recipe[12][1])
            recipe_.inactive = recipe[13]
            recipes_db_parsed.append(recipe_)
        return recipes_db_parsed



    def getWaitingRecipesFromDB(self):
        recipes_db = self.db.get_waiting_recipes()
        recipes_db_parsed = []
        for recipe in recipes_db:
            init = recipe[:2] + [recipe[6]]
            recipe_ = Recipe(init) # order_id, global_id, target_piece
            recipe_.recipe_id = recipe[2]
            recipe_.machine_id = recipe[3]
            recipe_.piece_in = recipe[4]
            recipe_.piece_out = recipe[5]
            recipe_.tool = recipe[7]
            recipe_.time = recipe[8]
            recipe_.end = recipe[9]
            recipe_.current_transformation = (recipe[10][0], recipe[10][1])
            recipe_.sended_date = (recipe[11][0], recipe[11][1])
            recipe_.finished_date = (recipe[12][0], recipe[12][1])
            recipe_.inactive = recipe[13]
            recipes_db_parsed.append(recipe_)
        return recipes_db_parsed



    def getTerminatedRecipesFromDB(self):
        recipes_db = self.db.get_terminated_recipes()
        recipes_db_parsed = []
        for recipe in recipes_db:
            init = recipe[:2] + [recipe[6]]
            recipe_ = Recipe(init) # order_id, global_id, target_piece
            recipe_.recipe_id = recipe[2]
            recipe_.machine_id = recipe[3]
            recipe_.piece_in = recipe[4]
            recipe_.piece_out = recipe[5]
            recipe_.tool = recipe[7]
            recipe_.time = recipe[8]
            recipe_.end = recipe[9]
            recipe_.current_transformation = (recipe[10][0], recipe[10][1])
            recipe_.sended_date = (recipe[11][0], recipe[11][1])
            recipe_.finished_date = (recipe[12][0], recipe[12][1])
            recipe_.inactive = recipe[13]
            recipes_db_parsed.append(recipe_)
        return recipes_db_parsed
