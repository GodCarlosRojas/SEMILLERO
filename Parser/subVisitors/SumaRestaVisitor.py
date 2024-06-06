from LabeledExprVisitor import LabeledExprVisitor
from LabeledExprParser import LabeledExprParser

# Clase para interpretar operaciones aritmeticas basicas 
class SumaRestaVisitor(LabeledExprVisitor):
    
    # Constructor
    # Parametros: Clase compartida 'MyVisitor'
    def __init__(self, MainVisitor):
        self.main_visitor = MainVisitor
        
        # Diccionario propio de la clase para relaizar operaciones artimeticas
        self.math_operations = {LabeledExprParser.ADD: lambda x, y: x + y,
                  	       LabeledExprParser.SUB: lambda x, y: x - y,
                  	       LabeledExprParser.POT: lambda x, y: x ** y,
                  	       LabeledExprParser.MOD: lambda x, y: x % y,
                  	       LabeledExprParser.MUL: lambda x, y: x * y,
                  	       LabeledExprParser.DIV: lambda x,y: x / y,
                  	       LabeledExprParser.MATRIXMUL: lambda x,y: x @ y}  
                  	       
    # Identifica si se desea realizar una multiplicacion, division, potenciacion o modulo
    # Retorna: el resultado de la operacion matematica
    # Errores: Error si matematicamente no se puede realizar la operacion (ej: dividir por 0 o multiplicacion 
    #                                                                          elemento a elemento de matrices donde
    #                                                                          sus dimensiones no lo permitan)
    def visitMulDiv(self, ctx):
        left = self.main_visitor.visit(ctx.expr(0))
        right = self.main_visitor.visit(ctx.expr(1))
        try:
            return self.math_operations.get(ctx.op.type,None)(left, right)
        except Exception as e:
            id_symbol = ctx.expr(0).start 
            self.main_visitor.errorPosition(id_symbol,f"Error con: \n'{left}'\n\n'{right}'\n {e}")
        
    # Identifica si se desea realizar una operacion aritmetica
    # Retorna: el resultado de la operacion matematica
    # Errores: Error inesperado
    def visitAddSub(self, ctx):
        left = self.main_visitor.visit(ctx.expr(0))
        right = self.main_visitor.visit(ctx.expr(1))
        try:
            return self.math_operations.get(ctx.op.type,None)(left, right)
        except Exception as e:
            id_symbol = ctx.expr(0).start 
            self.main_visitor.errorPosition(id_symbol,f"Error con: \n'{left}'\n\n'{right}'\n {e}")
    
    # Identifica si se desea realizar una multiplicacion de matrices
    # Retorna: el resultado de la operacion matematica
    # Errores: - Error si las dimensiones de las matrices no permiten la operacion
    #          - Error si los datos de entrada no son matrices
    def visitMatrixMul(self, ctx):
        left = self.main_visitor.visit(ctx.expr(0))
        right = self.main_visitor.visit(ctx.expr(1))
        try:
            return self.math_operations.get(LabeledExprParser.MATRIXMUL,None)(left, right)
        except Exception as e:
            id_symbol = ctx.expr(0).start 
            self.main_visitor.errorPosition(id_symbol,f"Error con: \n'{left}'\n\n'{right}'\n {e}")
