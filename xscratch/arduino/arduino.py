'''
File responsible to the communication between the system and the arduino
'''

import serial
from xscratch.exceptions import XSArduinoError

serial_port = '/dev/ttyACM0'
bauld_rate = 9600


class XSArduinoService():
    '''
    Class that will communicate with the arduino
    '''

    # TODO: Change to portuguese
    led_list = {
        'blue': '0',
        'yellow': '1'
    }

    def __init__(self):
        '''
        Open the connection and the port(The port keep opened until end of class)
        '''
        # Creates the class serial handler
        self.handler = serial.Serial(serial_port, bauld_rate)
        # Waits for the arduino to start
        if 'Ready' not in self.handler.readline().decode('utf-8'):
            raise XSArduinoError('Arduino initializing fail')

    def open(self):
        '''
        Open the serial communication when needed
        '''
        if not self.handler.is_open:
            self.handler.open()

    def close(self):
        '''
        Close the serial communication after it is used
        '''
        if self.handler.is_open:
            self.handler.close()

    def write_data(self, data):
        '''
        Write data into the serial port to the arduino

        @param str data: the data to be writen
        '''
        data = str(data)
        self.handler.write(data.encode('utf-8'))
        # Waits for the command to finish
        if 'Command done' not in self.handler.readline().decode('utf-8'):
            raise XSArduinoError('Arduino communication error')

    def lcd_write(self, text):
        '''
        Send command to write a text in the Arduino LCD

        @param str text: The text to be written
        '''
        self.write_data('2{}'.format(text))

    def toggle_led(self, led):
        '''
        Send command to toggle a Led in the Arduino

        @param str led: The LED to be toggled
        '''
        self.write_data(self.led_list[led])
