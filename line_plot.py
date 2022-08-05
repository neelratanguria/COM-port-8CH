import logging
import threading
import time
import serial

import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

LEN = 1000
X = list(range(0, LEN))
window_size = 20
MOV_AVG_LEN = (LEN-window_size)+1
X_MOVING_AVG = list(range(0, MOV_AVG_LEN))
Y_LIMIT_U = 400
Y_LIMIT_L = 0
USE_Y_LIMIT = False


class EyeRa():
    def __init__(self):
        self.data = []
        self.ch0 = []
        figure, self.ax = plt.subplots(figsize=(4,3))
        self.line, = self.ax.plot([0,1,2,3,4], [100,200,300,400,500])
        
        
        
        self.ani = FuncAnimation(figure,
                    self.func_animate,
                    frames=10,
                    interval=50)


    def thread_function(self, arg):
        ser = serial.Serial(port='COM31', baudrate=115200)
        
        global LEN
        
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
                
                self.ch0.append(int(obj["0"]))
                
                
                if len(self.ch0) > LEN:
                    self.ch0.pop(0)
            except:
                pass
    def func_animate(self, i):
        global LEN
        global X
        global X_MOVING_AVG
        global Y_LIMIT_U
        global Y_LIMIT_L
        global USE_Y_LIMIT
        i = 0
        # Initialize an empty list to store moving averages
        moving_averages = []
          
        # Loop through the array to consider
        # every window of size 3
        while i < len(self.ch0) - window_size + 1:
            
            # Store elements from i to i+window_size
            # in list to get the current window
            window = self.ch0[i : i + window_size]
          
            # Calculate the average of current window
            window_average = round(sum(window) / window_size, 2)
              
            # Store the average of current
            # window in moving average list
            moving_averages.append(window_average)
              
            # Shift window to right by one position
            i += 1
        print(len(moving_averages))
        
        
        # No rolling avg
        '''
        if len(self.ch0) == LEN:
            self.ax.clear()
            self.ax.plot(X, self.ch0)
        '''
        
        if len(moving_averages) == (MOV_AVG_LEN):
            self.ax.clear()
            if USE_Y_LIMIT:
                plt.ylim([Y_LIMIT_L, Y_LIMIT_U])
            self.ax.plot(X_MOVING_AVG, moving_averages)
        
        return self.line,
    
    def start(self):
        x = threading.Thread(target=self.thread_function, args=(1,))
        x.start()


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    eyera = EyeRa()
    eyera.start()
    
    
    