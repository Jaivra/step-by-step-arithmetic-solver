# Project of formal languages and compiler Course 
Specifics available [here](https://github.com/let-unimi/progetti/tree/master/02-Simplicio)
## Requirements
* Installation of requirements.txt with pip
* Download ANTLR4 and set environment variable ANTLR4_JAR to the downloaded jar 

## How to use it
### Manager Creation

Create an ArithmeticManager(*domain*) object that receives in the constructor the domain of the expression.
Possibile domains: 'N', 'Z', 'Q', 'R'

<pre>
AM = ArithManager('Q')
</pre>


### Parser
For the expression parsing call the shuntingYardExpr2ast method of class ArithmeticManager, that returns an AST with annotaion about the property of each expression to guide  step by step the walker to the valutation.

<pre>
ast = AM.shuntingYardExpr2ast(expr)
</pre>


Note: The expression must follow the format defined in the specifics.
To define a sub-expression without using the arithmetic brackets, it's possible to use the symbolds < expr >.
For example:  < 2 + 3 > / < 4 x 6 > represents the following expression:
<img src="https://render.githubusercontent.com/render/math?math=\frac{2+3}{45 \times 6}">

Per definire una sottoespressione senza utilizzare le arithmetic squares (graffe, quadre e tonde) è possibile utilizzare le parentesi < expr >.
Ad esempio, < 2 + 3 > / < 4 x 6 > rappresenta la seguente espressione:  
<img src="https://render.githubusercontent.com/render/math?math=\frac{2+3}{45 \times 6}">


### Generation Blocks of sub-expressions
Using the blocks method of class ArithmeticManager to split the expressions in different blocks, each block is the AST of a sub-expression.
The returned list of subexpressions will be sorted according to the degree of nesting established by the parenthesization type.
So, the first sub-expression of the list will be the one to execute first. 
The blocks method, within it, uses an object of type ExprBlock for subdivision into blocks and to make inference on the type of parenthesis adopted in the expression and possibly throws an exception if the parenthesis is not allowed (another option was to do it directly in the parser).

When an expression A contains inside a sub-expression B, the AST of A will contain a block to identify the sub-expression (AST) of B through an identifier (see the diagram below).
In this way, for the evaluation of a subexpression it will not be necessary to visit the AST of the whole expression, but only the AST corresponding to that subexpression.

Additional memory will need to be used to hold the results of subexpressions that have already been evaluated.
<pre>
blocks = AM.blocks(ast)
MEMORY = dict(blocks)
</pre>

### Step by step valutation

After carrying out the previous steps, it is possible to move on to the step by step evaluation of the arithmetic expression.

For each evaluation step it will be necessary to call the prior method of the ArithmeticManager class, which has the task of:
* Annotate the AST node containing the subexpression to be evaluated.
* Annotate the AST passed in input with the new priorities, no longer considering the expression that will be calculated (that of the previous point).
* Return the parent of the node to be evaluated in that specific step.

The annotations on the AST defined by the prior method will also be used by the latex method (which prints the current expression according to the established rules) for formatting the text.

The eval method receives as input an AST and the dictionary which represents the "execution memory" (in case an expression that contains a sub-expression inside it is to be evaluated).
Returns the value obtained by evaluating the expression as output.

Each step must be repeated as long as there are expressions to be evaluated.

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
