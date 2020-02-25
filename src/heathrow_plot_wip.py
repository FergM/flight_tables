import pickle

file_name = "heathrow_draft.p"

with open(file_name, "rb") as f2:
    loaded_df = pickle.load(f2)

print("\nLoaded Head is:\n", loaded_df.head())
print("Loaded Tail is:\n", loaded_df.tail())
print("\n\n")

#----------------------------
flight1 = "SN2096"#"AA141"#"UA921"
flight2 = "BA404"#"AA6144"


df1 = loaded_df.loc[loaded_df['flight_id'] == flight1, ["scheduled_datetime", "delay_mins"]]
df2 = loaded_df.loc[loaded_df['flight_id'] == flight2, ["scheduled_datetime", "delay_mins"]]

#Care about dates not datetimes (for this part now)
df1['scheduled_datetime'] = df1['scheduled_datetime'].apply(lambda x: x.date())
df2['scheduled_datetime'] = df2['scheduled_datetime'].apply(lambda x: x.date())

df1 = df1.set_index("scheduled_datetime")
df2 = df2.set_index("scheduled_datetime")

df1 = df1.rename(columns={"delay_mins": "delay_mins1"})

print(df1)
print(df2)

merged_df = df1.join(df2, how="inner") #outer to keep days where only one of them flew

#merged_df.delay_mins1.iloc[9] = float("nan")#17#Hack to handle none into floatnan

f1 = merged_df.delay_mins1.values
f2 = merged_df.delay_mins.values

import numpy as np 

f2 = list(f2)
f1 = list(f1)

print(f1)
print(type(f1))
for i in range(0,len(f1)-1):
    if f1[i] == None:
        f1[i] = float("nan")
print(f1)

for i in range(0,len(f2)-1):
    if f2[i] == None:
        f2[i] = float("nan")

print(merged_df)
print(f1)
print(f2)
print("--------------------")

###-----------hack to get diff
'''for i in range(0,len(f2)):
    f2[i] = f2[i]-f1[i]
for i in range(0,len(f2)):
    f1[i] = 0
print(len(f2))
print(len(f1))

print(f2)
print(f1)
'''
###-----------hack to get diff end

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