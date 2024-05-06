from opcua import ua
import datetime
import yaml
import emoji



with open("constants.yaml", 'r') as stream2:
    CONSTANTS = yaml.safe_load(stream2)



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def printAuthorsCredits(show_credits=True):
    print(chr(27) + "[2J")
    if show_credits:
        print("\n***************************************************")
        print(emoji.emojize("Academic Year: 2023/2024 :calendar:"))
        print(emoji.emojize("Course: Informática Indústrial (INFI) :TOP_arrow:"))
        print("Students:")
        print(emoji.emojize(":right_arrow:  Carlos Thadeu Aguiar de Faria - up202202472"))
        print(emoji.emojize(":right_arrow:  Daniele da Mota Caldana - up202308625"))
        print(emoji.emojize(":right_arrow:  João Miguel de Carvalho Oliveira - up202007580"))
        print(emoji.emojize(":right_arrow:  Joana Sofia Pais Silva - up202006241"))
        print(emoji.emojize(":right_arrow:  Thiago Baldassarri Levin - up201900223"))
        print("***************************************************\n")
        print(emoji.emojize(f':rocket:  {bcolors.HEADER}Starting MES{bcolors.ENDC} :rocket:\n'))



def date_diff_in_Seconds(dt2: datetime.datetime, dt1: datetime.datetime):
        '''
        Função que calcula a diferença entre duas datas em segundos
        
        args:
            dt2: datetime -> data final
            dt1: datetime -> data inicial
        return:
            int -> diferença entre as duas datas em segundos
        '''
        # Calculate the time difference between dt2 and dt1
        timedelta = dt2 - dt1
        # Return the total time difference in seconds
        return timedelta.days * 24 * 3600 + timedelta.seconds