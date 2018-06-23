# coding: utf-8

import networkx as nx
import numpy as np
from queue import Queue
from time import time
from typing import List
from numpy.random import (random, randint, seed, choice)
import matplotlib.pyplot as plt
import os

from informationFlow import Net

seed(1)


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


def simu_and_plot(net: Net, source: List, tendency: List, name="temp", path="./picture", show=False):
    Rec, politicRed, politicBlue = net.Spread(source, tendency)
    print("%f s: Simulation %s. " % (time() - start_time, name))

    # figure for spread
    cmap = plt.cm.get_cmap('rainbow', 100)
    plt.imshow(np.sort(Rec, axis=0), interpolation='nearest', cmap=cmap, aspect='auto', vmin=0, vmax=35)
    plt.colorbar()
    plt.xlabel('Time')
    plt.ylabel('User ID')
    plt.title('Receiving Message Situation for All Users')
    plt.savefig(os.path.join(path, name+"_spread.png"))
    if show:
        plt.show()
    else:
        plt.clf()

    # figure for result
    PoliMap = net.Change(Rec, politicRed, politicBlue)
    plt.plot(PoliMap)
    plt.xlabel('Time')
    plt.ylabel('Political Value')
    plt.title('Political Attitude')
    plt.axis([0, Rec.shape[1], 0, 1])
    plt.savefig(os.path.join(path, name + "_result.png"))
    if show:
        plt.show()
    else:
        plt.clf()


def main(path="./Graph2k.pickle"):
    global start_time
    start_time = time()

    g = nx.read_gpickle(path)   # type: nx.DiGraph
    print("%f s: Load graph. " % (time()-start_time))
    net = Net(g)
    print("%f s: Prepare delay time and prob. " % (time()-start_time))

    pr = nx.pagerank_numpy(g)
    pr = sorted(pr, key=lambda key: pr[key], reverse=True)
    print("%f s: Get pagerank and sort user according to it. " % (time()-start_time))
    selected_by_pagerank = pr[:50]

    # # time for calculate network constraint is so long!!! I give up.
    # nc = nx.constraint(g)
    # nc = sorted(nc, key=lambda key: nc[key], reverse=True)
    # print("%f s: Get network constraint and sort user according to it. " % (time()-start_time))

    influence = dfs(g, pr[:200])
    big_name = sorted(influence, key=lambda key: influence[key], reverse=True)
    print("%f s: Get influence of each celebrity. " % (time()-start_time))
    selected_by_influence = big_name[:50]

    # Stochastic policy
    blue_sources = list(choice(list(set(g.nodes)-set(selected_by_influence)-set(selected_by_pagerank)), 50))
    red_sources = list(choice(list(set(g.nodes)-set(blue_sources)), 50))
    simu_and_plot(net, red_sources+blue_sources, [1] * 50 + [0] * 50, "Stochastic")

    # our policy
    simu_and_plot(net, selected_by_influence + blue_sources, [1] * 50 + [0] * 50, "Influence")

    # pagerank policy
    simu_and_plot(net, selected_by_pagerank + blue_sources, [1] * 50 + [0] * 50, "PageRank")


if __name__ == '__main__':
    main()