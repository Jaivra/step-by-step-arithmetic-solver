E -> t | + t | - t
   | E ^ E
   | E / E
   | + E | - E
   | E x E | E : E
   | E + E | E - E
   | { E }    
   | [ E ]
   | ( E )   
   | < E >
   ;
   
   
E -> T E' E''
T -> F T' T''
E' -> + T E' | - T E' | ε
T' -> * F T' | : F T' | ε
T'' -> / F T'' | ^ F T'' | ε
F -> (E) | [E] | {E} | t