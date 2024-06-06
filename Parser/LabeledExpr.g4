// Grammar: LabeledExpr.g4
// Autores: Steven Sebastian Florido Paez, Carlos Andres Rojas Rocha, Luis Angel Rodriguez Calderon
// Descripción: Esta gramática define las reglas para nuestro parser 


// Gramatica
grammar LabeledExpr;

/* prog: Regla base a partir de la cual se generan todas las otras reglas. 
 * Esta regla define el punto de entrada del programa, que consiste en una secuencia de instrucciones.
 * Las instrucciones pueden ser:
 * - `stat`: Instrucciones de declaración o asignación.
 * - `write`: Instrucciones de escritura de archivos.
 * - `condition`: Instrucciones condicionales (if/else).
 * - `fork`: Instrucciones con bucles.
 * - `plt_data`: Instrucciones para la generación de gráficos de conjuntos de datos.
 * - `draw_fun`: Instrucciones para la generación de gráficos de funciones matematicas.
 */
prog:   (stat | write | condition | fork | plt_data | draw_fun)+;

/*stat: Define las diferentes declaraciones que pueden aparecer en el programa.
 * Las declaraciones pueden ser:
 * - `expr NEWLINE`: Una expresión que termina en una nueva línea (impresión de la expresión).
 * - `ID '=' value NEWLINE`: Asignación de un valor a una variable.
 * - `NEWLINE`: Una línea en blanco.
 */
stat:   expr NEWLINE               		# print
    |   ID '=' value NEWLINE			# assign
    |   NEWLINE		               	   	# blank
    ;

/* expr: Define las posibles expresiones aritméticas y funciones.
 * Las expresiones pueden incluir operaciones aritméticas, números, identificadores, funciones lambda, 
 * listas, y varias funciones matemáticas y de manipulación de datos.
 */
expr:   expr op=('*'|'/'|'^'|'%') expr      			        # MulDiv
    |   expr op=('+'|'-') expr      			                # AddSub
    |   expr '@' expr              		                        # MatrixMul
    |   '-'? NUMBER                         				# Number
    |   ID                          					# Id
    |	'pi'								# PiNumber
    |   ID '(' expr (',' expr)* ')'  					# ImplementLambda	
    |   '(' expr ')'                					# Parens
    |   LIST                        					# List
    |   fun=('MAX'|'MIN'|'MEAN'|'SUM') '(' expr ')'			# MaxMinMeanSum
    |   fun=('SIN'|'COS'|'TAN'|'SQRT') '(' expr (',' 'Radians')? ')'	# TrigonometricFuncs
    |   fun=('INV'|'TRAS') '(' expr ')'                 		# MatrixFuncs  
    |   'DATA_FRAME' '(' expr ')' 					# Cast_to_DataFrame 
    ;
    
/* value: Define los diferentes tipos de valores que pueden ser asignados o manipulados.
 * Los valores pueden ser una expresión, una definición de función lambda, la lectura de un DataFrame,
 * la selección de una columna, la concatenación de columnas o una acción sobre datos.
 */
value: expr | def_lambda | read_df | select_column | concat_column | data_action;

// def_lambda: Define una función lambda.
def_lambda: 'lambda ' (ID (',' ID)*)? ':' (ID|NUMBER) (op=('*'|'/'|'+'|'-'|'^'|'%') (ID|NUMBER))* (fun=('=='|'!='|'<'|'>'|'<='|'>=') NUMBER)?;

//*********** OPERACIONES QUE SOLO ACEPTAN DATAFRAMES COMO PARAMETROS *********** 

// read_df: Define la lectura de un DataFrame desde un archivo formato csv.
// Ejemplo1: READ '(' Name_dataframe, Header ')'
// Ejemplo2: READ '(' Name_dataframe ')'
read_df: 'READ' '(' ID (',' 'Header')? ')';

// select_column: Define la selección de una columna de un DataFrame.
// Ejemplo: SELECT_COLUMN '(' Name_dataframe, column_or_index ')'
select_column: 'SELECT_COLUMN' '(' ID ',' (ID|NUMBER) ')';

// concat_column: Define la concatenación de dos columnas en un DataFrame.
// Ejemplo: CONCAT_COLUMN '(' Name_dataframe1, Name_dataframe2 ')'
concat_column: 'CONCAT_COLUMN' '(' ID ',' ID ')';

/* data_action: Define varias acciones que pueden realizarse sobre un DataFrame.
 * Las acciones pueden incluir:
 * - `DROP`: Eliminar una columna.
 * - `FILLNA`: Rellenar valores nulos.
 * - `NORM`: Normalizar datos.
 */
data_action:   'DROP' '(' ID ',' (NUMBER|ID) ')'			# Drop
	   |   'FILLNA' '(' ID ')'					# Fillna
      	   |   'NORM' '(' ID ')'					# Norm
	   ;
	  
//*********** FIN OPERACIONES CON DATAFRAMES ***********

// write: Define la escritura de un conjunto de datos en un archivo .
// Ejemplo1: WRITE '(' name_archivo, name_datos, Header ')'
// Ejemplo1: WRITE '(' name_archivo, name_datos ')'
write: 'WRITE' '(' ID ',' ID (',' 'Header')? ')';

// condition: Define una estructura condicional (if/else).
condition: 'if' expr fun=('=='|'!='|'<'|'>'|'<='|'>=') expr '{' block '}' (NEWLINE 'else' '{' block '}' )? NEWLINE+;

// fork: Define un bucle `for` con un rango y un bloque de instrucciones.
fork: 'for' '(' expr ',' expr ',' expr ')' '{' block '}';

// block: Define un bloque de código que puede contener múltiples declaraciones.
block: NEWLINE  (prog);

/* plt_data: Define funciones de visualización de datos.
 * Las funciones pueden ser:
 * - `SCATTER`: Gráfico de dispersión.
 * - `BAR`: Gráfico de barras.
 * - `PLOT`: Gráfico de líneas.
 * - `HEATMAP`: Mapa de calor.
 * Ejemplo1: BAR '(' Name_dataframe, name_or_index_columna_X, name_or_index_columna_Y ')'
 * Ejemplo2: HEATMAP '(' Name_dataframe ')'
 */
plt_data: fun=('SCATTER' | 'BAR' | 'PLOT') '(' ID ','(NUMBER|ID) ',' (NUMBER|ID) ')' #plot
   	| 'HEATMAP' '(' ID ')'							     #sns
   	;
      
/* draw_fun: Define la instrucción para dibujar una función.
 * Ejemplo: DRAW (SIN(x), -5, 5, 1000)
*/
draw_fun: 'DRAW' '(' expr ',' NUMBER ',' NUMBER ',' NUMBER ')';   

/**
 * Definición de tokens para operadores y funciones.
 */
MUL :   '*' ; // Multiplicación
DIV :   '/' ; // División
ADD :   '+' ; // Suma
SUB :   '-' ; // Resta
POT :   '^' ; // Potencia
MOD :   '%' ; // Módulo
MATRIXMUL: '@'; // Multiplicacion de matrices
SQRT:   'SQRT'; // Raíz cuadrada
SIN :   'SIN' ; // Seno
COS :   'COS' ; // Coseno
TAN :   'TAN' ; // Tangente
INV :   'INV' ; // Inverso
TRAS:   'TRAS'; // Traspuesta
MAX :   'MAX'; // Máximo
MIN :   'MIN'; // Mínimo
MEAN:   'MEAN'; // Media
SUM :   'SUM'; // Suma
READ    : 'READ'; // Leer archivo
WRITE   : 'WRITE'; // Escribir archivo
DROP:   'DROP'; // Eliminar
BAR:    'BAR'; // Barra
PLOT:   'PLOT'; // Gráfico
FILLNA: 'FILLNA'; // Rellenar NA
NORM    : 'NORM'; // Normalizar
SCATTER: 'SCATTER'; // Dispersión
HEATMAP : 'HEATMAP'; // Mapa de calor
DRAW    : 'DRAW'; // Gráfico de funciones
DATA_FRAME : 'DATA_FRAME';
SELECT_COLUMN : 'SELECT_COLUMN';
CONCAT_COLUMN : 'CONCAT_COLUMN';
IF: 'if'; // Condicional
ELSE: 'else'; // Condicional parte 2
FOR: 'for'; // Bucle

/**
 * Definición de tokens para identificadores, números y listas.
 */
ID  :   [a-zA-Z]+ ;        // Identificadores
NUMBER: [0-9]+ ('.' [0-9]+)?; // Números (enteros y flotantes)
LIST:   '[' NUMBER ( ',' NUMBER)* ']' | '[' LIST ( ',' LIST)* ']' | '[' ']'; // Listas

/**
 * Definición de tokens de utilidad.
 */
NEWLINE: '\r'? '\n' ;       // Nueva línea
WS  :   [ \t]+ -> skip ;    // Espacios en blanco (ignorar)
