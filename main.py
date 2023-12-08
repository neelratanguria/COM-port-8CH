import serial
import json
import matplotlib.pyplot as plt

ser = serial.Serial(port='COM5', baudrate=115200)

line = ser.readline()
Channels = ["CH0","CH1","CH2","CH3","CH4","CH5","CH6","CH7",]

while True:
    try:
        measures = ser.readline().decode('utf-8-sig')
        measures = measures.rstrip()
        measures = measures.lstrip()
        measures = measures.strip()
        measures = measures.replace(measures[0], "")
        try:
            obj = json.loads(str(measures))
            print(obj)
            
            channel_vals = [obj["0"], obj["1"], obj["2"],
                            obj["3"], obj["4"], obj["5"],
                            obj["6"], obj["7"]]
            plt.bar(Channels,channel_vals)
            plt.pause(0.05)
            plt.clf()
        except Exception as e:
            pass
    except:
        pass