import numpy as np
import math

def others(n=None):
    all_mults = [0.005,0.01,0.025,0.05,0.075,0.1,0.125,0.15,1/6,0.175,0.2,0.25,0.3,1/3,0.5,0.7]

    m_multipliers = [-0.15,0.005,0.01,0.025,0.1,0.15,1/6,0.175,0.2,0.25,1/3,0.5,0.7]

    r_multipliers = [-0.2,0.025,0.05,0.075,0.1,0.125,0.15,1/6,0.2,0.25,0.3,0.5]

    mg_multipliers = [0.15,0.2,0.25,0.3,0.5]

    multipliers = m_multipliers

    # 0.21 bgs is .1*.1
    # 0.375 ags is .1*.25 or .25*.1???

    mult_array = 1 + np.asarray(multipliers)

    dmg_vals = np.arange(1,70)

    first = np.outer(dmg_vals, mult_array).astype("intc")  # this returns a len(mult_array)*len(dmgvals) array

    everything = (first[...,None] * mult_array).astype("intc")

    tee = everything.transpose(0,2,1)

    nonzero = everything - tee

    nonzero = np.moveaxis(nonzero, 0,-1)  # move dmg_vals to last dimension
    print_mult(nonzero, multipliers, n)

def print_mult(nonzero, multipliers, n = None):
    if n is not None:
        try:
            m = [multipliers.index(float(n))]
        except ValueError as e:
            raise e
    else:
        m = range(len(multipliers))

    for i in m:
        for j in range(i+1,len(multipliers)):
            places = np.argwhere(nonzero[i][j])
            if len(places) > 0:
                pos = np.where(nonzero[i][j] < 0, nonzero[i][j], 0)
                pos_only = np.argwhere(pos)
                neg = np.where(nonzero[i][j] > 0, nonzero[i][j], 0)
                neg_only = np.argwhere(neg)
                print(f"{multipliers[i]} * {multipliers[j]} differs in {len(places)} places: \n  {pos_only.flatten() + 1},\n  {neg_only.flatten() + 1}")
            else:
                print(f"{multipliers[i]} * {multipliers[j]} can't distinguish")


def guards():
    reqs = [1,6,11,21,31,41,61]
    mining_lvl = 99
    dmg_multiplier = (50 + mining_lvl + reqs[0])/150
    pass

# confirmed bgs is 1.1*1.1, ags is 1.1*1.25 in that order
def gs():
    ags10 = []
    ags25 = []
    agsb = []
    for i in range(1,60):
        if math.trunc(math.trunc(i*1.1)*1.25) != math.trunc(i*1.375):
            ags10.append(i)
        if math.trunc(math.trunc(i*1.25)*1.1) != math.trunc(i*1.375):
            ags25.append(i)
        if math.trunc(math.trunc(i*1.25)*1.1) != math.trunc(math.trunc(i*1.1)*1.25):
            agsb.append(i)

    print("ags 10 first: ", ags10)

    print("ags 25 first: ", ags25)
    print("ags difference: ", agsb)

def add_or_mult():
    base = 0.25
    mult = 0.2
    for i in range(1,30):
        aa = math.trunc(math.trunc(i * (1+base))*(1+mult))
        b = math.trunc(i * (1+base+mult))
        if not aa == b:
            print(i, aa>b)

def gs2():
    mults = [0.005,0.01,0.025,1/6,0.2]
    # mults = mults[3:]
    for i in mults:
        print(i)
        for j in range(30,45):
            print(f"   {j}:")
            a = math.trunc(math.trunc(math.trunc(j*1.1)*1.1)*(1+i))
            b = math.trunc(math.trunc(math.trunc(j*(1+i))*1.1)*1.1)
            if not a == b:
                print(f"bgs first:", a, "otherwise ", b)
            a = math.trunc(math.trunc(math.trunc(j*1.1)*1.25)*(1+i))
            b = math.trunc(math.trunc(math.trunc(j*(1+i))*1.1)*1.25)
            if not a == b:
                print(f"ags first:", a, "otherwise ", b)

    pass

others(0.1)