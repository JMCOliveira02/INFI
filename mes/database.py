from mes import datetime

from mes import psycopg2

from mes import emoji, bcolors




class Database:

    conn = None  # Class variable to store the database connection
    
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
        # conn = None
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
        except psycopg2.Error as e:
            print(f'\n{bcolors.BOLD+bcolors.FAIL}[Database]{bcolors.ENDC+bcolors.ENDC} Error executing query: ', end=" ", flush=True)
            print(e)
            # Rollback any changes made during the transaction
            conn.rollback()
            ans = None
        # finally:
        # # Close cursor (not necessary to close the connection)
        #     conn.commit()
        #     cur.close()
        #     conn.close()
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
        getReset_query = f"SELECT reset FROM erp_mes.\"start_time\""
        # reset = self.send_query(getReset_query)[0][0]
        reset = self.send_query(getReset_query)
        if len(reset) == 0:
            reset = False
            initialTime = datetime.datetime.now()
            query = """INSERT INTO erp_mes.start_time (initial_time, reset, id) 
                VALUES (%s, %s, 1)
            """
            parameters = (initialTime, reset)
            self.send_query(query, parameters, False)
            print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} Day 0 : {str(initialTime)}')
            return initialTime
        # else:
        #     reset = reset[0][1]

        # Reset a falso significa que o MES foi abaixo
        # Reset a verdadeiro significa que a execução atual do MES começa no dia 0, 
        #   armazenando-se o instante de execução na base de dados como instante 
        #   inicial

        # if reset == True:
        initialTime = datetime.datetime.now()
        query = f"UPDATE erp_mes.\"start_time\" SET initial_time = '{initialTime}'"
        self.send_query(query, None, False)
        # else:
        #     getTime_query = f"SELECT initial_time FROM erp_mes.\"start_time\""
        #     initialTime = reset = self.send_query(getTime_query)[0][0]
        return initialTime
    


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

