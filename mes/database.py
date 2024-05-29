from mes import datetime

from mes import psycopg2

from mes import emoji, bcolors

from mes import Recipe
from mes import ProductionOrder
from mes import ExpeditionOrder
from mes import Supplier

from mes import date_diff_in_Seconds



class Database:

    #conn = None  # Class variable to store the database connection
    
    def __init__(self):
        self.host="db.fe.up.pt"
        self.port="5432"
        self.user="infind202407"
        self.password="infinito"
        self.database="infind202407"
        # if not Database.conn:  # If connection doesn't exist, create it
        #     print(f'\n{bcolors.BOLD}[Communications]{bcolors.ENDC} Connecting to Database...', end=" ", flush=True)
        #     try:
        #         Database.conn = psycopg2.connect(
        #             host="db.fe.up.pt",
        #             port="5432",
        #             user="infind202407",
        #             password="infinito",
        #             database="infind202407"
        #         )
        #         print(emoji.emojize('Connected to Database! :check_mark_button:'))
        #     except psycopg2.Error as e:
        #         print(emoji.emojize(f'\n{bcolors.BOLD}{bcolors.FAIL}[Communications]{bcolors.ENDC}{bcolors.ENDC} Error connecting to Database!  :cross_mark:'))
        #         print(e)



    def connect(self):
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except psycopg2.Error as e:
            print(emoji.emojize(f'\n{bcolors.BOLD+bcolors.FAIL}[Database]{bcolors.ENDC+bcolors.ENDC} Error connecting to the database!  :cross_mark:'))
            print(e)
        except Exception as e:
            print(e)
        
        return conn
    


    def disconnect(self):
        '''
        disconnect from data base
        '''
        print(f'\n{bcolors.BOLD}[Database]{bcolors.ENDC} Disconnecting from Database...', end=" ", flush=True)
        try:
            self.conn.close()
        except psycopg2.Error as e:
            print(emoji.emojize(f'\n{bcolors.BOLD}{bcolors.FAIL}[Database]{bcolors.ENDC}{bcolors.ENDC} Error disconnecting from Database!  :cross_mark:'))
            return
        print(emoji.emojize('Disconnected from Database! :check_mark_button:'))
        return
    


    def send_query(self, query, parameters=None, fetch=True):
        '''
        Execute a SQL query on the database.
        
        args:
            query - The SQL query to execute.
            parameters - Optional parameters for the query.
            fetch - Whether to fetch the results or not (default True).
        
        return:
            The result of the query if fetch is True, otherwise None.
        '''
        while(True):
            try:                
                conn = self.connect()
                        
                cur = conn.cursor()
                cur.execute(query, (parameters))  # Use parameters directly here

                if fetch:
                    ans = cur.fetchall()
                else:
                    ans = None
                conn.commit()
                cur.close()
                conn.close()
                break
            except psycopg2.Error as e:
                print(f'\n{bcolors.BOLD+bcolors.FAIL}[Database]{bcolors.ENDC+bcolors.ENDC} Error executing query: ', end=" ", flush=True)
                print(e)
                # Rollback any changes made during the transaction
                conn.rollback()
                ans = None
            except Exception as e:
                print(f'\n{bcolors.BOLD+bcolors.FAIL}[Database]{bcolors.ENDC+bcolors.ENDC} Error executing query: ', end=" ", flush=True)
                print(e)
        return ans   
    


    def get_all_supply_orders(self):
        return self.send_query(
            """SELECT * from erp_mes.supply_order;"""
        )
    


    def get_all_supply_orders_sorted(self):
        return self.send_query(
            """SELECT * from erp_mes.supply_order order by buy_date asc;"""
        )
    


    def get_earliest_order(self):
        return self.send_query(
            """SELECT * from erp_mes.supply_order order by buy_date asc limit 1;"""
        )
    


    def get_production_order(self):
        return self.send_query(
            """
            SELECT po.* 
            FROM erp_mes.production_order po
            LEFT JOIN erp_mes.production_status ps ON po.id = ps.production_order_id
            WHERE ps.id IS NULL
            ORDER BY po.start_date ASC, po.quantity DESC;
            """
        )
    


    def insert_production_status(self, production_order_id, end_date):
        query = """
            INSERT INTO erp_mes.production_status (production_order_id, end_date)
            VALUES (%s, %s);
        """
        parameters = (production_order_id, end_date)
        self.send_query(query, parameters, fetch=False)  

    def insert_stock(self, day: int, stock: dict):
        for piece, quantity in stock.items():
            query = """
                INSERT INTO erp_mes.stock (day, piece, quantity)
                VALUES (%s, %s, %s);
            """
            self.send_query(query, (day, "P"+str(piece), quantity), fetch=False)
    


    def get_expedition_order(self):
        return self.send_query(
            """
            SELECT eo.* 
            FROM erp_mes.expedition_order eo
            LEFT JOIN erp_mes.expedition_status es ON po.id = ps.expedition_order_id
            WHERE ps.id IS NULL
            ORDER BY po.start_date ASC;
            """
        )
    


    def expedition_production_status(self, expedition_order_id, end_date):
        query = """
            INSERT INTO erp_mes.expedition_status (expedition_order_id, end_date)
            VALUES (%s, %s);
        """
        parameters = (expedition_order_id, end_date)
        self.send_query(query, parameters, fetch=False)  
    


    def update_stock_quantity(self, piece, new_quantity):
        query = "UPDATE erp_mes.stock SET quantity = %s WHERE piece = %s"
        parameters = (new_quantity, piece)
        self.send_query(query, parameters)



    def update_initial_time(self):
        print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} Checking Database...')
        query = f"SELECT * FROM erp_mes.\"start_time\""
        reply = self.send_query(query)
        if len(reply) == 0:
            reply = False
            initialTime = datetime.datetime.now()
            query = """INSERT INTO erp_mes.start_time (initial_time, id, day) 
                VALUES (%s, 1, %s)
            """
            parameters = (initialTime, 0)
            self.send_query(query, parameters, False)
            return initialTime

        # MES foi a abaixo. Verficar em que dia está
        query = """SELECT initial_time FROM erp_mes.start_time"""
        reply = self.send_query(query)
        
        return reply[0][0]
    


    def update_day(self, day):
        query = "UPDATE erp_mes.start_time SET day = %s"
        self.send_query(query, (day,), False)
    


    def get_production_order_by_id(self, id):
        """
        Retrieves production orders from the database with an ID greater than or equal to the specified ID.

        Args:
            id (int): The ID to search for. Production orders with IDs greater than or equal to this value will be retrieved.

        Returns:
            list or None: A list of production orders matching the criteria, or None if no matching orders are found.
        """   
        query= """ SELECT po.* 
            FROM erp_mes.production_order po
            WHERE po.id >=%s
            """
        parameters=(id,)    
        return self.send_query(query, parameters)
    


    def get_expedition_order_by_id(self, id):
        """
        Retrieves expedition orders from the database with an ID greater than or equal to the specified ID.

        Args:
         id (int): The ID to search for. Expedition orders with IDs greater than or equal to this value will be retrieved.

        Returns:
        list or None: A list of expedition orders matching the criteria, or None if no matching orders are found.
        """
        query= """ SELECT eo.* 
            FROM erp_mes.expedition_order eo
            WHERE eo.id >=%s
            """
        parameters=(id,)    
        return self.send_query(query, parameters)
    


    def add_piece_quantities_in_order(self, day, piece_quantities):
        """
        Adds piece quantities to the database in order.

        Args:
            piece_quantities (list of tuples): A list of piece quantities.

        Returns:
            bool: True if the piece quantities were successfully added, False otherwise.
        """

        # Iterate over the piece quantities and insert them into the database
        for index, quantity in enumerate(piece_quantities, start=1):
            query = "INSERT INTO erp_mes.stock (day, piece, quantity) VALUES (%s, %s, %s)"            
            parameters = (day, index, quantity)
            self.send_query(query, parameters, fetch=False)
            


    def get_supply_orders_by_id(self, id):
        """
        Retrieves supply orders from the database where the ID is greater than the specified threshold.

        Args:
            id (int): The ID threshold.

        Returns:
            list: A list of tuples containing the supply order data if found, else an empty list.
        """
        query = """SELECT * FROM erp_mes.delivery WHERE id >= %s"""
        parameters = (id,)
        return self.send_query(query,(parameters))



    def insert_active_recipe(self, recipe: Recipe):
        """
        Inserts the active recipe into the database.

        Args:
            recipe (Recipe): The active recipe to insert.

        Returns:
            None
        """
        query = """INSERT INTO erp_mes.mes_active_recipes (order_id, global_id, recipe_id, machine_id, piece_in, piece_out, target_piece, tool, time, "end", current_transformation, sended_date, finished_date, inactive) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        parameters = (recipe.order_id, recipe.global_id, recipe.recipe_id, recipe.machine_id, recipe.piece_in, recipe.piece_out, recipe.target_piece, recipe.tool, recipe.time, recipe.end, [recipe.current_transformation[0], recipe.current_transformation[1]] if recipe.current_transformation != None else None, [recipe.sended_date[0], recipe.sended_date[1]] if recipe.sended_date != None else None, [recipe.finished_date[0], recipe.finished_date[1]] if recipe.finished_date != None else None, recipe.inactive)
        self.send_query(query, parameters, fetch=False)



    def remove_active_recipe(self, recipe: Recipe):
        """
        Removes the active recipe from the database.

        Args:
            recipe (Recipe): The active recipe to remove.

        Returns:
            None
        """
        query = """UPDATE erp_mes.mes_active_recipes SET order_id=%s, global_id=%s, recipe_id=%s, machine_id=%s, piece_in=%s, piece_out=%s, target_piece=%s, tool=%s, time=%s, "end"=%s, current_transformation=%s, sended_date=%s, finished_date=%s, inactive=%s WHERE global_id = %s"""
        # query = """DELETE FROM erp_mes.mes_active_recipes WHERE global_id = %s"""
        parameters = (None, None, None, None, None, None, None, None, None, 'FALSE', None, None, None, 'FALSE', recipe.global_id)
        self.send_query(query, parameters, fetch=False)



    def insert_stashed_recipe(self, recipe: Recipe):
        """
        Inserts the stashed recipe into the database.

        Args:
            recipe (Recipe): The stashed recipe to insert.

        Returns:
            None
        """
        query = """INSERT INTO erp_mes.mes_stashed_recipes (order_id, global_id, recipe_id, machine_id, piece_in, piece_out, target_piece, tool, time, "end", current_transformation, sended_date, finished_date) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        parameters = (recipe.order_id, recipe.global_id, recipe.recipe_id, recipe.machine_id, recipe.piece_in, recipe.piece_out, recipe.target_piece, recipe.tool, recipe.time, recipe.end, [recipe.current_transformation[0], recipe.current_transformation[1]] if recipe.current_transformation != None else None, [recipe.sended_date[0], recipe.sended_date[1]] if recipe.sended_date != None else None, [recipe.finished_date[0], recipe.finished_date[1]] if recipe.finished_date != None else None)
        self.send_query(query, parameters, fetch=False)



    def remove_stashed_recipe(self, recipe: Recipe|None):
        """
        Removes the stashed recipe from the database.

        Args:
            recipe (Recipe): The stashed recipe to remove.

        Returns:
            None
        """
        # if recipe is None:
        #     return
        if recipe == None:
            return
        query = """DELETE FROM erp_mes.mes_stashed_recipes WHERE global_id = %s"""
        parameters = (recipe.global_id,)
        self.send_query(query, parameters, fetch=False)



    def insert_waiting_recipe(self, recipe: Recipe):
        """
        Inserts the waiting recipe into the database.

        Args:
            recipe (Recipe): The waiting recipe to insert.

        Returns:
            None
        """
        query = """INSERT INTO erp_mes.mes_waiting_recipes (order_id, global_id, recipe_id, machine_id, piece_in, piece_out, target_piece, tool, time, "end", current_transformation, sended_date, finished_date) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        parameters = (recipe.order_id, recipe.global_id, recipe.recipe_id, recipe.machine_id, recipe.piece_in, recipe.piece_out, recipe.target_piece, recipe.tool, recipe.time, recipe.end, [recipe.current_transformation[0], recipe.current_transformation[1]] if recipe.current_transformation != None else None, [recipe.sended_date[0], recipe.sended_date[1]] if recipe.sended_date != None else None, [recipe.finished_date[0], recipe.finished_date[1]] if recipe.finished_date != None else None)
        self.send_query(query, parameters, fetch=False)
    


    def remove_waiting_recipe(self, recipe: Recipe|None):
        """
        Removes the waiting recipe from the database.

        Args:
            recipe (Recipe): The waiting recipe to remove.

        Returns:
            None
        """
        if recipe == None:
            return
        query = """DELETE FROM erp_mes.mes_waiting_recipes WHERE global_id = %s"""
        parameters = (recipe.global_id,)
        self.send_query(query, parameters, fetch=False)



    def insert_terminated_recipe(self, recipe: Recipe):
        """
        Inserts the terminated recipe into the database.

        Args:
            recipe (Recipe): The terminated recipe to insert.

        Returns:
            None
        """
        query = """INSERT INTO erp_mes.mes_terminated_recipes (order_id, global_id, recipe_id, machine_id, piece_in, piece_out, target_piece, tool, time, "end", current_transformation, sended_date, finished_date) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        parameters = (recipe.order_id, recipe.global_id, recipe.recipe_id, recipe.machine_id, recipe.piece_in, recipe.piece_out, recipe.target_piece, recipe.tool, recipe.time, recipe.end, [recipe.current_transformation[0], recipe.current_transformation[1]] if recipe.current_transformation != None else None, [recipe.sended_date[0], recipe.sended_date[1]] if recipe.sended_date != None else None, [recipe.finished_date[0], recipe.finished_date[1]] if recipe.finished_date != None else None)
        self.send_query(query, parameters, fetch=False)



    def remove_terminated_recipe(self, recipe: Recipe):
        """
        Removes the terminated recipe from the database.

        Args:
            recipe (Recipe): The terminated recipe to remove.

        Returns:
            None
        """
        query = """DELETE FROM erp_mes.mes_terminated_recipes WHERE global_id = %s"""
        parameters = (recipe.global_id,)
        self.send_query(query, parameters, fetch=False)



    def insert_recipe(self, recipe: Recipe):
        """
        Inserts a recipe into the database.

        Args:
            recipe (Recipe): The recipe to insert.

        Returns:
            None
        """
        query = """INSERT INTO erp_mes.mes_recipes (order_id, global_id, recipe_id, machine_id, piece_in, piece_out, target_piece, tool, time, "end", current_transformation, sended_date, finished_date, inactive) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        parameters = (recipe.order_id, recipe.global_id, recipe.recipe_id, recipe.machine_id, recipe.piece_in, recipe.piece_out, recipe.target_piece, recipe.tool, recipe.time, recipe.end, [recipe.current_transformation[0], recipe.current_transformation[1]] if recipe.current_transformation != None else None, [recipe.sended_date[0], recipe.sended_date[1]] if recipe.sended_date != None else None, [recipe.finished_date[0], recipe.finished_date[1]] if recipe.finished_date != None else None, recipe.inactive)
        self.send_query(query, parameters, fetch=False)



    def update_recipe(self, recipe: Recipe):
        """
        Updates a recipe in the database.

        Args:
            recipe (Recipe): The recipe to update.

        Returns:
            None
        """
        query = """UPDATE erp_mes.mes_recipes SET order_id = %s, global_id = %s, recipe_id = %s, machine_id = %s, piece_in = %s, piece_out = %s, target_piece = %s, tool = %s, time = %s, "end" = %s, current_transformation = %s, sended_date = %s, finished_date = %s, inactive = %s WHERE global_id = %s"""
        parameters = (recipe.order_id, recipe.global_id, recipe.recipe_id, recipe.machine_id, recipe.piece_in, recipe.piece_out, recipe.target_piece, recipe.tool, recipe.time, recipe.end, [recipe.current_transformation[0], recipe.current_transformation[1]] if recipe.current_transformation != None else None, [recipe.sended_date[0], recipe.sended_date[1]] if recipe.sended_date != None else None, [recipe.finished_date[0], recipe.finished_date[1]] if recipe.finished_date != None else None, recipe.inactive, recipe.global_id)
        self.send_query(query, parameters, fetch=False)
        query = """UPDATE erp_mes.mes_active_recipes SET order_id = %s, global_id = %s, recipe_id = %s, machine_id = %s, piece_in = %s, piece_out = %s, target_piece = %s, tool = %s, time = %s, "end" = %s, current_transformation = %s, sended_date = %s, finished_date = %s, inactive = %s WHERE global_id = %s"""
        parameters = (recipe.order_id, recipe.global_id, recipe.recipe_id, recipe.machine_id, recipe.piece_in, recipe.piece_out, recipe.target_piece, recipe.tool, recipe.time, recipe.end, [recipe.current_transformation[0], recipe.current_transformation[1]] if recipe.current_transformation != None else None, [recipe.sended_date[0], recipe.sended_date[1]] if recipe.sended_date != None else None, [recipe.finished_date[0], recipe.finished_date[1]] if recipe.finished_date != None else None, recipe.inactive, recipe.global_id)
        self.send_query(query, parameters, fetch=False)


    def remove_recipe(self, recipe: Recipe):
        """
        Removes a recipe from the database.

        Args:
            recipe (Recipe): The recipe to remove.

        Returns:
            None
        """
        query = """DELETE FROM erp_mes.mes_recipes WHERE global_id = %s"""
        parameters = (recipe.global_id,)
        self.send_query(query, parameters, fetch=False)



    def insert_production_order(self, order: ProductionOrder):
        """
        Inserts a production order into the database.

        Args:
            production_order (ProductionOrder): The production order to insert.

        Returns:
            None
        """
        query = """INSERT INTO erp_mes.mes_production_orders (order_id, client_id, target_piece, quantity, start_date, quantity_done, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        parameters = (order.order_id, order.client_id, order.target_piece, order.quantity, order.start_date, order.quantity_done, order.status)
        self.send_query(query, parameters, fetch=False)



    def update_production_order(self, order: ProductionOrder):
        """
        Updates a production order in the database.

        Args:
            production_order (ProductionOrder): The production order to update.

        Returns:
            None
        """
        query = """UPDATE erp_mes.mes_production_orders SET order_id = %s, client_id = %s, target_piece = %s, quantity = %s, start_date = %s, quantity_done = %s, status = %s WHERE order_id = %s"""
        parameters = (order.order_id, order.client_id, order.target_piece, order.quantity, order.start_date, order.quantity_done, order.status, order.order_id)
        self.send_query(query, parameters, fetch=False)



    def remove_production_order(self, order: ProductionOrder):
        """
        Removes a production order from the database.

        Args:
            production_order (ProductionOrder): The production order to remove.

        Returns:
            None
        """
        query = """DELETE FROM erp_mes.mes_production_orders WHERE order_id = %s"""
        parameters = (order.order_id,)
        self.send_query(query, parameters, fetch=False)
    


    def insert_completed_production_order(self, order: ProductionOrder):
        """
        Inserts a completed production order into the database.

        Args:
            production_order (ProductionOrder): The production order to insert.

        Returns:
            None
        """
        query = """INSERT INTO erp_mes.mes_completed_production_orders (order_id, client_id, target_piece, quantity, start_date, quantity_done, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        parameters = (order.order_id, order.client_id, order.target_piece, order.quantity, order.start_date, order.quantity_done, order.status)
        self.send_query(query, parameters, fetch=False)
    


    def remove_completed_production_order(self, order: ProductionOrder):
        """
        Removes a completed production order from the database.

        Args:
            production_order (ProductionOrder): The production order to remove.

        Returns:
            None
        """
        query = """DELETE FROM erp_mes.mes_completed_production_orders WHERE order_id = %s"""
        parameters = (order.order_id,)
        self.send_query(query, parameters, fetch=False)



    def insert_expedition_order(self, order: ExpeditionOrder):
        """
        Inserts an expedition order into the database.

        Args:
            expedition_order (ExpeditionOrder): The expedition order to insert.

        Returns:
            None
        """
        query = """INSERT INTO erp_mes.mes_deliveries (order_id, client_id, target_piece, quantity, expedition_date, quantity_sent, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        parameters = (order.order_id, order.client_id, order.target_piece, order.quantity, order.expedition_date, order.quantity_sent, order.status)
        self.send_query(query, parameters, fetch=False)



    def update_expediton_order(self, order: ExpeditionOrder):
        """
        Updates an expedition order in the database.

        Args:
            expedition_order (ExpeditionOrder): The expedition order to update.

        Returns:
            None
        """
        query = """UPDATE erp_mes.mes_deliveries SET order_id = %s, client_id = %s, target_piece = %s, quantity = %s, expedition_date = %s, quantity_sent = %s, status = %s WHERE order_id = %s"""
        parameters = (order.order_id, order.client_id, order.target_piece, order.quantity, order.expedition_date, order.quantity_sent, order.status, order.order_id)
        self.send_query(query, parameters, fetch=False)



    def remove_expedition_order(self, order: ExpeditionOrder):
        """
        Removes an expedition order from the database.

        Args:
            expedition_order (ExpeditionOrder): The expedition order to remove.

        Returns:
            None
        """
        query = """DELETE FROM erp_mes.mes_deliveries WHERE order_id = %s"""
        parameters = (order.order_id,)
        self.send_query(query, parameters, fetch=False)



    def insert_completed_expedition_order(self, order: ExpeditionOrder):
        """
        Inserts a completed expedition order into the database.

        Args:
            expedition_order (ExpeditionOrder): The expedition order to insert.

        Returns:
            None
        """
        query = """INSERT INTO erp_mes.mes_completed_deliveries (order_id, client_id, target_piece, quantity, expedition_date, quantity_sent, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        parameters = (order.order_id, order.client_id, order.target_piece, order.quantity, order.expedition_date, order.quantity_sent, order.status)
        self.send_query(query, parameters, fetch=False)



    def remove_completed_expedition_order(self, order: ExpeditionOrder):
        """
        Removes a completed expedition order from the database.

        Args:
            expedition_order (ExpeditionOrder): The expedition order to remove.

        Returns:
            None
        """
        query = """DELETE FROM erp_mes.mes_completed_deliveries WHERE order_id = %s"""
        parameters = (order.order_id,)
        self.send_query(query, parameters, fetch=False)
    


    def insert_supply_order(self, order: Supplier):
        """
        Inserts a supplier order into the database.

        Args:
            supplier_order (SupplierOrder): The supplier order to insert.

        Returns:
            None
        """
        query = """INSERT INTO erp_mes.mes_supply_orders (id ,day, num_pieces) 
            VALUES (%s, %s, %s)"""
        parameters = (order.id, order.day, [order.num_pieces[0], order.num_pieces[1]])
        self.send_query(query, parameters, fetch=False)



    def remove_supply_order(self, order: Supplier):
        """
        Removes a supplier order from the database.

        Args:
            supplier_order (SupplierOrder): The supplier order to remove.

        Returns:
            None
        """
        query = """DELETE FROM erp_mes.mes_supply_orders WHERE id = %s"""
        parameters = (order.id,)
        self.send_query(query, parameters, fetch=False)

    

    def insert_completed_supply_order(self, order: Supplier):
        """
        Inserts a completed supplier order into the database.

        Args:
            supplier_order (SupplierOrder): The supplier order to insert.

        Returns:
            None
        """
        query = """INSERT INTO erp_mes.mes_completed_supply_orders (id ,day, num_pieces) 
            VALUES (%s, %s, %s)"""
        parameters = (order.id, order.day, [order.num_pieces[0], order.num_pieces[1]])
        self.send_query(query, parameters, fetch=False)



    def remove_completed_supply_order(self, order: Supplier):
        """
        Removes a completed supplier order from the database.

        Args:
            supplier_order (SupplierOrder): The supplier order to remove.

        Returns:
            None
        """
        query = """DELETE FROM erp_mes.mes_completed_supply_orders WHERE id = %s"""
        parameters = (order.id,)
        self.send_query(query, parameters, fetch=False)



    def update_carrier_occupied(self, index: int, value: int|None):
        """
        Updates the carrier occupied status in the database.

        Args:
            index (int): The carrier index.
            order_id (int): The order ID.

        Returns:
            None
        """
        carrier = "carrier"+str(index)
        query =f"UPDATE erp_mes.mes_carriers_occupied SET {carrier} = %s"
        parameters = (value,)
        self.send_query(query, parameters, fetch=False)



    def insert_piece_time(self, recipe: Recipe, client_id: int, total_time: int):
        """
        Updates the piece time in the database.

        Args:
            recipe (Recipe): The recipe to update.

        Returns:
            None
        """
        query = """INSERT INTO erp_mes.piece_info (client_order_id, piece, total_time)
        VALUES (%s, %s, %s)"""
        parameters = [client_id, 'P'+str(recipe.target_piece), total_time]
        self.send_query(query, parameters, fetch=False)



    def get_last_supplier_order_id(self):
        """
        Retrieves the last supplier order ID from the database.

        Returns:
            int: The last supplier order ID.
        """
        query = "SELECT MAX(id) FROM erp_mes.mes_supply_orders"
        return self.send_query(query)[0][0]
    


    def get_supplier_orders(self):
        """
        Retrieves supplier orders from the database.

        Args:
            None

        Returns:
            supplier_orders (list): A list of the supplier orders.
        """
        query = "SELECT * FROM erp_mes.mes_supply_orders"
        return self.send_query(query)
    


    def get_carriers_occupied(self):
        """
        Retrieves the carriers that are currently occupied.

        Args:
            None

        Returns:
            carriers_occupied (list): A list of the carriers that are currently occupied.
        """
        query = "SELECT * FROM erp_mes.mes_carriers_occupied"
        return self.send_query(query)
    


    def get_last_production_order_id(self):
        """
        Retrieves the last production order ID from the database.

        Args:
            None

        Returns:
            last_production_order_id (int): The last production order ID.
        """
        query = "SELECT MAX(order_id) FROM erp_mes.mes_production_orders"
        return self.send_query(query)[0][0]
    


    def get_production_orders(self):
        """
        Retrieves production orders from the database.

        Args:
            None

        Returns:
            production_orders (list): A list of the production orders.
        """
        query = "SELECT * FROM erp_mes.mes_production_orders"
        return self.send_query(query)



    def get_last_expedition_order_id(self):
        """
        Retrieves the last expedition order ID from the database.

        Args:
            None
        
        Returns:
            last_expedition_order_id (int): The last expedition order ID.
        """
        query = "SELECT MAX(order_id) FROM erp_mes.mes_deliveries"
        return self.send_query(query)[0][0]
    


    def get_expedition_orders(self):
        """
        Retrieves expedition orders from the database.

        Args:
            None

        Returns:
            expedition_orders (list): A list of the expedition orders.
        """
        query = "SELECT * FROM erp_mes.mes_deliveries"
        return self.send_query(query)



    def get_recipes(self):
        """
        Retrieves recipes from the database.

        Args:
            None

        Returns:
            recipes (list): A list of the recipes.
        """
        query = "SELECT * FROM erp_mes.mes_recipes"
        return self.send_query(query)
    


    def get_active_recipes(self):
        """
        Retrieves active recipes from the database.

        Args:
            None

        Returns:
            active_recipes (list): A list of the active recipes.
        """
        query = "SELECT * FROM erp_mes.mes_active_recipes"
        return self.send_query(query)
    


    def get_stashed_recipes(self):
        """
        Retrieves stashed recipes from the database.

        Args:
            None

        Returns:
            stashed_recipes (list): A list of the stashed recipes.
        """
        query = "SELECT * FROM erp_mes.mes_stashed_recipes"
        return self.send_query(query)
    


    def get_waiting_recipes(self):
        """
        Retrieves waiting recipes from the database.

        Args:
            None

        Returns:
            waiting_recipes (list): A list of the waiting recipes.
        """
        query = "SELECT * FROM erp_mes.mes_waiting_recipes"
        return self.send_query(query)
    


    def get_terimanted_recipes(self):
        """
        Retrieves terminated recipes from the database.

        Args:
            None

        Returns:
            terminated_recipes (list): A list of the terminated recipes.
        """
        query = "SELECT * FROM erp_mes.mes_terminated_recipes"
        return self.send_query(query)