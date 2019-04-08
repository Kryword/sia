class Nodo(object):
    def __init__(self, estado):
        self.estado = estado
        self.coste = 0
        self.heuristica = 0
        self.camino = []
    def __cmp__(self, other):
        if(self.estado[0] == other.estado[0] and self.estado[1] == other.estado[1]):
            return 0
        elif(self.coste + self.heuristica > other.coste + other.heuristica):
            return -1
        else:
            return 1
    def __getitem__(self, item):
        return getattr(self, item)