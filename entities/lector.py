import os
import pandas as pd
import json

class Lector:
    def __init__(self, path: str):
        self.path = path

    def _comprueba_extension(self, extension):
        name, extension_ar = os.path.splitext(self.path)
        if extension_ar == extension:
            return True
        raise Exception("La extension no es correcta")

    def lee_archivo(self):
        pass

    @staticmethod
    def convierte_dict_a_csv(data: dict):
        df = pd.DataFrame(data)
        return df


class LectorCSV(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self, datetime_columns=[]):
        df = None
        if super()._comprueba_extension('.csv'):
            df = pd.read_csv(self.path)
            for column in datetime_columns:
                if column in df:
                    df[column] = pd.to_datetime(df[column])
                else:
                    raise Exception(f'La columna {column} no existe en el dataframe pasado como argumento.')
        return df


class LectorJSON(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self):
        data = None
        if super()._comprueba_extension('.json'):
            with open(self.path, 'r') as file:
                data = json.load(file)
        return [{k: v.strip() if isinstance(v, str) else v for k, v in item.items()} for item in data]

class LectorTXT(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self):
        data = []
        if super()._comprueba_extension('.txt'):
            with open(self.path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            header = lines[0].replace('\n', '').split(',')
            lines = lines[1:]

            for line in lines:
                line = line.replace('\n', '').split(',')
                if len(line) == len(header):
                    v_dict = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in zip(header, line)}
                    v_dict['destino'] = v_dict['destino'].replace(' ', '')
                    data.append(v_dict)
                else:
                    raise Exception('El número de columnas no coincide con el encabezado.')

        return data










