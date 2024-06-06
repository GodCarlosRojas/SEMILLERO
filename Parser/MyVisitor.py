from LabeledExprVisitor import LabeledExprVisitor
from LabeledExprParser import LabeledExprParser

#from name_archivo import nombre_clase
from subVisitors.ExpressionVisitor import ExpressionVisitor
from subVisitors.PandasVisitor import PandasVisitor
from subVisitors.NumpyVisitor import NumpyVisitor
from subVisitors.PltVisitor import PltVisitor
from subVisitors.SumaRestaVisitor import SumaRestaVisitor
from subVisitors.LambdaVisitor import LambdaVisitor

class MyVisitor(LabeledExprVisitor):
    
    def __init__(self):
        self.memory = {}
        self.expression_visitor = ExpressionVisitor(self)
        self.sumaresta_visitor = SumaRestaVisitor(self)
        self.pandas_visitor = PandasVisitor(self)
        self.lambda_visitor = LambdaVisitor(self)
        self.numpy_visitor = NumpyVisitor(self)
        self.plt_visitor = PltVisitor(self)     	     
          
           
    def errorPosition(self,id_symbol,menssage):
        print(f"Error en línea {id_symbol.line}, columna {id_symbol.column}")
        print(menssage)
        raise ValueError("Se detuvo el analisis por error logico o matematico")
        
    def visitPrint(self, ctx):
        return self.expression_visitor.visitPrint(ctx)

    def visitAssign(self, ctx):
        return self.expression_visitor.visitAssign(ctx)
    
    def visitMulDiv(self, ctx):
        return self.sumaresta_visitor.visitMulDiv(ctx)
    
    def visitAddSub(self, ctx):
        return self.sumaresta_visitor.visitAddSub(ctx)
    
    def visitMatrixMul(self, ctx):
        return self.sumaresta_visitor.visitMatrixMul(ctx)
       
    def visitNumber(self, ctx):
        return self.expression_visitor.visitNumber(ctx)
            
    def visitId(self, ctx):
        return self.expression_visitor.visitId(ctx)
    
    def visitPiNumber(self, ctx):
        return self.numpy_visitor.visitPiNumber(ctx)
            
    def visitImplementLambda(self,ctx):
    	return self.lambda_visitor.visitImplementLambda(ctx)
        
    def visitParens(self, ctx):
        return self.visit(ctx.expr())
        
    def visitList(self, ctx):
        return self.numpy_visitor.visitList(ctx)
    
    def visitMaxMinMeanSum(self, ctx):
        return self.numpy_visitor.visitMaxMinMeanSum(ctx)
    
    def visitTrigonometricFuncs(self, ctx):
        return self.numpy_visitor.visitTrigonometricFuncs(ctx)
        
    def visitMatrixFuncs(self, ctx):
        return self.numpy_visitor.visitMatrixFuncs(ctx)
    
    def visitCast_to_DataFrame(self,ctx):
        return self.pandas_visitor.visitCast_to_DataFrame(ctx)
    
    def visitRead_df(self, ctx):
        return self.pandas_visitor.visitRead_df(ctx)
    
    def visitSelect_column(self, ctx):
        return self.pandas_visitor.visitSelect_column(ctx)
    
    def visitConcat_column(self, ctx):
        return self.pandas_visitor.visitConcat_column(ctx)
        
    def visitCondition(self, ctx):
        return self.expression_visitor.visitCondition(ctx)

    def visitFork(self, ctx):
        return self.expression_visitor.visitFork(ctx)
        
    def visitWrite(self, ctx):
        return self.pandas_visitor.visitWrite(ctx)
    
    def visitDef_lambda(self,ctx):
        return self.lambda_visitor.visitDef_lambda(ctx)
    
    def visitDrop(self,ctx): 
        return self.pandas_visitor.visitDrop(ctx)
    
    def visitFillna(self,ctx):
        return self.pandas_visitor.visitFillna(ctx)
        
    def visitNorm(self,ctx):
        return self.pandas_visitor.visitNorm(ctx)
       
    def visitPlot(self, ctx):
        return self.plt_visitor.visitPlot(ctx)
        
    def visitSns(self, ctx):
        return self.plt_visitor.visitSns(ctx)
            
    def visitDraw_fun(self, ctx):
    	return self.plt_visitor.visitDraw_fun(ctx)
    
