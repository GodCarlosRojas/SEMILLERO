# SEMILLERO - PARSER sobre Python
## Lista de Integrantes

- Steven Sebastián Flórdio Páez
- Luis Ángel Rodríguez Calderón
- Carlos Andrés Rojas Rocha


## ¡Bienvenido!

Este es el repositorio donde se encuentra nuestro parser. A continuacion te daremos una breve explicacion del contenido:

Carpeta Parser: Aqui se encuentran todos los archivos necesarios para ejecutar el proyecto
Parser/calc.py: Clase main 
Parser/LabeledExpr.g4: Gramatica
Parser/MyVisitor.py: Analisador semantico
Parser/open: archivo.csv (ejemplo)
Parser/t.expr: Archivo entrada con instrucciones (ejemplo)

Capeta Ejemplos: Aqui se encuentran algunos ejemplos de que cosas puede hacer nuestra gramatica.




En otras palabras, el contenido de la carpeta "Parser" es el proyecto. Para ejecutar los archivos ejemplo que estan en la carpeta debes seguir los siguientes pasos:

1. Instalar python
2. Istalar Antlr4
3. Descargar la carpeta "Parser"
4. Abrir una consola en la direccion de la capeta
5. Ingresar en la consola: antlr4 -Dlanguage=Python3 LabeledExpr.g4 -visitor
6. Ingresar en la consola: python3 calc.py t.expr

Cabe resaltar que si deseas ejecutar el proyecto con otro archivo que no sea "t.expr" lo puedes hacer, este solo es un pequeño ejemplo que decidimos incluir en la carpeta para que verificaras si todo esta funcionando correctamente al descargarlo.
