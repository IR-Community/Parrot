


import matplotlib.pyplot as plt
import numpy as np


def plot_trend(xlabel, parameter_list, ylabel, result_list):
    plt.plot(parameter_list, result_list,
         color='blue', marker='o', linestyle='dashed',linewidth=1, markersize=6)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def plot_bar(xlabel, model_list, ylabel, result_list):
       
    plt.rcdefaults()
    fig = plt.gcf()
    
    objects = models_list
    y_pos = np.arange(len(objects))

    plt.bar(y_pos, result_list, align='center', alpha=0.3)
    plt.xticks(y_pos, objects)
    plt.ylabel(ylabel)

    plt.show()