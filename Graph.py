import matplotlib.pyplot as plt 
import random
from matplotlib.animation import FuncAnimation
import pandas as pd
import datetime as dt

fig, (ax1, ax2) = plt.subplots(2,1, figsize=(8, 7))
graph1, = ax1.plot([],[],color = 'b')
graph2, = ax2.plot([],[],color = 'b')
graph = [graph1,graph2]
axes = [ax1, ax2]
ax1.set_ylim(0,30)
ax2.set_ylim(0,100)
x = [1]

ax1.set_title("Temperature vs Time")
ax2.set_title("Humidity vs Time")
ax1.set_xlabel("Time")
ax2.set_xlabel("Time")
ax1.set_ylabel("Temperature (celsius)")
ax2.set_ylabel("Humidity")

fig.subplots_adjust(hspace=0.5, bottom=0.1, top=0.9, left=0.15, right=0.95)

def update(frame):
    global graph

    data = pd.read_csv('modbus_log.csv')
    data['DateTimeString'] = pd.to_datetime(data['Timestamp']) 
    time_now = data['DateTimeString'].max()
    yesterday = time_now - dt.timedelta(days=1)
    earliest_available = data['DateTimeString'].min()
    graph_start = max(yesterday, earliest_available)
    one_day = data[data['DateTimeString'] >= yesterday]

    x = one_day['DateTimeString']
    y = [one_day['Temp C'], one_day['Humidity']]

    # creating a new graph or updating the graph
    for ax, graphs, ydata in zip(axes, graph, y):
        graphs.set_xdata(x)
        graphs.set_ydata(ydata)
        ax.set_xlim(graph_start, time_now)
        ax.relim()
        ax.autoscale_view(scalex=False, scaley=True)
    fig.canvas.draw_idle()
    return graph,


anim = FuncAnimation(fig, update, interval=1000)
plt.show()