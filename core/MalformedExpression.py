class MalformedExpression(SystemExit):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super().__init__(self.format_msg(*args))

    @staticmethod
    def format_msg(message, tokens, underline, bars):
        res = ' '
        for i, c in enumerate(tokens):
            if i in underline:
                c = f'\033[91m{c}\033[0m'
            if i in bars:
                c = f'{c}\033[91m\u2193\033[0m'

            res += c + ' '
        return f'{message}\n\n{res}'
