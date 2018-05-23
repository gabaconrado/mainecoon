'''
xScratch analysers components
'''

from xscratch.exceptions import XSSyntaxError
from .token import XSToken
from . import functions


class XSInterpreter():
    '''
    The xScratch interpreter class
    '''

    reserved_words = ['se', 'entao', 'para', 'fimse', 'fimpara']
    operators = '+-*/'
    comparators = ['maior', 'menor', 'diferente', 'igual']

    functions = {
        'escreva': functions.escreva
    }

    environment = {}
    if_flag = False
    if_branch = False

    # TODO: Get the string from the view
    def __init__(self):
        '''
        Initialize interpreter

        @param str script: the raw script
        '''
        with open('/home/gabriel/dev/mainecoon/resources/test/script.xs', 'rb') as script_file:
            script = script_file.read().decode('utf-8')
        self.script = iter(script.splitlines())

    def _clear(self):
        '''
        Clears the environment after an execution
        '''
        self.environment.clear()

    def read(self):
        '''
        Interpret the loaded script
        '''
        # try:
        self._process()
        self._clear()
        # except XSSyntaxError as error:
        #     print("Syntax error found: {}".format(error))

    # pylint: disable=too-many-branches
    def _process(self):
        '''
        Process the input while there is new lines

        @param: str script: the full script iterator splitted by lines
        @raises: SyntaticError if there is an error within the script
        '''
        # While there is a new line
        while True:
            next_line = self._get_line()
            if not next_line:
                break
            # Gets the token iterator
            tokens = self._tokenize(next_line)
            first = next(tokens)
            # If branching
            if self.if_flag:
                if first.value == 'fimse':
                    self.if_flag = False
                    continue
                if not self.if_branch:
                    continue
            if first.t_type == 'identifier':
                second = next(tokens)
                if second.t_type == 'equal':
                    # Assignment
                    expression = list(tokens)
                    if len(expression) == 1:
                        self._save_to_environment(first.value, expression[0].value)
                    elif len(expression) == 3:
                        right = expression.pop()
                        operator = expression.pop().value
                        left = expression.pop()
                        right = right.value if right.t_type == 'immediate' else \
                            self._load_from_environment(right.value)
                        left = left.value if left.t_type == 'immediate' else \
                            self._load_from_environment(left.value)
                        result = self._evaluate_expression(left, right, operator)
                        self._save_to_environment(first.value, result)
                elif first.value in self.functions:
                    # Function
                    argument = self._load_from_environment(second.value) if \
                        second.t_type == 'identifier' else second.value
                    self.functions[first.value](argument)
                else:
                    self._raise_error()
            elif first.t_type == 'reserved':
                if first.value == 'se':
                    expression = list(tokens)
                    right = expression.pop()
                    comparator = expression.pop().value
                    left = expression.pop()
                    right = right.value if right.t_type == 'immediate' else \
                        self._load_from_environment(right.value)
                    left = left.value if left.t_type == 'immediate' else \
                        self._load_from_environment(left.value)
                    self.if_flag = True
                    self.if_branch = self._evaluate_comparison(left, right, comparator)
                    # TODO: implement the branching
                # elif first.value == 'para':
                #     iterator = next(tokens)
                #     start = next(tokens)
                #     end = next(tokens)
                #     if start.t_type != 'immediate' or end.t_type != 'immediate' or
                #        end.value == start.value or end.value < start.value:
                #         self._raise_error()
                #     self.for_counter = (end.value - start.value) + 1
                else:
                    self._raise_error()
            else:
                self._raise_error()

    # TODO: Improve the error detection
    # pylint: disable=no-self-use
    def _raise_error(self):
        '''
        Raise an exception
        '''
        raise XSSyntaxError()

    def _get_line(self):
        '''
        Gets a new line from the script

        @return: New line if there is, None otherwise
        '''
        return next(self.script, None)

    def _tokenize(self, line):
        '''
        Tokenize a given line

        @param str line: the line to be tokenized
        @return iter token tokenized: an iterator with the tokens
        @raises SyntaxError if invalid token
        '''
        # TODO: Improve this function in order to accept spaces in strings
        tokenized = []
        for token_str in line.split(' '):
            if token_str.isdigit():
                token = XSToken('immediate', int(token_str))
            elif token_str in self.operators:
                token = XSToken('operator', token_str)
            elif token_str == '=':
                token = XSToken('equal', token_str)
            elif token_str in self.reserved_words:
                token = XSToken('reserved', token_str)
            elif token_str in self.comparators:
                token = XSToken('comparator', token_str)
            elif token_str.isalpha():
                token = XSToken('identifier', token_str)
            elif token_str[0] == '"' and token_str[-1] == '"':
                token = XSToken('string', token_str)
            else:
                raise XSSyntaxError('Invalid token {}'.format(token))
            tokenized.append(token)
        return iter(tokenized)

    def _evaluate_expression(self, left, right, operator):
        '''
        Evaluate an expression

        @param int left: the left operand
        @param int right: the right operand
        @param str operator: the operator
        @return int result: the expression result
        '''
        if operator == '+':
            result = left + right
        elif operator == '-':
            result = left - right
        elif operator == '/':
            result = left / right
        elif operator == '*':
            result = left * right
        else:
            self._raise_error()
        return result

    def _evaluate_comparison(self, left, right, comparator):
        '''
        Evaluate an expression

        @param int left: the left operand
        @param int right: the right operand
        @param str comparator: the operator
        @return bool result: result of the comparison
        '''
        if comparator == 'maior':
            result = left > right
        elif comparator == 'menor':
            result = left < right
        elif comparator == 'igual':
            result = left == right
        elif comparator == 'diferente':
            result = left != right
        else:
            self._raise_error()
        return result

    def _load_from_environment(self, identifier):
        '''
        Get an variable saved in the environment

        @param str identifier: variable name
        @raises XSSemanticError if the variable does not exist
        @return the value from the variable
        '''
        if identifier not in self.environment:
            raise XSSyntaxError('Invalid reference to "{}"'.format(identifier))
        return self.environment[identifier]

    def _save_to_environment(self, identifier, value):
        '''
        Saves a variable into the environment

        @param str identifier: variable name
        @param value: the value
        '''
        self.environment[identifier] = value
