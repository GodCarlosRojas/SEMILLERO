from LabeledExprVisitor import LabeledExprVisitor
from LabeledExprParser import LabeledExprParser
import numpy as np #Para manejo de matrices (listas), operaciones trigonometricas y matriciales

# Clase para interpretar acciones con numpy 
class NumpyVisitor(LabeledExprVisitor):
    
    # Constructor
    # Parametros: Clase compartida 'MyVisitor'
    def __init__(self, MainVisitor):
        self.main_visitor = MainVisitor
        
        # Diccionario propio de la clase para relaizar operaciones con numpy
        self.numpy_operations = {LabeledExprParser.SQRT: np.sqrt,
                          	     LabeledExprParser.SIN: np.sin,
                          	     LabeledExprParser.COS: np.cos,
                          	     LabeledExprParser.TAN: np.tan,
                          	     LabeledExprParser.INV: np.linalg.inv,
                          	     LabeledExprParser.TRAS: np.transpose,
                          	     LabeledExprParser.MAX: np.max,
                          	     LabeledExprParser.MIN: np.min,
                          	     LabeledExprParser.MEAN: np.mean,
                          	     LabeledExprParser.SUM: np.sum}
    
    # Identifica si se ha ingresado un vector o una matriz (LIST) 
    # Retorna: un array de numpy con el contenido de LIST
    # Errores: Erros si se crea una matriz no valida (ej: [[1,2],
    #                                                      [3]]
    def visitList(self, ctx):
        try:
            lista = eval(ctx.getChild(0).getText())
            return np.array(lista)
        except Exception as e:
            id_symbol = ctx.LIST().getSymbol()
            self.main_visitor.errorPosition(id_symbol,f"Error con '{ctx.getChild(0).getText()}': {e}")
    
    # Identifica si se ha realizado un llamado al numero pi 
    # Retorna: el numero pi
    def visitPiNumber(self, ctx):
        return np.pi
    
    # Halla el maximo, minimo, promedio o sumatoria de un numero, LIST (arreglo o matriz) o DataFrame
    # Retorna: el valor hallado
    # Errores: Error si se ingresa un DataFrame con valores tipo string
    def visitMaxMinMeanSum(self, ctx):
        try:
            num = self.main_visitor.visit(ctx.expr())
            MaxMin_fun = self.numpy_operations.get(ctx.fun.type,None)
            return MaxMin_fun(num)
        except Exception as e:
            id_symbol = ctx.expr().start
            self.main_visitor.errorPosition(id_symbol,f"Error con '{ctx.getChild(0).getText()}': {e}")
        
    # Evalua en N funcion trigonometrica un numero, LIST (arreglo o matriz) o DataFrame
    # Retorna: el valor hallado
    # Errores: Error si se ingresa un DataFrame con valores tipo string
    def visitTrigonometricFuncs(self, ctx):
        try:
            num = self.main_visitor.visit(ctx.expr())
            if ctx.getChildCount() > 4:
                num = np.radians(num)
            trig_fun = self.numpy_operations.get(ctx.fun.type,None)
            return trig_fun(num)
        except Exception as e:
            id_symbol = ctx.expr().start
            self.main_visitor.errorPosition(id_symbol,f"Error con '{ctx.getChild(0).getText()}': {e}")
    
    # Evalua en N funcion matricial un LIST (arreglo o matriz) o DataFrame
    # Retorna: el valor hallado
    # Errores: Error si se ingresa un DataFrame con valores tipo string o si matematicamente no se puede realizar una
    #          operacion (ej: inversa de una matriz no cuadrada)
    def visitMatrixFuncs(self, ctx):
       mat = self.main_visitor.visit(ctx.expr())  
       try:
           mat_fun = self.numpy_operations.get(ctx.fun.type,None)
           return mat_fun(mat)
       except Exception as e:
           id_symbol = ctx.expr().start 
           self.main_visitor.errorPosition(id_symbol,f"Error con '{mat}': {e}")
