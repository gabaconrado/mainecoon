'''
File with token definitions
'''


class XSToken():
    '''
    The xScratch token class
    '''

    def __init__(self, t_type, value):
        '''
        Initialize token

        @param str type: the token type
        @param str/int value: the token value
        '''
        self.t_type = t_type
        self.value = value

    def __str__(self):
        '''
        Human readable representation for the object, outputs the type and the value
        '''
        return '{} : {}'.format(self.t_type, self.value)
