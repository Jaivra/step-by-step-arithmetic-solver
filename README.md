# Progetto di Linguaggi e Traduttori Valerio Cislaghi

## Procedimento

### Creazione Manager

Creare un oggetto di tipo ArithmeticManager(*domain*) che riceve il dominio in cui l'espressione aritmetica deve essere valutata

possibili domini: 'N', 'Z', 'Q', 'R'

<pre>
AM = ArithManager('Q')
</pre>


### Parser
Per il parsing di un'espressione chiamare il metodo shuntingYardExpr2ast della classe ArithmeticManager, il quale restituirà un AST con annotazioni riguardo la priorità di ogni espressione per guidare il walker alla valutazione step by step.

<pre>
ast = AM.shuntingYardExpr2ast(expr)
</pre>


Nota: l'espressione deve seguire il formato definito nelle specifiche.
Per definire una sottoespressione senza utilizzare le parentesi "aritmetiche" (graffe, quadre e tonde) è possibile utilizzare le parentesi < expr >.
Ad esempio, < 2 + 3 > / < 4 x 6 > rappresenta la seguente espressione:  
<img src="https://render.githubusercontent.com/render/math?math=\frac{2+3}{45 \times 6}">


### Generazione blocchi di sottoespressioni

Utilizzare il metodo blocks della classe ArithmeticManager per suddividere l'espressioni in blocchi, ogni blocco non sarà altro che l'AST di una sottoespressione.
La lista di sottoespressioni restituita sarà ordinata secondo il grado di annidamento stabilito dal tipo di parentesizzazione. Quindi la prima sottoespressione della lista sarà quella da eseguire per prima.
Il metodo blocks, al suo interno, utilizza un oggetto di tipo ExprBlock per la suddivisione in blocchi e per fare inferenza sul tipo di parentesizzazione adottato nell'espressione ed eventualmente lancia un'eccezione nel caso in cui la parentesizzazione non sia consentita (un'altra opzione era farlo direttamente nel parser).

Quando un'espressione A contiene al suo interno una sottoespressione B, l'AST di A conterrà un blocco che identifica univocamente attraverso un ID che identifica la sottoespressione (l'AST) di B (guarda lo schema sotto).
In questo modo per la valutazione di una sottoespressione non sarà necessario visitare l'AST di tutta l'espressione, ma solo l'ast corrispondente a quella sottoespressione.

Dovrà essere utilizzata una memoria aggiuntiva per contenere i risultati delle sottoespressioni già valutate.

<pre>
blocks = AM.blocks(ast)
MEMORY = dict(blocks)
</pre>

### Valutazione step by step

Dopo aver svolto i passi precedenti è possibile passare alla valutazione step by step dell'espressione aritmetica.

Per ogni passo di valutazione sarà necessario chiamare il metodo prior della classe ArithmeticManager, che ha il compito di:
* Annotare il nodo dell'AST contenente la sottoespressione da valutare.
* Annotare l'AST passato in input con le nuove priorità non considerando più l'espressione che sarà calcolata (quella del punto precedente).
* Restituire il parent del nodo che si deve valutare in quello specifico step.

Le annotazioni sull'AST definite dal metodo prior serviranno anche al metodo latex (che stampa l'espressione corrente secondo le regole stabilite) per la formattazione del testo.

Il metodo eval riceve in input un AST e il dizionario che rappresenta la "memoria di esecuzione" (nel caso in cui debba essere valutata un'espressione che contiene una sottoespressione al suo interno).
Restituisce in output il valore ottenuto valutando l'espressione.

Ogni passo va ripetuto finchè esistono espressioni da valutare.
<pre>
while blocks:
    block_id, current_block = blocks[0]
    parent_to_calc = AM.prior(current_block)
    tex = AM.latex(main_block, MEMORY)
        
    parent_to_calc.children =  [Tree({'type': 'atomExpr', 'value': AM.eval(child, MEMORY), 'priority': 0, '_calc': 'last'}, []) 
                                    if is_next_to_calc(child) else child
                                    for child in parent_to_calc.children]

    if is_calculable(current_block):
        current_block = current_block.children[0]
        blocks = blocks[1:]

    MEMORY[block_id] = current_block
</pre>

![a relative link](doc/schema.png)
