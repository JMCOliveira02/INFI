import modules.communications.plc_communications as plc
import threading
import time

class GenCin:
    def __init__(self, client: plc.PLCCommunications):
        self.client = client



    def _spawnPieces_thread(self, generator: int, num_pieces: int):
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
            Exception: caso o número de peças seja inválido ou não haja geradores disponíveis.
        '''
        # validar número de peças
        if num_pieces[0] < 0 or num_pieces[1] < 0:
            raise ValueError("Number of pieces must be greater than 0.", name="InvalidNumberPieces")
        
        # Se número de peças de cada tipo for maior que 1, dividir por duas threads cada tipo
        # Por exemplo, se número de peças do tipo 1 for 3, então gera 2 threads, uma envia 2 peças e outra uma peça
        generators = [(1, 2), (3, 4)]
        threads = []

        for generator, num_piece in zip(generators, num_pieces):
            if num_piece > 1:
                for i in range(2):
                    t = threading.Thread(target=self._spawnPieces_thread, args=(generator[i], num_piece // 2 + (num_piece % 2 if i == 1 else 0)))
                    threads.append(t)
            elif num_piece == 1:
                t = threading.Thread(target=self._spawnPieces_thread, args=(generator[0], 1))
                threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()