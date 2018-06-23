# coding: utf-8

import networkx as nx
import numpy as np
from queue import Queue
from time import time
from typing import List

from informationFlow import Net


def dfs(g: nx.DiGraph, sources: List):
    influence = {s: 0 for s in sources}
    for s in sources:
        count = 0
        arrive = np.zeros(nx.number_of_nodes(g))
        tocheck = Queue(nx.number_of_nodes(g))

        arrive[s] = 1
        tocheck.put_nowait(s)
        while not tocheck.empty():
            u = tocheck.get_nowait()
            listener = g.predecessors(u)
            for v in listener:
                if arrive[v] == 0:
                    arrive[v] = arrive[u]*g[v][u]['Eprob']
                    count = count+1
                    tocheck.put_nowait(v)
                else:
                    arrive[v] = 1-(1-arrive[v])*(1-arrive[u]*g[v][u]["Eprob"])
        influence[s] = np.sum(arrive)
        print("%f s: Influence of user %d is %f. He influences %d people. "
              % (time()-start_time, s, influence[s], count))
    return influence


def main(path="./Graph2k.pickle"):
    global start_time
    start_time = time()

    g = nx.read_gpickle(path)   # type: nx.DiGraph
    print("%f s: Load graph. " % (time()-start_time))
    net = Net(g)
    print("%f s: Prepare delay time and prob. " % (time()-start_time))

    pr = nx.pagerank_numpy(g)
    pr = sorted(pr, key=lambda key: pr[key])
    print("%f s: Get pagerank and sort user according to it. " % (time()-start_time))

    indegree = [g.in_degree[node] for node in pr]
    influence = dfs(g, pr[:20])
    pass


if __name__ == '__main__':
    main()