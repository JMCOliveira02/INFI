from mes import datetime

from mes import Database
from mes import date_diff_in_Seconds



class Clock:
    def __init__(self):
        self.db = Database()
        self.initil_date = self.db.update_initial_time()
        self.curr_time_seconds = date_diff_in_Seconds(datetime.datetime.now(), self.initil_date)
        self.curr_day = self.curr_time_seconds / 60



    def update_time(self):
        '''
        Função que atualiza a data atual

        args:
            None
        return:
            None
        '''
        self.curr_time_seconds = date_diff_in_Seconds(datetime.datetime.now(), self.initil_date)
        self.curr_day = self.curr_time_seconds // 60
        return
    

    def get_time(self):
        '''
        Função que retorna a data atual

        args:
            None
        return:
            int, int: data atual em dias e segundos
        '''
        return self.curr_day, self.curr_time_seconds