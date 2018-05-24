'''
File responsible to the communication between the system and the arduino
'''

import serial

serial_port = '/dev/ttyACM0'
bauld_rate = 9600


class XSArduinoService():
    '''
    Class that will communicate with the arduino
    '''

    def __init__(self):
        '''
        Open the connection and the port(The port keep opened until end of class)
        '''
        # Creates the class serial handler
        self.handler = serial.Serial(serial_port, bauld_rate)
        # Waits for the arduino to start
        self.handler.readline()

    def write_data(self, data):
        '''
        Write data into the serial port to the arduino

        @param str data: the data to be writen
        '''
        data = str(data)
        self.handler.write(data.encode('utf-8'))
