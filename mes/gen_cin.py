from mes import threading
from mes import time

import mes as PLCCommunications
from mes import cur_pieces_top_wh, updatePiecesTopWh
from mes import bcolors, emoji

class GenCin():
    def __init__(self, client: PLCCommunications):
        self.client = client


    # método privado
    def __spawnPieces_thread(self, generator: int, num_pieces: int):
        # realiza tarefa
        self.client.incomingPiece(generator, num_pieces)



    def spawnPieces(self, num_pieces: list):
        '''
        Função para receber peças de um fornecedor. Basta indicar o
        número de peças para cada tipo. Internamente é feita a gestão de qual
        gerador de peças é escolhido. Geradores 1 e 2 geram peças do tipo 1.
        Geradores 3 e 4 geram peças do tipo 2.

        args:
            num_pieces (list): número de peças a serem geradas de cada tipo. [1, 3] significa 1 peça do tipo 1 e 3 peças do tipo 2.
        return:
            -1: caso o número de peças seja inválido ou não haja geradores disponíveis.
        '''
        # validar número de peças
        if any(piece < 0 for piece in num_pieces):
            print(emoji.emojize(f"\n{bcolors.FAIL+bcolors.BOLD}[Shop Floor]{bcolors.ENDC+bcolors.ENDC}:{bcolors.FAIL} Invalid number of pieces {bcolors.UNDERLINE}{num_pieces}{bcolors.ENDC}"))
            return -1
        # validar número de peças for igual a zero
        if sum(num_pieces) == 0:
            print(emoji.emojize(f"\n{bcolors.WARNING+bcolors.BOLD}[Shop Floor]{bcolors.ENDC}: :warning: Supplier's order received but there are no pieces to spawn{bcolors.ENDC}"))
            return -1

        print(emoji.emojize(f"\n{bcolors.BOLD}[Shop Floor]{bcolors.ENDC}: Supplier's order received and accepted. :check_mark_button:\n\033[4mOrder summary\033[0m:\n\tType 1 -> {num_pieces[0]} pieces\n\tType 2 -> {num_pieces[1]} pieces"))
        print("Working...", end=" ", flush=True)

        updatePiecesTopWh(self.client)
        prev_type1 = cur_pieces_top_wh[1]
        prev_type2 = cur_pieces_top_wh[2]


        # Se número de peças de cada tipo for maior que 1, dividir por duas threads cada tipo
        # Por exemplo, se número de peças do tipo 1 for 3, então gera 2 threads, uma envia 2 peças e outra uma peça
        generators = [(1, 2), (3, 4)]
        threads = []

        for generator, num_piece in zip(generators, num_pieces):
            if num_piece > 1:
                for i in range(2):
                    t = threading.Thread(target=self.__spawnPieces_thread, args=(generator[i], num_piece // 2 + (num_piece % 2 if i == 1 else 0)))
                    threads.append(t)
            elif num_piece == 1:
                t = threading.Thread(target=self.__spawnPieces_thread, args=(generator[0], 1))
                threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        # Esperar peças entrar no armazém
        updatePiecesTopWh(self.client)
        while (cur_pieces_top_wh[1] < (prev_type1 + num_pieces[0])) or (cur_pieces_top_wh[2] < (prev_type2 + num_pieces[1])):
            time.sleep(0.5)
            updatePiecesTopWh(self.client)
        print(f"Supplier's order handed over. \n{bcolors.UNDERLINE}Current number of pieces available{bcolors.ENDC}:\n\tType 1 -> {cur_pieces_top_wh[1]} pieces\n\tType 2 -> {cur_pieces_top_wh[2]} pieces")