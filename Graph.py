'''
import matplotlib.pyplot as plt 
import random
from matplotlib.animation import FuncAnimation
import pandas as pd

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
    y = [data['Temp C'],data['Humidity']]
    x = list(range(1, len(data) + 1))
    # creating a new graph or updating the graph
    for ax, graphs, ydata in zip(axes, graph, y):
        graphs.set_xdata(x)
        graphs.set_ydata(ydata)
        ax.relim()
        ax.autoscale_view()
    fig.canvas.draw_idle()
    return graph,


anim = FuncAnimation(fig, update, interval=1000)
plt.show()
'''
import matplotlib.pyplot as plt 
import random
from matplotlib.animation import FuncAnimation
import pandas as pd

fig, (ax1, ax2) = plt.subplots(2,1, figsize=(8, 7))
graph1, = ax1.plot([],[],color = 'b')
graph2, = ax2.plot([],[],color = 'b')
graph = [graph1,graph2]
axes = [ax1, ax2]
ax1.set_ylim(0,30)
ax2.set_ylim(0,100)

ax1.set_title("Temperature vs Time")
ax2.set_title("Humidity vs Time")
ax1.set_xlabel("Time")
ax2.set_xlabel("Time")
ax1.set_ylabel("Temperature (celsius)")
ax2.set_ylabel("Humidity")

fig.subplots_adjust(hspace=0.5, bottom=0.1, top=0.9, left=0.15, right=0.95)

def update(frame):
    global graph

    # 1. Read data and convert Timestamp column to datetime objects
    data = pd.read_csv('modbus_log.csv')
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])

    # 2. Filter for only the last 24 hours based on the latest log entry
    if not data.empty:
        latest_time = data['Timestamp'].max()
        cutoff_time = latest_time - pd.Timedelta(hours=24)
        data = data[data['Timestamp'] >= cutoff_time]

    # 3. Use the filtered data for plotting
    y = [data['Temp C'], data['Humidity']]
    x = data['Timestamp'] # Using actual time for the X-axis

    # creating a new graph or updating the graph
    for ax, graphs, ydata in zip(axes, graph, y):
        graphs.set_xdata(x)
        graphs.set_ydata(ydata)
        ax.relim()
        ax.autoscale_view()
        
    fig.canvas.draw_idle()
    return graph,

anim = FuncAnimation(fig, update, interval=1000)
plt.show()