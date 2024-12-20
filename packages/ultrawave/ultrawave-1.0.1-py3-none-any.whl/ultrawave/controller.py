import serial, socket

class UHF:
    
    def __init__(self, port:str, timeout:int, baudrate:int, debug=False):
        self.__port = port
        self.__timeout = timeout
        self.__baudrate = baudrate
        self.__conn = None
        self.__debug = debug
        
        if self.__debug:
            print('Init UHF Object')
        
    def set_callback(self, func):
        func()
        
    def connect(self):
        try:
            if self.__debug:
                print(f'Try connecting to {self.__port} . . .')
            self.__conn = serial.Serial(port=self.__port, baudrate=self.__baudrate, timeout=self.__timeout)
            if self.__debug:
                print(f'Connection success!')
            return self.__conn
        except Exception as error_conn:
            if self.__debug:
                print(f'Error when try connect {self.__port}')
                print(f'{error_conn}')
            return None