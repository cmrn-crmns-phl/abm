import plot_thickens as pt
import subprocess
import os


def dimensions():
    """ if this is 50x50, dimesnions = 50"""
    dimensions = 70
    return dimensions

def wolf_gn():
    fd = 30
    return fd

def radyis():
    """detection radius for consumer"""
    r = 6
    return r

def fmr_cost():
    c = 9
    return c

def initial_carcs():
    c = 5
    return 5

def saurp_mass():
    m = 45000
    return m

def allsr_reprd_rte():
    m = .02
    return m

def saurp_rprd_rate():
    r = .82
    return r



metab_dkt = {9.04   :"1000kg_varanid"
            ,17.04  :"2000kg_varanid"
            ,5.94   :"1000kg_reptile"
            ,11.01  :"2000kg_reptile"
            ,18     :"1000kg_bird"
            ,28     :"2000kg_bird"
            ,17.17  :"1000kg_mammal"
            ,28.57  :"2000kg_mammal"}
    # """<== notes:
    #    Gene A - max between 1500 and 1750,
    #    Gene B - max between 1600 and 2200 kg.
    #    make their energy needs conditional within each object based on Nagy
    #    Gene C - 35% chance to kill on contact of living sauropod 25% to be killed, rest of % draw
    #    Gene D - 25% chance to kill on contact of living sauropod 35% to be killed, rest of % draw"""
def summary(dmnsn, wolf_gn, rdius, fmr_cost, intl_crcs, intl_als
            , saurp_mass, carcass_apprnce_rte, totl_allsrs, totl_crcs
            , mx_pop_allsr):

    """extinct=TRUE if days didn't reach 365
       competition = TRUE if multiple phenotypes compete for resources"""

    thrtcl_max_allsrs =  ((saurp_mass * totl_crcs)/365)/fmr_cost
    txt = "Results\n"+\
    "dimensions                     : "+str(dmnsn)+"x"+str(dmnsn)+" squares at 1km each\n"+\
    "area                           : "+str(dmnsn * dmnsn)+ "sq km\n"+\
    "mass & metabolism              : "+str(metab_dkt[fmr_cost])+"\n"+\
    "fmr                            : "+str(fmr_cost)+"kg / day\n"+\
    "max food consumption rate      : "+str(wolf_gn)+"kg/day \n"+\
    "carcass detection radius       : "+str(rdius)+"km\n"+\
    "initial allosaur population    : "+str(intl_als)+"\n"+\
    "initial carcass population     : "+str(intl_crcs)+"\n"+\
    "max carcass mass               : "+str(saurp_mass)+"\n"+\
    "average distance of carcass when first detected : \n"+\
    "percent of allosaurs out of range:\n"+\
    "percent of allosaurs with gene : A  [start , end]\n"+\
    "percent of allosaurs with gene : B  [start , end]\n"+\
    "percent of allosaurs with gene : C  [start , end]\n"+\
    "percent of allosaurs with gene : D  [start , end]\n"+\
    "allosaur reproduction rate / step :\n"+\
    "decay euqation                 : rep = ( -87/(1+ math.exp(-0.208506*n + 6.1256) ) + 100 )\n"+\
    "disappear when mass between 0 and 15000kg (25% of initial mass)\n"+\
    "rate of carcass appearance     : "+str(carcass_apprnce_rte)+"/day\n"+\
    "\n"+\
    "total allosaurs made           : "+str(totl_allsrs)+"\n"+\
    "---allosaurs pop plateau reached at day 160 ish, between 1750-1899---\n"+\
    "total carcasses                : "+str(totl_crcs)+"\n" +\
    "actual max of allosaurs        : "+str(mx_pop_allsr)+"\n" +\
    "theoretical max of allosaurs   : "+str( thrtcl_max_allsrs )+"\n" +\
    "In gross terms "+str(totl_crcs)+" carcasses at "+str(saurp_mass)+" kg is enough to feed "+ str( ((saurp_mass * totl_crcs)/365)/fmr_cost ) +" allosaurs\n"+\
    "-- "+str(mx_pop_allsr)+" is "+str( (mx_pop_allsr-thrtcl_max_allsrs)/thrtcl_max_allsrs )+"% of theoretical max\n"+\
    "total living adult sauropod pop: "+str(totl_crcs*20)+"\n"+\
    "sauropod density               : "+str( ((totl_crcs/3)*10)/(dmnsn * dmnsn))+" / km2\n"+\
    "allosaur density               : "+str( mx_pop_allsr/(dmnsn * dmnsn))+ " /km2\n"+\
    "number of unmet carcasses      :\n"+\
    "allosaurs that starved         :\n"+\
    "avg swarm size per carcass     :\n"

    print(txt)
    print(os.path.dirname(os.path.realpath(__file__)))

    new_path = os.path.dirname(os.path.realpath(__file__))+"/"+str(metab_dkt[fmr_cost])
    print(new_path)
    #
    subprocess.call("mkdir "+new_path, shell=True)
    #
    "45000kg_saurp-extinct-FALSE-competition-TRUE.txt"
    f= open(new_path+"/45000kg_saurp-extinct-FALSE-competition-TRUE.txt","w+")

    f.write(txt)




    #
    #
    # """ at mass 2000kg, 45kg sauropods support 5969 carnosaurs at sauropod adult pop 30k (total popl 100)
    #     that ratio is 6:10
    #
    #     so far, a pop of 10k saurops in the simulation has sustained 1750 allosaurs at once but total of 3670 created.
    #     that really makes sense
    #
    #     update: K might be 1500-1750 , 273 carcasses"""


if __name__=="__main__":

    summary(70, 20, 6, 9.04, 13, 10, 45000, .82, 6000, 299, 1720)
