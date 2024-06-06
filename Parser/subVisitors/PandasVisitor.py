from LabeledExprVisitor import LabeledExprVisitor
from LabeledExprParser import LabeledExprParser
import pandas as pd #Para abrir ficheros (open txt) y operaciones con dataframes

# Clase para interpretar acciones con pandas
class PandasVisitor(LabeledExprVisitor):
    
    # Constructor
    # Parametros: Clase compartida 'MyVisitor'
    def __init__(self, MainVisitor):
        self.main_visitor = MainVisitor
        # Diccionario propio de la clase para relaizar operaciones con pandas de manera funcional
        self.dataframe_operations = {'select_column_index': lambda df , column_index: df.iloc[:, int(column_index)],
                                     'select_column_name': lambda df , column_name: df[column_name]}
                                     
    # Identifica si se desea castear una LIST (arreglo / matriz) a un DataFrame 
    # Retorna: un DataFrame con los valores correspondientes
    # Errores: Erros si se ingresa un numero y no una LIST (ej: DATA_FRAME([1]) | Correcto
    #                                                           DATA_FRAME(1)   | Incorrecto)
    def visitCast_to_DataFrame(self,ctx):
        try:
            value = self.main_visitor.visit(ctx.expr())
            return pd.DataFrame(value)
        except Exception as e:
            id_symbol = ctx.expr().start
            self.main_visitor.errorPosition(id_symbol,f"Error con '{ctx.expr().getText()}': No se ingreso un valor esperado")
    
    # Identifica si se desea leer un archivo csv 
    # Retorna: un DataFrame con los valores del archivo
    # Errores:  - Erros si no se encuentra el archivo
    #           - Error si hay un fallo al leer el archivo
    #           - Error si no es un archivo csv
    #           - Error si tiene o no cabecera y se indica lo contrario
    def visitRead_df(self, ctx):
        try:
           value_header = 0 if ctx.getChildCount() > 4 else None
           name_txt = ctx.ID().getText()
           df = pd.read_csv(name_txt,header=value_header)
           return df
        except FileNotFoundError:
            id_symbol = ctx.ID().getSymbol()
            self.main_visitor.errorPosition(id_symbol,f"Error con '{ctx.ID().getText()}': Archivo no encontrado")
        except Exception as e:
            id_symbol = ctx.ID().getSymbol()
            self.main_visitor.errorPosition(id_symbol,f"Error con '{ctx.ID().getText()}': {e}")
    
    # Identifica si se desea seleccionar una columna de un DataFrame
    # Retorna: un nuevo DataFrame solo con el valor de la columna especificada
    # Errores: Erros si el DataFrame no contiene la columna señalada 
    #          (no existe la columna con X nombre o fuera de indice)
    def visitSelect_column(self, ctx):
        try:
            # ID del dataframe en el diccionario
            name = ctx.getChild(2).getText()
            # Numero o nombre de la columna
            value_column = ctx.getChild(4).getText()
            if value_column.isdigit():
                # Busca funcion lambda en el diccionario local
                lambda_function = self.dataframe_operations['select_column_index']
                # Retorna el resultado de la funcion lambda
                return lambda_function(self.main_visitor.memory[name], value_column)
            else:
                # Busca funcion lambda en el diccionario local
                lambda_function = self.dataframe_operations['select_column_name']
                # Retorna el resultado de la funcion lambda
                return lambda_function(self.main_visitor.memory[name], value_column)
        except Exception as e: 
            id_symbol = ctx.getChild(2).getSymbol()
            self.main_visitor.errorPosition(id_symbol,f"Error: {e}")
    
    # Identifica si se desea concatenar 2 DataFrames
    # Retorna: un nuevo DataFrame con los valores correspondientes a la union
    # Errores: - Error si se ingresa un DataFrame que no existe
    #          - Error si se ingresa un dato que no es un DataFrame
    def visitConcat_column(self, ctx):
        try:
            data_frame_1 = ctx.ID(0).getText()
            data_frame_2 = ctx.ID(1).getText()
            df1 = self.main_visitor.memory[data_frame_1]
            df2 = self.main_visitor.memory[data_frame_2]
            return pd.concat([df1, df2], axis=1)
        except Exception as e: 
            id_symbol = ctx.ID(0).getSymbol()
            self.main_visitor.errorPosition(id_symbol,f"Error: Revise los parametros de CONCAT_COLUMN")
    
    # Identifica si se desea escribir algun resultado / valor en un archivo (txt). Si el archivo no existe se crea
    # Retorna: None (nada)
    # Errores: - Error si se ingresa una variable que no existe
    #          - Error si el archivo donde se desea escribir los datos no existe
    def visitWrite(self, ctx):
        try:
            name_archivo = ctx.ID(0).getText()
            data = ctx.ID(1).getText()
            header_value = True if ctx.getChildCount() > 6 else False

            df = pd.DataFrame(self.main_visitor.memory[data])
            df.to_csv(name_archivo, index=False, header=header_value)
            return None
        except Exception as e: 
            id_symbol = ctx.ID(0).getSymbol()
            self.main_visitor.errorPosition(id_symbol,f"'Error: {e}")
            
            
    # Identifica si se desea eliminar una columna de un DataFrame
    # Retorna: Un nuevo DataFrame con la columna eliminada
    # Errores: - Error si el DataFrame no existe
    #          - Error si la columna a eliminar no existe o esta fuera de indice
    def visitDrop(self,ctx): 
        try:
            name = ctx.ID(0).getText()
            data = self.main_visitor.memory[name]
            column_string = ctx.getChild(4).getText()
            
            if column_string.isdigit():
                indice = int(column_string)
                return data.drop(data.columns[indice], axis=1, inplace=False)
            else: 
                return data.drop(column_string, axis=1, inplace=False)
        except Exception as e:
            id_symbol = ctx.ID(0).getSymbol()
            self.main_visitor.errorPosition(id_symbol,f"Error: {e}")
    
    # Identifica si se desea rellenar los datos nulos de un DataFrame con el valor promedio de cado columna
    # Retorna: Un nuevo DataFrame con los nuevos datos
    # Errores: - Error si el DataFrame no existe
    #          - Error si el DataFrame contiene cadenas (str)
    def visitFillna(self,ctx):
        try:
            name = ctx.ID().getText()
            data = self.main_visitor.memory[name]
            return data.fillna(data.mean(numeric_only=True), inplace=False)
        except Exception as e:
            id_symbol = ctx.ID().getSymbol()
            self.main_visitor.errorPosition(id_symbol,f"Error: {e}")
    
    # Identifica si se desea normalizar los datos de un DataFrame
    # Retorna: Un nuevo DataFrame con los datos normalizados
    # Errores: - Error si el DataFrame no existe
    #          - Error si el DataFrame contiene cadenas (str)
    def visitNorm(self,ctx):
        try:
            name = ctx.ID().getText()
            data = self.main_visitor.memory[name]
            return (data - data.min()) / (data.max() - data.min())
        except Exception as e:
            id_symbol = ctx.ID().getSymbol()
            self.main_visitor.errorPosition(id_symbol,f"Error: {e}")

