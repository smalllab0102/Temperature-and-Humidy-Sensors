import matplotlib.pyplot as plot 
import random
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
graph = ax.plot(x,y,color = 'g')[0]
plt.ylim(0,30)
x = [1]

def update(frame):
    global graph

    x.append(x[-1] + 1)

    data = pd.read_csv('modbus_log.csv')
        y = data['Temp C']
    # creating a new graph or updating the graph
    graph.set_xdata(x)
    graph.set_ydata(y)
    plt.xlim(x[0], x[-1])

anim = FuncAnimation(fig, update, frames = None)
plt.show()