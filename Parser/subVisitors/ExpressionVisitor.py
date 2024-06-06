from LabeledExprVisitor import LabeledExprVisitor
from LabeledExprParser import LabeledExprParser

# Clase para interpretar expresiones 
class ExpressionVisitor(LabeledExprVisitor):
    
    # Constructor
    # Parametros: Clase compartida 'MyVisitor'
    def __init__(self, MainVisitor):
        self.main_visitor = MainVisitor
    
    # Imprime una expresion (expr)
    # Retorna: None (nada)
    def visitPrint(self, ctx):
        value = self.main_visitor.visit(ctx.expr())
        print(value)
        return None
    
    # Identifica una asignasion (ej: a=10) y la almacena en el diccionario (memory) 
    # de la case compartida ('MyVisitor')
    # Retorna: El valor asignado  
    def visitAssign(self, ctx):
        name = ctx.ID().getText()
        value = self.main_visitor.visit(ctx.value())
        self.main_visitor.memory[name] = value
        return value
    
    # Identifica cadena (str) como numero (float)
    # Retorna: Numero tipo float
    def visitNumber(self, ctx):
        if ctx.getChild(0).getText() == '-':
            return float('-' + ctx.NUMBER().getText())
        else:
            return float(ctx.NUMBER().getText())
    
    # Identifica si un identificador (variable) existe en el diccionario (memory) 
    # de la case compartida ('MyVisitor')
    # Retorna: El valor asignado al identificador
    # Errores: Erros si no existe el identificador en el diccionario
    def visitId(self, ctx):        
        try:
            name = ctx.ID().getText()
            return self.main_visitor.memory[name]
        except KeyError:
            id_symbol = ctx.ID().getSymbol()
            self.main_visitor.errorPosition(id_symbol,f"'{name}' no existe")
    
    # Identifica los valores para realizar un condicional (if)
    # Retorna: None (nada)
    # Error: Error si el condicional no es logico o ambiguo (ej: comparar una lista; lista_1 > lista_2) 
    def visitCondition(self, ctx):
    
        left = self.main_visitor.visit(ctx.expr(0))
        operator = ctx.fun.text 
        right = self.main_visitor.visit(ctx.expr(1))
        try:
            condicion = eval(f"{left} {operator} {right}")

            if condicion:
                self.main_visitor.visit(ctx.block()[0])
            else:
                self.main_visitor.visit(ctx.block()[1])

            return None
        except Exception as e:
            id_symbol = ctx.expr(0).start 
            self.main_visitor.errorPosition(id_symbol,f"Error: {left} {operator} {right} \n" + 
                                                      "No es posible realizar condicionales con listas o dataframes, es ambiguo")
    
    # Identifica los valores para realizar un bucle (for)
    # Retorna: None (nada)
    # Error: Error si los parametros del bucle no son numeros enteros
    def visitFork(self, ctx):
        # Valores tipo float
        start = self.main_visitor.visit(ctx.expr(0))
        stop = self.main_visitor.visit(ctx.expr(1))
        step = self.main_visitor.visit(ctx.expr(2))
        
        try:
            # Verificar si son valores enteros y no float (ej: 4.0 == 4 | 4.1 != 4)
            start = int(start) if start == int(start) else start
            stop = int(stop) if stop == int(stop) else stop
            step = int(step) if step == int(step) else step
            for i in range(start,stop,step):
                 self.main_visitor.visit(ctx.block())
            return None
        except Exception as e:
            id_symbol = ctx.expr(0).start 
            self.main_visitor.errorPosition(id_symbol,f"Error inesperado: {e}")
