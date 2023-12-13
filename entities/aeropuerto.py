import datetime
import pandas as pd

from entities.slot import Slot


class Aeropuerto:
    def __init__(self, vuelos: pd.DataFrame, slots: int, t_embarque_nat: int, t_embarque_internat: int):
        self.df_vuelos = vuelos
        self.n_slots = slots
        self.slots = {}
        self.tiempo_embarque_nat = t_embarque_nat
        self.tiempo_embarque_internat = t_embarque_internat

        for i in range(1, self.n_slots + 1):
            self.slots[i] = Slot()

        self.df_vuelos['fecha_despegue'] = pd.NaT
        self.df_vuelos['slot'] = 0

    def calcula_fecha_despegue(self, row) -> pd.Series:
        time_offset = self.tiempo_embarque_nat
        if row['tipo_vuelo'] == 'INTERNAT':
            time_offset = self.tiempo_embarque_internat

        retraso = 0

        if row['retraso'] != '-':
            tmp = pd.to_datetime(row['retraso'])
            retraso = (tmp.second + tmp.minute * 60)

        row['fecha_despegue'] = row['fecha_llegada'] + pd.Timedelta(minutes=time_offset) + pd.Timedelta(seconds=retraso)
        return row

    def encuentra_slot(self, fecha_vuelo) -> int:
        slot = -1
        for id in self.slots:
            time = self.slots[id].slot_esta_libre_fecha_determinada(fecha_vuelo)

            if time == 0:
                return id
        return slot

    def asigna_slot(self, vuelo) -> pd.Series:
        slot = -1
        fecha_vuelo = vuelo['fecha_llegada']

        while slot == -1:
            vuelo['fecha_llegada'] = fecha_vuelo
            slot = self.encuentra_slot(vuelo['fecha_llegada'])
            fecha_vuelo = fecha_vuelo + datetime.timedelta(minutes=10)

        vuelo = self.calcula_fecha_despegue(vuelo)
        self.slots[slot].asigna_vuelo(vuelo['id'], vuelo['fecha_llegada'], vuelo['fecha_despegue'])

        print(f'El vuelo {vuelo["id"]} con fecha de llegada y despegue {vuelo["fecha_llegada"]}, {vuelo["fecha_despegue"]} ha sido asignado al slot {slot}')

        vuelo['slot'] = slot
        return vuelo

    def asigna_slots(self):
        self.df_vuelos.sort_values(by=['fecha_llegada'], inplace=True)
        while len(self.df_vuelos) > 0:
            df_i = self.df_vuelos.iloc[0: self.n_slots, :]
            df_i = df_i.apply(lambda vuelo: self.asigna_slot(vuelo), axis=1)
            self.df_vuelos = self.df_vuelos.iloc[self.n_slots:, :]










