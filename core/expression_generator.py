class Expression:
    pass

class Number(Expression):
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)

class BinaryExpression(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"{self.left} {self.op} {self.right}"

class UnaryExpression(Expression):
    def __init__(self, left, op):
        self.left = left
        self.op = op

    def __str__(self):
        return f"{self.op} {self.left}"

class ParenthesizedExpression(Expression):
    def __init__(self, exp):
        self.exp = exp

    def __str__(self):
        return f"( {self.exp} )"


from random import random, randint, choice


def generate_expression(prob):
    def generate_expression_aux(prob):
        p = random()
        if p > prob:
            return Number(randint(1, 100))
        elif randint(0, 3) == 0:
            return ParenthesizedExpression(generate_expression(prob / 1.2))
        else:
            left = generate_expression(prob / 1.2)
            if randint(0, 2) == 0:
                return UnaryExpression(left, '-')
            # op = choice(["+", "-", "x",'^'])
            # op = choice(["+", "-", "x",":", "/", '^'])
            op = choice(["+", "-", "x", "/", '^'])
            if op == '^': right = 2 if randint(0, 1) == 0 else -2
            else: right = generate_expression(prob / 1.2)
            return BinaryExpression(left, op, right)
    return str(generate_expression_aux(prob))