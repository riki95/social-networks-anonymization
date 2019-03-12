

def hi(g, i: int):
    neighbors = {n: knbrs(g, n, i-1) for n in g.nodes()}

    res = {}
    for k,v in neighbors.items():
        if i == 0:
            res[k] = [0]
        else:
            res[k] = sorted([g.degree(n) for n in v])
    
    return res


def knbrs(g, start, k):
    nbrs = set([start])
    for i in range(k):
        nbrs = set((nbr for n in nbrs for nbr in g[n]))
    return nbrs


