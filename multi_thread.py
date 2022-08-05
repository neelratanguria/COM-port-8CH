import logging
import threading
import time
import serial

import json
import matplotlib.pyplot as plt


class EyeRa():
    def __init__(self):
        self.data = []

    def thread_function(self, arg):
        ser = serial.Serial(port='COM31', baudrate=115200)
        
        while True:
            try:
                measures = ser.readline().decode('utf-8-sig')
                measures = measures.rstrip()
                measures = measures.lstrip()
                measures = measures.strip()
                measures = measures.replace(measures[0], "")
                
                obj = json.loads(str(measures))
                
                channel_vals = [obj["0"], obj["2"],
                                obj["3"], obj["4"], obj["5"],
                                 obj["7"]]
                self.data = channel_vals
                
            except:
                pass
    
    def start(self):
        x = threading.Thread(target=self.thread_function, args=(1,))
        x.start()
        
        while True:
            print(self.data)
            try:
                Channels = ["CH0","CH2","CH3","CH4","CH5","CH7"]
                plt.barh(Channels, self.data)
                
                for index, value in enumerate(self.data):
                    plt.text(value, index,
                             str(value))
                plt.show()
                plt.xlim((0,46000))
                plt.pause(0.05)
                plt.clf()
            except:
                pass
            

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    eyera = EyeRa()
    eyera.start()
    
    
    