grammar LabeledExpr; // rename to distinguish from Expr.g4

prog:   (stat | condition | for | write | def | dfaction | graf)+;

stat:   expr NEWLINE          # print
    |   ID '=' expr NEWLINE   #assign
    |   NEWLINE               # blank
    ;

expr:   expr op=('*'|'/'|'+'|'-'|'^'|'%') expr      	# AddSub
    |   INT                         			# int
    |   ID                          			# id
    |   '(' expr ')'                			# parens
    |   LIST                        			# list
    |   fun=('SIN'|'COS'|'TAN'|'SQRT') '(' expr ')'	# Funcs
    |   fun=('INV'|'TRAS') '(' expr ')'                 # Mat
    |   'READ' '(' ID (',' 'Header')? ')'               #DataFrame
    ;

condition: 'if' expr fun=('=='|'!='|'<'|'>'|'<='|'>=') expr '{' block '}' (NEWLINE 'else' '{' block '}' )? NEWLINE+;

block: NEWLINE  (prog);

for: 'for' '(' expr ',' expr ',' expr ')' '{' block '}';

write: 'WRITE' '(' ID ',' ID ')';

def: ID '=' 'lambda ' ID (',' ID)* ':' ID (op=('*'|'/'|'+'|'-'|'^'|'%') ID)* NEWLINE;

dfaction: ID '.' action NEWLINE;

action: ('DROP' | 'MIN' | 'MEAN' | 'MAX' | 'FILLNA') '[' (INT|ID) ']'	#drop
      | 'NORM'							#norm
      ;
      
graf: ID '.' plt NEWLINE;

plt: ('SCATTER' | 'BAR' | 'PLOT') '[' (INT|ID) ',' (INT|ID) ']' #plot
   | 'HEATMAP'					#sns
   ;

MUL :   '*' ; // assigns token name to '*' used above in grammar
DIV :   '/' ;
ADD :   '+' ;
SUB :   '-' ;
POT : 	'^' ;
MOD :   '%' ;
SQRT:   'SQRT';
SIN :   'SIN' ;
COS :   'COS' ;
TAN :   'TAN' ;
INV :   'INV' ;
TRAS:   'TRAS';
LIST:   '[' INT ( ',' INT)* ']' | '[' LIST ( ',' LIST)* ']' | '[' ']';
ID  :   [a-zA-Z]+ ;        // match identifiers
INT: '-'? [0-9]+ ('.' [0-9]+)?; // match floats
NEWLINE:'\r'? '\n' ;       // return newlines to parser (is end-statement signal)
WS  :   [ \t]+ -> skip ;   // toss out whitespace

