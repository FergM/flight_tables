import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

def ecdf(data):
    """ Compute Empirical CDF 
    Input: List or np array of numbers.
    """
    x = np.sort(data)
    n = x.size
    y = np.arange(1, n+1) / n
    return(x,y)

file_name = "heathrow_draft.p"
with open(file_name, "rb") as f2:
    flights_df = pickle.load(f2)

flights_df.replace({'delay_mins': None}, float("nan"))
flights_df.dropna(inplace=True)

data = list(flights_df.delay_mins)
x, y = ecdf(data)

plt.scatter(x=x, y=y);
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
plt.xticks(x)
plt.yticks(y)
plt.show()