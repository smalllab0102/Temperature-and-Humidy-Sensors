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
import matplotlib.dates as mdates
import random
from matplotlib.animation import FuncAnimation
import pandas as pd

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7))

graph1, = ax1.plot([], [], color='b')
graph2, = ax2.plot([], [], color='b')
graph = [graph1, graph2]
axes = [ax1, ax2]

ax1.set_ylim(0, 30)
ax2.set_ylim(0, 100)

ax1.set_title("Temperature vs Time")
ax2.set_title("Humidity vs Time")
ax1.set_xlabel("Time")
ax2.set_xlabel("Time")
ax1.set_ylabel("Temperature (celsius)")
ax2.set_ylabel("Humidity")

# Format X-axis to display readable clock times (HH:MM:SS)
for ax in axes:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    fig.autofmt_xdate()  # Rotates the dates so they do not overlap

fig.subplots_adjust(hspace=0.5, bottom=0.15, top=0.9, left=0.15, right=0.95)

def update(frame):
    # 1. Read data from CSV
    data = pd.read_csv('modbus_log.csv')
    
    # Clean the 'timestamp' text column by erasing "modbus_log.csv" if it appears in any cells
    clean_timestamps = data['timestamp'].astype(str).str.replace('modbus_log.csv', '', regex=False)
    
    # Convert cleaned text to actual pandas datetime objects
    data['DateTime'] = pd.to_datetime(clean_timestamps)
    
    # 2. Filter data so it only includes rows from today
    today_start = pd.Timestamp.today().normalize()
    tomorrow_start = today_start + pd.Timedelta(days=1)
    daily_data = data[data['DateTime'] >= today_start]
    
    # 3. Extract filtered X and Y values
    x = daily_data['DateTime'].tolist()
    y = [daily_data['Temp C'].tolist(), daily_data['Humidity'].tolist()]
    
    # 4. Update the plots and force the X-axis view boundaries to today
    for ax, graphs, ydata in zip(axes, graph, y):
        graphs.set_xdata(x)
        graphs.set_ydata(ydata)
        
        # Lock X-axis view strictly from midnight today to midnight tomorrow
        ax.set_xlim(today_start, tomorrow_start)
        
        # Rescale the Y-axis automatically based on today's data limits
        ax.relim()
        ax.autoscale_view(scalex=False, scaley=True)
        
    fig.canvas.draw_idle()
    return graph

# blit=False handles dynamic axis manipulation smoothly
anim = FuncAnimation(fig, update, interval=1000, blit=False)
plt.show()
