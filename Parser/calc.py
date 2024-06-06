import time
import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from LabeledExprLexer import LabeledExprLexer
from LabeledExprParser import LabeledExprParser
from MyVisitor import MyVisitor  
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import ParseCancellationException

#ErrorListener personalizado
class CustomErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_message = "Error de análisis sintáctico en línea {}, columna {}: {}".format(line, column, msg)
        self.errors.append(error_message)

    def hasErrors(self):
        return len(self.errors) > 0

    def getErrors(self):
        return self.errors
    
    def clearErrors(self):
        self.errors = []

if __name__ == '__main__':
    
    # Manejo de errores personalizado
    error_listener = CustomErrorListener()

    # Importa el visitor una sola vez
    visitor = MyVisitor()

    while True:
        if len(sys.argv) > 1:
            archivo = sys.argv[1]
        else:
            archivo = input("\nIngrese el nombre del archivo de instrucciones o escriba 'salir' para finalizar: ")

        if archivo.lower() == "salir":
            break

        # Procesa el archivo
        inicio = time.time()  # Medir tiempo
        try:
            input_stream = FileStream(archivo)
            lexer = LabeledExprLexer(input_stream)
            lexer.removeErrorListeners()             # Remover el listener de errores predeterminado
            lexer.addErrorListener(error_listener)   # Agregar el listener personalizado
            token_stream = CommonTokenStream(lexer)
            
            parser = LabeledExprParser(token_stream)
            parser.removeErrorListeners()            # Remover el listener de errores predeterminado
            parser.addErrorListener(error_listener)  # Agregar el listener personalizado

            tree = parser.prog()
            
            if not error_listener.hasErrors():
                visitor.visit(tree)
            else:
                for error in error_listener.getErrors():
                    print(error)
                error_listener.clearErrors()  # Vaciar la lista de errores después de imprimirlos
        
        except Exception as e:
            print("Error: ", e)
        finally:
            fin = time.time()  # Medir tiempo
            print("\nTiempo de ejecución:", fin - inicio)  # Medir tiempo

