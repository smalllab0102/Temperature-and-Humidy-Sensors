import matplotlib.pyplot as plt 
import random
from matplotlib.animation import FuncAnimation
import pandas as pd

fig, ax = plt.subplots()
graph = ax.plot(x,y,color = 'g')[0]
plt.ylim(0,30)
x = [1]

def update(frame):
    global graph

    data = pd.read_csv('modbus_log.csv')
    y = data['Temp C']
    x = list(range(1, len(y) + 1))
    # creating a new graph or updating the graph
    graph.set_xdata(x)
    graph.set_ydata(y)
    plt.xlim(x[0], x[-1])

anim = FuncAnimation(fig, update, interval=1000)
plt.show()