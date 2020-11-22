from mesa import Agent
# from random_walk import RandomWalker
from wolf_sheep.random_walk import RandomWalker


import pandas as pd
import os
from os import path
import math
import random
from scipy import spatial
import networkx as nx

dfw = pd.DataFrame([])
dfs = pd.DataFrame([])
#
# dfw = pd.DataFrame(columns = ["adjacent_sheep","unique_id","step_no","resulting_energy","adjacent_sheep","reproduced","initial_energy","age"])
# dfs = pd.DataFrame(columns = ["consuming_wolves","unique_id","step_no","resulting_energy","adjacent_sheep","reproduced","initial_energy","age"])

        # dst= {"consuming_wolves"  :[str(len(wlvs))]
        #     , "unique_id"         :[str(self.unique_id)]
        #     , "initial_energy"    :[str(nrg)]
        #     ,"resulting_energy"   :[str(nw_nrg)]
        #     ,"reproduced"         :[str(rprd)]
        #     ,"step_no"            :[str(self.model.schedule.time)]
        #     ,"steps_alive"        :[str(self.stps_alive)]}
# if not path.exists("data_sheet.csv"):
#     dfw.to_csv("data_sheet.csv")

class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.
    The init is the same as the RandomWalker. the time thing must be related to this_cell
    """

    energy = None



    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

        # if self.energy>45000:
        #     self.energy =45000
        self.energy +=45000


        # print("sheep energy is "+ str(self.energy))
        """the sheep's lifespan is len(dfs[dfs["unique_id"]==unique_id])
        I need to solve this datafraem problem"""




    def step(self):

        def decay_equation(n):
            rep = ( -87/(1+ math.exp(-0.208506*n + 6.1256) ) + 100 )

            # print(rep)

            return rep/100




        data = pd.read_csv("sheep_data_sheet.csv")

        da = data[data["unique_id"]==self.unique_id]

        self.age = len(da.index)


        """
        A model step. Move, then eat grass and reproduce.

        But for me it will be each step the sheep loses energy according to the decay equation.
        I need to record the number of days the sheep has existed by step.
        """
        # self.random_move()
        living = True

        nrg = self.energy
        # rprd="false"

        self.energy *= decay_equation(self.age)

        nw_nrg = self.energy

        """if self.model.schedule.time between 1 and 90, it is spring
        if between 270 and 365, reproduce"""

        """i definitely need the list of adjacent wolves because i need to demonstrate that multiple wolves profit
           from a single carcassj
           and i can't forget to measure how many steps they take avg to find a carcass
           and I need to make them stay at a carcass once they find  it,"""
        this_cell = self.model.grid.get_neighbors(pos=self.pos,moore=True,radius=5)

        wlvs = [obj for obj in this_cell if isinstance(obj, Wolf)]

        if self.energy < 9000:

            """9000 kg is 20% of the original mass of the carcass
               when it becomes effectively useless to local animals.
               At that point, it is mostly bones and inedible elements
               """

            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        if self.model.grass:
            # Reduce energy by a certain amount

            # If there is grass available, eat it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in this_cell if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                self.energy += self.model.sheep_gain_from_food
                grass_patch.fully_grown = False

            # Death


        print(da["reproduced"].tolist())
        rprd = "false"
        print(self.age)

        if self.age == 1:

            """if the carcass hasn't reproduced yet, make a new carcass
               otherwise collect the data and do nothing"""

            rprd="true"
            # Create a new sheep:
            """if each sheep reproduces 1 time, and i start with 4 sheep, it will
                add only 4 sheep per step.  the existing sheep will decay and die."""

            """i might need to make this produce like 2 carcasses per day
               based on 100k kg average carrion production per day.
               if only 5 die every year

               if 1.5 animals died per day at 45000kg each, that would be avg 180kg per day
               I'll need to do it this way to demonstrate algebraic supply demand
               but
               """
            # self.nwnrg = random.randrange(20000,45000)

            # print(self.nwnrg)

            lamb = Sheep(self.model.next_id(), self.pos, self.model, self.moore, 1)

            nx = random.randrange(100)
            ny = random.randrange(100)

            self.npos = (nx,ny)

            print(self.npos)

            self.model.grid.place_agent(lamb, self.npos)

            self.model.schedule.add(lamb)

        dst= {"consuming_wolves"  :[str(len(wlvs))]
            , "unique_id"         :[str(self.unique_id)]
            , "initial_energy"    :[str(nrg)]
            ,"resulting_energy"   :[str(nw_nrg)]
            ,"reproduced"         :[str(rprd)]
            ,"step_no"            :[str(self.model.schedule.time)]
            ,"age"                :[str(self.age)]}

        dsx = pd.DataFrame(dst)
        # print("DFX")
        # print(dsx)
        dsx.to_csv("sheep_data_sheet.csv",mode="a",header=False)


        dfs.append(dsx, ignore_index=True)
        # dfs.to_csv("sheep_data_sheet.csv",mode="a")


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

        # if self.energy>45000:
        #     self.energy =45000
        """how much energy should the wolves start with?
           should it be 1000 kg? yes
           and depending on metabolism

           okay so this is good: a monitor lizard loses 0.2 % of its mass every day it goes without eating
           after 168 days of no food, it dies, having lost 29% of its body mass.

           i need to check this citation. if 0.2% of body mass is near its FMR ,

           i think if the allosaur gets to 70% body mass as an ectotherm, it dies.
           that is pretty generous so i should do this with a range of values... even if it could only go 10 days wihtout food it dies

           this is another great citation
           Huitu, O.; Koivula, M.; Korpimäki, E.; Klemola, T. & Norrdahl, K. (2003) “Winter food supply limits growth of northern vale populations in the absence of predation”, Ecology, 84, pp. 2108-2118.

           this paper is outstanding:
           starvation physiology:
           https://www.sciencedirect.com/science/article/pii/S109564331000005X?casa_token=ZrU6VR5dfeYAAAAA:1fRVw4gypP82tqjz72Rwuo6E160PMW_2ocdHRRnjSTMClCJCHklwaQIGjZXROQkqJco_ZBzIEQ
           section 1.3
           also for bird and mammal physiology they can only go like 5 days wihtout food, arbitrary but good

           """

        self.energy +=1000

    def step(self):

        def path_to_closest_sheep(crnt_crdnt,trgt_crdnt):

            G = nx.grid_2d_graph(100,100)

            # coor1= self.pos
            # coor2 = sheep.pos

            pth = nx.bidirectional_shortest_path(G, source=crnt_crdnt, target=trgt_crdnt)

            # print(pth)

            return pth[1]

        """ life cost is 9kg / day for 1000kg varanid metabolism"""
        self.energy -= 9
        nrg = self.energy
        """ it costs self.energy to move"""

        data = pd.read_csv("wolf_data_sheet.csv")

        da = data[data["unique_id"]==self.unique_id]

        self.age = len(da.index)

        x, y = self.pos

        """radius = 10 km because
           komodo dragons can smell carcasses 10km away
           brown bears may be at 20km but email here for sources: heiko jansen bear smell
           the other thing is that giant rotting sauropods must have smelled awful"""
        this_cell = self.model.grid.get_neighbors(pos=self.pos,moore=True,radius=10)
        # this_cell = self.model.grid.get_cell_list_contents([self.pos])

        """ the given list of sheep in adjacent cells with self.model.grid.get_cell_list_contents is inaccurate.
            self.model.grid.get_neighbors is better
        2020 9 17 and i can't forget to measure how many steps they take avg to find a carcass
        and I need to make them stay at a carcass once they find  it,"""

        sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]

        nw_nrg = self.energy

        if len(sheep) > 0:

            """this captures the list of all sheep within 5 step radius of the wolf
                wolves need to go toward the closest one, and this can't damage self.random_move() at 89
                but i may need to say if sheep within radius 5, move. else random_move and flip the order
                of actions"""

            cls_shp = []

            for ps in sheep:
                """this is the list of sheep objects the wolf can detect based on detection radius=5 in line 217"""
                cls_shp.append(ps.pos)

            tree = spatial.KDTree(cls_shp)

            arr = tree.query([self.pos])

            clsst_shp = arr[1][0]

            sheep_to_eat = sheep[clsst_shp]
            # print("SHEEP TO TARGET:")
            # print(sheep_to_eat)
            #
            # print("SHEEP TO TARGET COORDINATES:")
            # print(sheep_to_eat.pos)

            to_trgt = path_to_closest_sheep(self.pos,sheep_to_eat.pos)

            self.non_random_move(to_trgt)

            # sheep_to_eat = self.random.choice(sheep)
            """ if the sheep is NOT adjacent to the wolf square,
                move toward it
                else
                don't move at all adn keep eating"""
            # print(sheep)

            start_e = sheep_to_eat.energy

            """make a dataframe to record the actions of each agent, if they ate, etc.  """

            # print("sheep from wolf perspective has  " +str()+ " energy")
            """this selects the random sheep to be consumed """
            self.energy += self.model.wolf_gain_from_food
            sheep_to_eat.energy -= self.model.wolf_gain_from_food

            nw_nrg = self.energy

        else:

            self.random_move()

        # Death or reproduction
        rprd = "false"

        """ if the reptile allosaur's body mass drops by 30%, it dies.
            just as in monitor lizards"""
        if self.energy < 700:

            self.model.grid._remove_agent(self.pos, self)

            self.model.schedule.remove(self)

        else:
            """ reproduce if wolf energy is greater than 270 (1 month of food survival?)
                or
                reproduce if step is between 275-280 for breeding season"""

            if self.model.schedule.time > 275 and self.model.schedule.time < 280:
            # if self.random.random() < self.model.wolf_reproduce:
                # Create a new wolf cub
                """self.energy/=2 divides the wolf's energy by 2 as a cost of having a cub, i don't want this because dinosaurs laid eggs"""
                self.energy *= 0.85

                """new wolves start with 1+1000 energy"""

                cub = Wolf(self.model.next_id(), self.pos, self.model, self.moore, 1)

                self.model.grid.place_agent(cub, cub.pos)

                self.model.schedule.add(cub)

                rprd = "true"

        dkt= {"adjacent_sheep"  :[str(len(sheep))]
            , "unique_id"       :[str(self.unique_id)]
            , "initial_energy"  :[str(nrg)]
            , "resulting_energy" :[str(nw_nrg)]
            , "reproduced"       :[str(rprd)]
            ,"step_no"           :[str(self.model.schedule.time)]
            ,"age"               :[str(self.age)]}

        dfx = pd.DataFrame(dkt)
        # print("DFX")
        # print(dfx)
        dfx.to_csv("wolf_data_sheet.csv",mode="a",header=False)

        # dfw.append(dfx, ignore_index=True)
        # dfw.to_csv("wolf_data_sheet.csv",mode="a")


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass
        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1


def function_test():
    print("test")
