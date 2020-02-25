import pickle

file_name = "heathrow_draft.p"

with open(file_name, "rb") as f2:
    loaded_df = pickle.load(f2)

print("\nLoaded Head is:\n", loaded_df.head())
print("Loaded Tail is:\n", loaded_df.tail())
print("\n\n")

#----------------------------
flight1 = "UA921"
flight2 = "AA6144"#"AA141"


df1 = loaded_df.loc[loaded_df['flight_id'] == flight1, ["scheduled_datetime", "delay_mins"]]
df2 = loaded_df.loc[loaded_df['flight_id'] == flight2, ["scheduled_datetime", "delay_mins"]]

df1 = df1.set_index("scheduled_datetime")
df2 = df2.set_index("scheduled_datetime")

df1 = df1.rename(columns={"delay_mins": "delay_mins1"})

print(df1)
print(df2)

merged_df = df1.join(df2, how="outer")

merged_df.delay_mins1.iloc[17] = float("nan")

f1 = merged_df.delay_mins1.values
f2 = merged_df.delay_mins.values

print(merged_df)
print(f1)
print(f2)
print("--------------------")

#-----------------------------------------Plot

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

ind = np.arange(len(f1))  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, f1, width,
                label=flight1)
rects2 = ax.bar(ind + width/2, f2, width, 
                label=flight2)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Delay (mins)')
ax.set_title('Delay of Flights')
ax.set_xticks(ind)
#ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
ax.legend()


def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')


autolabel(rects1, "left")
autolabel(rects2, "right")

fig.tight_layout()

plt.show()