import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    return graph

def get_plot(x, subscriber, customer, title, xlabel, ylabel):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,10))
    plot1 = plt.subplot2grid((2, 2), (0, 0))
    plot2 = plt.subplot2grid((2, 2), (0, 1))
    plot3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)

    plot1.plot(x[0], subscriber[0], label='Subscriber')
    plot1.plot(x[0], customer[0], label='Customer')
    plot1.set_xlabel(xlabel[0])
    plot1.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    plot1.set_ylabel(ylabel[0])
    plot1.set_title(title[0])
    plot1.legend()

    plot2.plot(x[1], subscriber[1], label='Subscriber')
    plot2.plot(x[1], customer[1], label='Customer')
    plot2.set_xlabel(xlabel[1])
    plot2.set_xticks([0, 1, 2, 3, 4, 5, 6])
    plot2.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    plot2.set_ylabel(ylabel[1])
    plot2.set_title(title[1])
    plot2.legend()

    plot3.plot(x[2], subscriber[2], label='Subscriber')
    plot3.plot(x[2], customer[2], label='Customer')
    plot3.set_xlabel(xlabel[2])
    plot3.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])
    plot3.set_ylabel(ylabel[2])
    plot3.set_title(title[2])
    plot3.legend()    
    
    plt.tight_layout()
    graph = get_graph()
    return graph