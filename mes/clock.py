from mes import datetime

from mes import Database
from mes import bcolors
from mes import date_diff_in_Seconds



class Clock:
    def __init__(self):
        self.db = Database()
        self.initial_date = self.db.update_initial_time()
        #self.initial_date = datetime.datetime.now()
        self.curr_time_seconds = date_diff_in_Seconds(datetime.datetime.now(), self.initial_date)
        self.curr_day = self.curr_time_seconds // 60
        self.curr_time_seconds = self.curr_time_seconds % 60
        print(f'\n{bcolors.BOLD}[MES]{bcolors.ENDC} Day {self.curr_day}: {str(self.initial_date)}')
        self.db.update_day(self.curr_day)



    def update_time(self):
        '''
        Função que atualiza a data atual

        args:
            None
        return:
            None
        '''
        self.curr_time_seconds = date_diff_in_Seconds(datetime.datetime.now(), self.initial_date)
        self.curr_day = self.curr_time_seconds // 60
        self.curr_time_seconds = self.curr_time_seconds % 60
        return
    

    def get_time(self):
        '''
        Função que retorna a data atual

        args:
            None
        return:
            tuple (int, int): data atual em dias e segundos
        '''
        return self.curr_day, self.curr_time_seconds
    


    def get_time_pretty(self):
        '''
        Função que retorna a data atual de forma legível

        args:
            None
        return:
            str: data atual em formato legível
        '''
        self.update_time()
        return f'{self.curr_day}:{(self.curr_time_seconds * 24)//60} (D:H)'
    


    def get_time_seconds(self):
        '''
        Função que retorna a data atual em segundos

        args:
            None
        return:
            int: data atual em segundos
        '''
        return self.curr_time_seconds + self.curr_day * 60
    


    def diff_time(self, time: tuple[int, int]):
        '''
        Função que retorna a diferença entre a data atual e a data passada

        args:
            time (tuple[int, int]): data passada (dias, segundos)
        return:
            int: diferença entre as datas em segundos
        '''
        self.update_time()
        time = time[0] * 60 + time[1]
        return self.curr_time_seconds + self.curr_day * 60 - time
    


    def diff_between_times(self, time1: tuple[int, int], time2: tuple[int, int]):
        '''
        Função que retorna a diferença entre duas datas. time1 - time2

        args:
            time1 (tuple[int, int]): primeira data (dias, segundos)
            time2 (tuple[int, int]): segunda data (dias, segundos)
        return:
            int: diferença entre as datas em segundos
        '''
        time1 = time1[0] * 60 + time1[1]
        time2 = time2[0] * 60 + time2[1]
        return time1 - time2


    
    def add_seconds(self, curr_date: tuple[int, int], seconds: int):
        '''
        Função que adiciona segundos a data atual

        args:
            curr_date (tupple): data a somar os segundos
            seconds (int): segundos a serem adicionados
        return:
            None
        '''
        new_date = curr_date[0] * 60 + curr_date[1] + seconds
        return new_date // 60, new_date % 60