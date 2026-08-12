import matplotlib.pyplot as plt 
import random
from matplotlib.animation import FuncAnimation
import pandas as pd

fig, (ax1, ax2) = plt.subplots(2,1)
graph1, = ax1.plot([],[],color = 'b')
graph2, = ax2.plot([],[],color = 'b')
graph = [graph1,graph2]
axes = [ax1, ax2]
plt.ylim(0,30)
x = [1]

def update(frame):
    global graph

    data = pd.read_csv('modbus_log.csv')
    y = data[['Temp C'],['Humidity']]
    x = list(range(1, len(data) + 1))
    # creating a new graph or updating the graph
    for axes, graph, data in zip(axes, graph, y):
        graph.set_xdata(x)
        graph.set_ydata(y)
        ax.relim()
        ax.autoscale_view()
    fig.canvas.draw_idle()
    ax1.title("Temperature vs Time")
    ax2.title("Humidity vs Time")
    ax1.xlabel("Time")
    ax2.xlabel("Time")
    ax1.set_ylabel("Temperature (celsius)")
    ax2.set_ylabel("Humidity")
    return graph,

anim = FuncAnimation(fig, update, interval=1000)
plt.show()