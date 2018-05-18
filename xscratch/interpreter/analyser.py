'''
xScratch analysers components
'''

from xscratch.exceptions import XSSyntaxError, XSSemanticError


class XSInterpreter():
    '''
    The xScratch interpreter class
    '''

    comparators = ['igual', 'maior', 'menor']
    functions = ['escreva']
    reserved_words = ['se', 'entao', 'para', 'fimse', 'fimpara', 'de', 'ate']
    operators = '+-*/'

    rules = {}

    # TODO: Get the string from the view
    def __init__(self):
        '''
        Initialize interpreter

        @param str script: the raw script
        '''
        with open('/home/gabriel/dev/mainecoon/resources/test/script.xs', 'rb') as script_file:
            script = script_file.read().decode('utf-8')
        self.script = script

    def read(self):
        '''
        Interpret the loaded script
        '''
        try:
            for line in self.script.splitlines():
                tokenized_line = self._tokenize(line)
                print(tokenized_line)
                self._process(tokenized_line)
        except XSSyntaxError as error:
            print("Syntax error found: {}".format(error))
        except XSSemanticError as error:
            print("Semantic error found: {}".format(error))

    def _tokenize(self, line):
        '''
        Tokenize a given line

        @param str line: the line to be tokenized
        @return list token tokenized: a list with the token types
        @raises SyntaxError if invalid token or identifier is a reserved word
        '''
        tokenized = []
        for token in line.split(' '):
            if token.isdigit():
                # Immediate
                tokenized.append('immediate')
            elif token in self.operators:
                # Operator
                tokenized.append('operator')
            elif token in self.comparators:
                # Comparator
                tokenized.append('comparator')
            elif token in self.functions:
                # Comparator
                tokenized.append('function')
            elif token.isalpha():
                # Identifier
                if token not in self.reserved_words:
                    tokenized.append('identifier')
                else:
                    raise XSSyntaxError('Invalid identifier "{}"'.format(token))
            elif token == '=':
                # Equal
                tokenized.append('equal')
            else:
                raise XSSyntaxError('Invalid token "{}"'.format(token))
        return tokenized

    def _process(self, tokenized_line):
        '''
        Process the line semantically

        @param: list token tokenized: a list with the token types
        @return: list operation operations: list with the needed operations to run the line
        @raises: SemanticError if the statement does not follow the semantic rules
        '''
        pass
