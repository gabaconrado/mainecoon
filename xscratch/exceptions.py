'''
xScratch exceptions
'''


class XSSyntaxError(Exception):
    '''
    Error raised when there is a syntax error in the script
    '''
    pass


class XSSemanticError(Exception):
    '''
    Error raised when there is a semantic error in the script
    '''
    pass


class XSArduinoError(Exception):
    '''
    Error raised when there is a communication error with the arduino
    '''
    pass
