import psycopg2
from utils import bcolors
import emoji
import time
import datetime

class Database:
    def __init__(self) -> None:
        pass


    def connect(self):
        try:
            conn = psycopg2.connect(
                host="db.fe.up.pt",
                port="5432",
                user="infind202407",
                password="infinito",
                database="infind202407"
                #user=os.getenv('db_user'),
                #password=os.getenv('db_password'),
               # database=os.getenv('db_name')
            )
            print(f'\n{bcolors.BOLD}[Communications]{bcolors.ENDC}: Connecting to Data Base...', end=" ", flush=True)

        except psycopg2.Error as e:
            print("Error connecting to the database:")
            print(e)

        else:
            print(emoji.emojize('Connected to Data Base! :check_mark_button:'))
        
        return conn
    

    def send_query(self, query, parameters=None, fetch=True):
        conn = self.connect()
        cur = conn.cursor()

        if parameters == None:
            cur.execute(query)
        else:
            cur.execute(query, (parameters))

        if fetch == True:
            ans = cur.fetchall()
        else:
            ans = None

        conn.commit()
        cur.close()
        conn.close()
        print("Connection to database closed")

        return ans
    

    def get_all_orders(self):
        return self.send_query(
            """SELECT * from "INFI".orders;"""
        )
    def get_all_orders_sorted(self):
        return self.send_query(
            """SELECT * from "INFI".orders order by duedate asc;"""
        )
    def get_earliest_order(self):
        return self.send_query(
            """SELECT * from "INFI".orders order by duedate limit 1;"""
        )
    def update_initial_time(self):
        getReset_query = f"SELECT reset FROM erp_mes.\"start_time\""
        reset = self.send_query(getReset_query)[0][0]

        # Reset a falso significa que o MES foi abaixo
        # Reset a verdadeiro significa que a execução atual do MES começa no dia 0, 
        #   armazenando-se o instante de execução na base de dados como instante 
        #   inicial

        if reset == False:
            getTime_query = f"SELECT initial_time FROM erp_mes.\"start_time\""
            initialTime = reset = self.send_query(getTime_query)[0][0]
        if reset == True:
            initialTime = datetime.datetime.now()
            query = f"UPDATE erp_mes.\"start_time\" SET initial_time = '{initialTime}'"
            self.send_query(query, None, False)
        print("Dia 0 : " + str(initialTime))
        return initialTime

        


