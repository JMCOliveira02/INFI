import psycopg2
import os


class Database:
    def __init__(self) -> None:
        pass


    def connect(self):
        '''
        connect to data base
        '''
        try:
            conn = psycopg2.connect(
                host="db.fe.up.pt",
                port="5432",
                user="infind202407",
                password="infinito",
                database="infind202407"
                #user=os.getenv('db_user'),
                #password=os.getenv('db_password'),
                #database=os.getenv('db_name')
            )

        except psycopg2.Error as e:
            print("Error connecting to the database:")
            print(e)

        else:
            print("Connection to database established successfully")
        
        return conn
    

    def send_query(self, query, parameters=None, fetch=True):
        try:
            conn = self.connect()
            cur = conn.cursor()

            if parameters is None:
                cur.execute(query)
            else:
                cur.execute(query, parameters)

            if fetch:
                ans = cur.fetchall()
            else:
                ans = None

            conn.commit()
        except psycopg2.Error as e:
            print("Error executing query:")
            print(e)
            # Rollback any changes made during the transaction
            conn.rollback()
            ans = None
        finally:
            # Close cursor and connection
            cur.close()
            conn.close()
            print("Connection to database closed")

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
        
  
        

            
    
         
        

        
    