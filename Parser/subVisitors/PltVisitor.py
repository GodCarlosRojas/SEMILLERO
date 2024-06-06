from LabeledExprVisitor import LabeledExprVisitor
from LabeledExprParser import LabeledExprParser
import matplotlib.pyplot as plt # Graficas PLOT, SCATTER, BAR
import sympy as sp              # Grafica de funciones
import seaborn as sns           # Grafica heatmap

# Clase para interpretar acciones con plt, sp y sns
class PltVisitor(LabeledExprVisitor):
    
    # Constructor
    # Parametros: Clase compartida 'MyVisitor'
    def __init__(self, MainVisitor):
        self.main_visitor = MainVisitor
        
        # Diccionario propio de la clase para relaizar operaciones con plt
        self.plt_operations = {LabeledExprParser.SCATTER: plt.scatter,
                  	           LabeledExprParser.PLOT: plt.plot,
                  	           LabeledExprParser.BAR: plt.bar}
                  	           
    # Identifica si se desea graficar con plt (plot, bar, scatter)
    # Retorna: Se muestra la grafica pero retorna None (nada)
    # Errores: Erros si los datos a graficar no existen
    def visitPlot(self, ctx):
        try:
            name = ctx.getChild(2).getText()
            name_x = ctx.getChild(4).getText()
            name_y = ctx.getChild(6).getText()
            
            if name_x.isdigit():
               name_x = int(name_x)
            if name_y.isdigit():
               name_y = int(name_y)
               
            x = self.main_visitor.memory[name][name_x]
            y = self.main_visitor.memory[name][name_y]
            
            funct_select = self.plt_operations.get(ctx.fun.type,None)
            funct_select(x,y)
             
            plt.xlabel(name_x)
            plt.ylabel(name_y)
            titulo = f"Gráfico {name_x} vs {name_y}"
            plt.title(titulo)
            plt.grid(True)
            plt.show()   
            
            return None
        except Exception as e:
            id_symbol = ctx.getChild(2).getSymbol()
            self.main_visitor.errorPosition(id_symbol,f"Error: {e}")
        
    # Identifica si se desea graficar con sns (heatmap)
    # Retorna: Se muestra la grafica pero retorna None (nada)
    # Errores: Erros si los datos a graficar no existen
    def visitSns(self, ctx):
        try:
            name = ctx.ID().getText()
            sns.heatmap(self.main_visitor.memory[name], cmap='viridis')
            plt.grid(True)
            plt.show()   
            return None
        except Exception as e: 
            id_symbol = ctx.ID().getSymbol()
            self.main_visitor.errorPosition(id_symbol,f"Error: {e}")
    
    # Identifica si se desea graficar una funcion matematica
    # Retorna: Se muestra la grafica pero retorna None (nada)
    # Errores: - Error si la funcion esta mal planteada
    #          - ERror inesperado
    def visitDraw_fun(self, ctx):
        # Importacion perezosa de numpy para calculos locales
        import numpy as np
        x = sp.symbols('x')
        funcion = ctx.expr().getText()
        expresion = funcion.lower()
        num1 = int(ctx.NUMBER(0).getText())
        num2 = int(ctx.NUMBER(1).getText())
        num3 = int(ctx.NUMBER(2).getText())
        rango_x = np.linspace(num1, num2, num3)
        f = sp.lambdify(x, expresion, 'numpy')
        valores_y = f(rango_x)

        plt.plot(rango_x, valores_y)
        plt.title('Gráfica de '+ expresion)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid()
        plt.show()

        return None 
