grammar arithmetic;
ignoblebug: expr;

s : expr EOF;



expr
   : <assoc=right>expr POW expr           # powExpr
   | (PLUS | MINUS) expr                  # unaryExpr
   | (PLUS | MINUS)? (INT|REAL|RAT)       # atomExpr
   | expr FRACT expr                      # fractExpr
   | expr (TIMES | DIV) expr              # divProdExpr
   | expr (PLUS | MINUS) expr             # addSubExpr
   | CURLY_L_BRACK expr CURLY_R_BRACK     # curlyBlockExpr
   | SQUARE_L_BRACK expr SQUARE_R_BRACK   # squareBlockExpr
   | ROUND_L_BRACK expr ROUND_R_BRACK     # roundBlockExpr
   | SUBEXP_L_BRACK expr SUBEXP_R_BRACK   # subExpr
   ;


INT
   : NUM
   ;

RAT
    : NUM FRACT NUM
    ;

REAL
   : NUM ('.' NUM +)? (E SIGN? NUM)?
   ;

NUM
   :  ('0' .. '9') + (('0' .. '9') +)?
   ;


fragment E
   : 'E' | 'e'
   ;

fragment SIGN
   : ('+' | '-')
   ;

CURLY_L_BRACK : '{' ;
CURLY_R_BRACK : '}' ;
SQUARE_L_BRACK : '[' ;
SQUARE_R_BRACK : ']' ;
ROUND_L_BRACK : '(' ;
ROUND_R_BRACK : ')' ;
SUBEXP_L_BRACK : '<' ;
SUBEXP_R_BRACK : '>' ;
PLUS   : '+' ;
MINUS  : '-' ;
TIMES  : 'x' ;
DIV    : ':' ;
POINT  : '.' ;
POW    : '^' ;
FRACT  : '/' ;

WS: [ \t\n\r]+ -> skip ;
