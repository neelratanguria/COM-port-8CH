import logging
import threading
import time
import serial

import json
import matplotlib.pyplot as plt

def Average(lst):
    return sum(lst) / len(lst)

show_plot = True


class EyeRa():
    def __init__(self):
        self.data = []

    def thread_function(self, arg):
        ser = serial.Serial(port='COM4', baudrate=115200)
        
        while True:
            try:
                measures = ser.readline().decode('utf-8-sig')
                measures = measures.rstrip()
                measures = measures.lstrip()
                measures = measures.strip()
                measures = measures.replace(measures[0], "")
                
                obj = json.loads(str(measures))
                
                channel_vals = [obj["0"], obj["1"], obj["2"],
                                obj["3"], obj["4"], obj["5"],obj["6"],
                                 obj["7"]]
                self.data = channel_vals
                
            except:
                pass
    
    def start(self):
        x = threading.Thread(target=self.thread_function, args=(1,))
        x.start()
        mListCH2 = []
        mListCH1 = []
        while True:
            
            try:
                #print(self.data[2])
                mListCH2.append(int(self.data[2]))
                if len(mListCH2) > 40:
                    mListCH2.pop(0)
                
                
                mListCH1.append(int(self.data[1]))
                if len(mListCH1) > 40:
                    mListCH1.pop(0)
                print("CH1: ", Average(mListCH1), end='\t\t')
                print("CH2: ",Average(mListCH2))
                
                Channels = ["CH0","CH1","CH2","CH3","CH4","CH5","CH6","CH7"]
                if show_plot:
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
    
    
    