import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import simps
from numpy import trapz
from itertools import count

from matplotlib.animation import FuncAnimation

from mpl_toolkits import mplot3d

# import matplotlib.animation as animation
import time


"""from sauropod sheet
   get nunique unique_ids for total number of carcasses,
   then compute number of sauropods that could make nunique items
   graph individuals w/ decay patterns
   graph total amount of food
   number unused carcasses
   density of carcasse / sq mile
   against estimated values
   comput ratio of carnosaurs to sauropods
   population changes over time AND
   the fact that they spiked at birth , then dropped because babies only had 10 days of travel reserves to find a new carcass
   and some of them couldn't do it in time.
   this really makes sense anyway because the babies had to rely on carcasses to survive,
   there is no effing way 2ft long juvenile allosauyrs hunted anything
   NOTE I ALSO NEED TO DO A SINGLE CARCASS VS A SINGLE POPULATION OF ALLOSAURS TO SEE HOW THE CARCASS RESPONDS TO MULTIPLE ANIMALS W/ and W/OUT COMPETITION
   THIS SHOULD BE A 10x10 PLOT WITH A SINGLE CARCASS"""


def plot_sauropods():
    df = pd.read_csv("sheep_data_sheet.csv")
    """205 carcasses over 171 days is 1.19 mortalities/ day. that is really good.
    there must be a point at which density of carcasses is high enough to support allosaurs

    I need to run this model for each metabolism where 1 dead sauropod and n number of allosaurs eat it. then get the data
    about how carcasses are consumed  with COMPETITION"""
    print(df["unique_id"].nunique())

    # step_no = x axis
    # enrgy = y axis
    # unique_id = columns

    df = df[["step_no","initial_energy","unique_id"]]

    df = df.pivot(index='step_no', columns='unique_id', values='initial_energy')
    df.plot(kind="line")
    plt.show()

def sauropod_neighbors():
    df = pd.read_csv("sheep_data_sheet.csv")

    df = df[["step_no","consuming_wolves"]].groupby(["step_no"]).sum()
    df = df.reset_index()
    df.columns =["step_no","allosarus_at_carcass"]
    return df

def sauropod_data():
    df = pd.read_csv("sheep_data_sheet.csv")
    "unique sauropod carcasses"
    print("ttl sauropods")



    ttl_saurp = df["unique_id"].nunique()
    print(ttl_saurp)

    # print(df.head())

    # df = df[["step_no","unique_id"]]

    # tfr = df[df["step_no"]==24]
    # print(tfr.groupby(["initial_energy"]).mean())
    #
    # print(len(tfr.index))
    #
    # tfv = df[df["step_no"]==25]
    # print(tfv.groupby(["initial_energy"]).mean())
    #
    # print(len(tfv.index))
    #
    # ts = df[df["step_no"]==26]
    # print(ts.groupby(["initial_energy"]).mean())
    #
    # print(len(ts.index))
    #
    df = df.groupby(["step_no"]).count()
    #
    df = df.reset_index()

    df["animal"]="sauropod"

    df =df[["step_no","unique_id","animal"]]

    df.columns = ["step_no","count","animal"]
    print(df)


    return df

def plot_allsr_vs_carcass():
    df = pd.read_csv("wolf_data_sheet.csv")
    # print(df[df["step_no"]==1])
    # df = df.groupby(["unique_id"]).sum() <== this is maybe good to see how each allosaur fared
    "unique allosaur carcasses"
    print("ttl allosaurs")
    ttl_allsr = df["unique_id"].nunique()
    print(ttl_allsr)

    df_saurp = sauropod_data()

    # print(df)
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    df["animal"]="allosaur"
    print(df)
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","count","animal"]
    # print(df)

    neighbs = sauropod_neighbors()

    # neighbs = dict(zip(neighbs["step_no"],neighbs["consuming_wolves"]))

    # df = df.reset_index()
    # df = df[["step_no","unique_id"]]
    # df["srp"] = df["step_no"].map(sauropod_map())
    # df.columns = ["step_no","allsr","srp"]

    df = df.append(df_saurp,ignore_index=True)
    print(df)

    # #
    # area = trapz(lst_allsr, dx=5)
    # print("area =", area)
    # df = df.pivot(index='x', columns='color', values='y')
    df = df.pivot(index='step_no', columns='animal', values='count')


    fig, ax = plt.subplots()

    df.plot(kind="line",ax=ax)
    neighbs.plot(kind="line",y="allosarus_at_carcass",ax=ax)

    ax.set_xlabel("Step Number")
    ax.set_ylabel("Population")

    plt.title("allosaur population vs carrion supply over time")
    # ani = animation.FuncAnimation(fig, animate, interval=1000)

    plt.show()

#
# srp = sauropod_data()
# x_values = []
# y_values = []
# z_values = []
# q_values = []
# counter = 0
# index = count()
#
# def animate(i):
#
#
#     #print(counter)
#     dfw = pd.read_csv("wolf_data_sheet.csv")
#     dfw = dfw.groupby(["step_no"]).count()
#     dfw = dfw.reset_index()
#     dfw["animal"]="allosaur"
#     dfw =dfw[["step_no","unique_id","animal"]]
#     dfw.columns = ["step_no","count","animal"]
#
#     dfsh = pd.read_csv("sheep_data_sheet.csv")
#     dfs = dfsh.groupby(["step_no"]).count()
#     dfs = dfs.reset_index()
#     dfs["animal"]="allosaur"
#     dfs =dfs[["step_no","unique_id","animal"]]
#     dfs.columns = ["step_no","count","animal"]
#
#     df_c = dfsh[["step_no","consuming_wolves"]].groupby(["step_no"]).sum()
#     df_c = df_c.reset_index()
#     df_c.columns =["step_no","allosaurs_at_carcass"]
#
#     x = next(index) # counter or x variable -> index
#     counter = next(index)
#     print(counter)
#     x_values.append(x)
#     '''
#     Three random value series ->
#     Y : 0-5
#     Z : 3-8
#     Q : 0-10
#     '''
#     y = dfw["count"].iat[-1]#random.randint(0, 5)
#     z = dfs["count"].iat[-1]
#     q = df_c["allosaurs_at_carcass"].iat[-1]
#     # append values to keep graph dynamic
#     # this can be replaced with reading values from a csv files also
#     # or reading values from a pandas dataframe
#     y_values.append(y)
#     z_values.append(z)
#     q_values.append(q)
#
#
#     if counter >3:
#         '''
#         This helps in keeping the graph fresh and refreshes values after every 40 timesteps
#         '''
#         x_values.pop(0)
#         y_values.pop(0)
#         z_values.pop(0)
#         q_values.pop(0)
#         #counter = 0
#         plt.cla() # clears the values of the graph
#
#     plt.plot(x_values, y_values)
#     plt.plot(x_values, z_values)
#     plt.plot(x_values, q_values)
#     fig, ax = plt.subplots()
#
#
#     # ax.legend(["Value 1 ","Value 2","Value 3"])
#     ax.set_xlabel("Step Number")
#     ax.set_ylabel("Population")
#     plt.title('allosaur population vs carrion supply over time')

def pop_check():

    return 6/5

if __name__=="__main__":

    # ani = FuncAnimation(plt.gcf(), animate, 1000)
    # plt.tight_layout()
    # plt.show()

    # print(pop_check())

    # sauropod_neighbors()
    plot_allsr_vs_carcass()
    # sauropod_data()
    # plot_allsr_vs_carcass()



    # plot_sauropods()

    # plot_allsr_vs_carcass()
