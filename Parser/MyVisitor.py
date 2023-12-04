from LabeledExprVisitor import LabeledExprVisitor
from LabeledExprParser import LabeledExprParser
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import importlib


class MyVisitor(LabeledExprVisitor):
    def __init__(self):
        self.memory = {}
        self.aux = 0

    def visitAssign(self, ctx):
        name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.memory[name] = value
        return value
   
    def visitList(self, ctx):
        return eval(ctx.getChild(0).getText())

    def visitPrint(self, ctx):
        value = self.visit(ctx.expr())
        print(value)
        return 0

    def visitInt(self, ctx):
        return ctx.INT().getText()

    def visitId(self, ctx):
        name = ctx.ID().getText()
        if name in self.memory:
            return self.memory[name]
        return 1
        
    def visitParens(self, ctx):
        return self.visit(ctx.expr())

    def visitAddSub(self, ctx):
    
       left = self.visit(ctx.expr(0))
       right = self.visit(ctx.expr(1))

       left, right = self.tipo(left,right)
       operations = {LabeledExprParser.ADD: lambda x, y: x + y,
          	     LabeledExprParser.SUB: lambda x, y: x - y,
          	     LabeledExprParser.POT: lambda x, y: x ** y,
          	     LabeledExprParser.MOD: lambda x, y: x % y,
          	     LabeledExprParser.MUL: lambda x, y: x * y,
          	     LabeledExprParser.DIV: lambda x,y: x / y}
	
       return operations.get(ctx.op.type,None)(left, right)
        
    def visitFuncs(self, ctx):
       num = self.visit(ctx.expr())
       
       if isinstance(num,list):
          num = np.array(num)
       elif isinstance(num,str):
          num = float(num)
       
       if ctx.fun.type == LabeledExprParser.SQRT:
           return np.sqrt(num)
           
       arg = np.radians(num)
       
       if ctx.fun.type == LabeledExprParser.SIN:
           return np.sin(arg)
       elif ctx.fun.type == LabeledExprParser.COS:
           return np.cos(arg)
       else:
          return np.tan(arg)
        
    def visitMat(self, ctx):
       num = self.visit(ctx.expr())
       if isinstance(num,list):
          num = np.array(num)
       
       if ctx.fun.type==LabeledExprParser.INV:
          return np.linalg.inv(num) 
       else:
          return num.T
        
    def tipo(self,left,right):
        
       if isinstance(left, list):
          left = np.array(left)
       elif isinstance(left, str):
          left = float(left)
          
       if isinstance(right, list):
          right = np.array(right)
       elif isinstance(right, str):
          right = float(right)
          
       return left, right
        
    def visitCondition(self, ctx):
       left = self.visit(ctx.expr(0))
       operator = ctx.fun.text 
       right = self.visit(ctx.expr(1))
       
       condicion = eval(f"{left} {operator} {right}")
       
       i = 0
       for block_ctx in ctx.block():
        if i==0 and condicion:
         self.visit(block_ctx)
        elif i==1 and condicion==False:
         self.visit(block_ctx)
        i+=1
           
       return None

    def visitFor(self, ctx):
        start = int(self.visit(ctx.expr(0)))
        stop = int(self.visit(ctx.expr(1)))
        step = int(self.visit(ctx.expr(2)))
        
        for i in range(start,stop,step):
             self.visit(ctx.block())
           
        return None
        
    def visitDataFrame(self, ctx):
        
        value = None
        if ctx.getChild(4) is not None:
           value = 0
           
        try:
           direccion = ctx.ID().getText()
           df = pd.read_csv(direccion,header=value)
           return df
        except FileNotFoundError:
           print("El archivo no se encontró.")
           return None
        except Exception as e:
           print("Error al leer el archivo:", str(e))
           return None
           

    def visitWrite(self, ctx):
    	
    	name_archivo = ctx.ID(0).getText()
    	
    	if ctx.ID(1).getText() in self.memory:
    	   df = self.memory[ctx.ID(1).getText()]
    	   df.to_csv(name_archivo, index=False, header=False)
    	return None
    
    def visitDef(self,ctx):
    	
        with open('metodosUser.py', 'a') as archivo:
           archivo.write(ctx.getText()+'\n')
        self.metodosUser = importlib.reload(self.metodosUser)
        print(getattr(self.metodosUser, ctx.getID(0))(3, 4))
        return None 
    
    def visitDfaction(self,ctx):
        name = ctx.ID().getText()
        
        if name in self.memory:
           self.aux = name
           self.visit(ctx.action())
        else:
           print("No se ha declarado ",name)
        
        return None
    
    def visitDrop(self,ctx):
        name = self.aux
        if ctx.getChild(2).getText().isdigit():
           columna = int(ctx.getChild(2).getText())
        else:
           columna = ctx.getChild(2).getText()
        
        action = ctx.getChild(0).getText()
        
        if action == "DROP":
           self.memory[name].drop(columna,axis=1, inplace=True)
        elif action == "MEAN":
           print(self.memory[name][columna].mean())
        elif action == "MIN":
           print(self.memory[name][columna].min())
        elif action == "MAX":
           print(self.memory[name][columna].max())
        elif action == "FILLNA":
           self.memory[name].fillna(self.memory[name][columna].mean(), inplace=True)
        else:
           print("Accion no reconocidad")
           
        return None
    
    def visitNorm(self,ctx):
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        name = self.aux
        datos_normalizados = scaler.fit_transform(self.memory[name])
        df_normalizado = pd.DataFrame(datos_normalizados, columns=self.memory[name].columns)
        self.memory[name] = df_normalizado
        return None 
    
    def visitGraf(self,ctx):
        name = ctx.ID().getText()
        
        if name in self.memory:
           self.aux = name
           self.visit(ctx.plt())
        else:
           print("No se ha declarado ",name)
        
        return None
    
    def visitPlot(self, ctx):
        import matplotlib.pyplot as plt
        name = self.aux
        name_x = ctx.getChild(2).getText()
        name_y = ctx.getChild(4).getText()
        
        if name_x.isdigit():
           name_x = int(name_x)
        if name_y.isdigit():
           name_y = int(name_y)
           
        x = self.memory[name][name_x]
        y = self.memory[name][name_y]
        
        if ctx.getChild(0).getText() == 'PLOT':
           plt.plot(x,y, marker='o')
        elif ctx.getChild(0).getText() == 'BAR':
           plt.bar(x,y)
        elif ctx.getChild(0).getText() == 'SCATTER':
           plt.scatter(x,y)
        else:
           print("No se identifico la accion")
           return None  
        
        plt.xlabel(name_x)
        plt.ylabel(name_y)
        titulo = f"Gráfico {name_x} vs {name_y}"
        plt.title(titulo)
        plt.grid(True)
        plt.show()   
        
        return None
        
    def visitSns(self, ctx):
        import matplotlib.pyplot as plt
        import seaborn as sns
        name = self.aux
        sns.heatmap(self.memory[name], cmap='viridis')
        plt.grid(True)
        plt.show()   
        
        return None
    
