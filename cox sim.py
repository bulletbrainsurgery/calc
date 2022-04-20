import random
import sys

def run(seed = None):
    if seed is None:
        seed = random.randrange(sys.maxsize)

    uniques = set()
    unique_kcs = {}

    random.seed(seed)

    i = 0
    purples = 0
    olmlet = {}

    weights = {"dex":20,"arcane":20,"dhcb":4,"buckler":4,"dinhs":3,"anc hat":3,"anc top":3,"anc legs":3,"claws":3,"kodai":2,"maul":2,"tbow":2}
    total_weight = 0
    for k, v in weights.items():
        total_weight += v

    while True:
        if len(uniques) == 12 and len(olmlet) > 0:
            break
        i += 1
        if random.random() < 30/867.5:
            purple = None
            purples += 1
            j = random.randint(1,total_weight)
            for k, v in weights.items():
                if j < v:
                    purple = k
                    if k not in uniques:
                        uniques.add(k)
                        unique_kcs[k] = i
                    break
                else:
                    j -= v
            if random.randint(1,53) == 1:
                olmlet[i] = purple

    print(f"""ending kc: {i}
    total purples: {purples}
    uniques: {unique_kcs}
    olmlet/s: {olmlet}
    rng seed: {seed}
    """)

run()