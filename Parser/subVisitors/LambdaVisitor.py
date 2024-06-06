from LabeledExprVisitor import LabeledExprVisitor
from LabeledExprParser import LabeledExprParser

# Clase para interpretar funciones lambda
class LambdaVisitor(LabeledExprVisitor):
    
    # Constructor
    # Parametros: Clase compartida 'MyVisitor'
    def __init__(self, MainVisitor):
        self.main_visitor = MainVisitor
    
    # Identifica si se esta implementando una funcion lambda previamente definida
    # Retorna: El resultado de la implementacion
    # Errores: Erros si existe un calculo inadecuado (ej: lambda x:x/0) u otra excepcion (ej: suma = lambda x:x+1
    #                                                                                         suma(2,3) 
    #                                                                                         Define 1 parametro pero
    #                                                                                         envia 2)
    def visitImplementLambda(self,ctx):
        try:
            nombre_fun = ctx.ID().getText()
            parametros = ctx.expr()
            parametros_numericos = []

            #Recorrer las expresiones (expr) para hallar su valor numerico
            for p in parametros:
                value_parametro_n = self.main_visitor.visit(p)
                parametros_numericos.append(value_parametro_n)
            resultado = self.main_visitor.memory[nombre_fun](*parametros_numericos)  
            return resultado
        except Exception as e:
            id_symbol = ctx.ID().getSymbol() 
            self.main_visitor.errorPosition(id_symbol,f"Error inesperado: {e}")
    
    # Identifica si se esta definiendo una funcion lambda
    # Retorna: La funcion lambda consturida
    def visitDef_lambda(self,ctx):
        lambda_value = eval(ctx.getText())
        return lambda_value
