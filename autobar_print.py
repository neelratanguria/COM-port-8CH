import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import random



x = []
y = []

Channels = ["CH0","CH1","CH2","CH3","CH4","CH5","CH6","CH7"]
channel_vals = [1000, 2000, 1500,
                1700, 2400, 1100,
                1400, 1700]

figure, ax = plt.subplots(figsize=(4,3))
bars = ax.bar(Channels, channel_vals)
#plt.axis(Channels)

print(dir(bars))
print(bars.datavalues)



def func_animate(i):
    randomlist = []
    for i in range(0,8):
        n = random.randint(1,3000)
    randomlist.append(n)
    
    bars.datavalues =  randomlist
    
    return bars,

ani = FuncAnimation(figure,
                    func_animate,
                    frames=10,
                    interval=50)

#ani.save(r'animation.gif', fps=10)

plt.show()