import matplotlib.pyplot as plt 
import random
from matplotlib.animation import FuncAnimation
import pandas as pd
import matplotlib.dates as mdates

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
for ax in axes:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

fig.subplots_adjust(hspace=0.5, bottom=0.1, top=0.9, left=0.15, right=0.95)

def update(frame):
    global graph

    data = pd.read_csv('modbus_log.csv')
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    y = [data['Temp C'],data['Humidity']]
    latest_time = data['Timestamp'].max()
    cutoff_time = latest_time - pd.Timedelta(hours=24)
    data = data[data['Timestamp'] >= cutoff_time]
    x = data['Timestamp']
    # creating a new graph or updating the graph
    for ax, graphs, ydata in zip(axes, graph, y):
        graphs.set_xdata(x)
        graphs.set_ydata(ydata)
        ax.set_xlim(x.min(), x.max())
        ax.relim()
        ax.autoscale_view()
    fig.canvas.draw_idle()
    counter += 1
    print(counter)
    if counter >= 10:
        plt.savefig("Temp and Humidity Graph.png")
        counter = 0
    return graph,


anim = FuncAnimation(fig, update, interval=1000)
plt.show()

