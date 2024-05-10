from mes import psycopg2


class Database:
    def __init__(self) -> None:
        pass


    def connect(self):
        try:
            conn = psycopg2.connect(
                host="db.fe.up.pt",
                port="5432",
                user="sinfmeec15",
                password="bogas",
                database="sinfmeec15"
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