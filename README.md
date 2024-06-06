# SEMILLERO - PARSER sobre Python
## Lista de Integrantes

- Steven Sebastián Flórdio Páez
- Luis Ángel Rodríguez Calderón
- Carlos Andrés Rojas Rocha


## ¡Bienvenido!

Este es el repositorio donde se encuentra nuestro parser. A continuacion te daremos una breve explicacion del contenido:

- Carpeta Parser: Aqui se encuentran todos los archivos necesarios para ejecutar el proyecto
- Parser/calc.py: Clase main 
- Parser/LabeledExpr.g4: Gramatica
- Parser/MyVisitor.py: Analizador semantico
- Parser/subVisitors/..: Subclases de MyVisitor especializadas en determinada tarea
- Parser/open: archivo.csv (ejemplo)
- Parser/t.expr: Archivo entrada con instrucciones (ejemplo)
- Carpeta Informe: Aqui detallamos paso a paso nuestro proceso para construir el Parser
- Capeta Ejemplos: Aqui se encuentran algunos ejemplos de que cosas puede hacer nuestra gramatica.


## Pasos para ejecutar el proyecto

Para ejecutar los archivos ejemplo que estan disponibles debes seguir los siguientes pasos:

1. Instalar python
2. Instalar las siguientes librerias de python: numpy, pandas, matplotlib, sympy y seaborn.
3. Istalar Antlr4 para python
4. Descargar la carpeta "Parser"
5. Abrir una consola en la direccion de la capeta
6. Ingresar en la consola: antlr4 -Dlanguage=Python3 LabeledExpr.g4 -visitor
7. Ingresar en la consola: python3 calc.py
8. Ingresar el nombre del archivo con las instrucciones (ej: t.expr)

Cabe resaltar que si deseas ejecutar el proyecto con otro archivo que no sea "t.expr" lo puedes hacer, este solo es un ejemplo que decidimos incluir en la carpeta para que verificaras si todo esta funcionando correctamente al descargarlo.


## ¡Un video para ti!

A continuacion te dejamos el link de un video hecho por nosotros para que observer paso a paso como ejecutar el proyecto:
