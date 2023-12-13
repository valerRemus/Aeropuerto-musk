
class Slot:
    def __init__(self):
        self.vuelo_id = None
        self.fecha_inicial = None
        self.fecha_final = None

    def asigna_vuelo(self, vuelo_id, fecha_inicial, fecha_final):
        self.vuelo_id = vuelo_id
        self.fecha_inicial = fecha_inicial
        self.fecha_final = fecha_final

    def slot_esta_libre_fecha_determinada(self, fecha):
        if self.fecha_inicial is None or self.fecha_final is None:
            return 0
        elif self.fecha_inicial <= fecha <= self.fecha_final:
            return self.fecha_final - fecha
        return 0

