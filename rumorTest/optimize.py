# coding: utf-8

import networkx as nx
import numpy as np
from queue import Queue
from time import time
from typing import (List, Any)
from numpy.random import (random, randint, seed, choice)
import matplotlib.pyplot as plt
import os
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy

from informationFlow import Net

seed(0)


def dfs(g: nx.DiGraph, sources: List):
    influence = {s: 0 for s in sources}
    weight = nx.get_node_attributes(g, "policy")
    weight = list(weight.values())
    weight = np.array(weight)
    weight = 0.01*np.exp(-0.01*weight)/np.square(1+np.exp(-0.01*weight))
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
        influence[s] = np.sum(arrive*weight)
        print("%f s: Influence of user %d is %f. He influences %d people. "
              % (time()-start_time, s, influence[s], count))
    return influence


def simu_and_plot(net: Net, source: List, tendency: List, name="temp", path="./picture", show=False):
    seed(0)
    Rec, politicRed, politicBlue = net.Spread(source, tendency)
    print("%f s: Simulation %s. " % (time() - start_time, name))

    # figure for spread
    cmap = plt.cm.get_cmap('rainbow', 100)
    plt.imshow(np.sort(Rec, axis=0), interpolation='nearest', cmap=cmap, aspect='auto', vmin=0, vmax=43)
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
    # plt.axis([0, Rec.shape[1], 0.45, 0.55])
    plt.savefig(os.path.join(path, name + "_result.png"))
    if show:
        plt.show()
    else:
        plt.clf()
    return Rec


def develop(rec_1: np.ndarray, rec_2: np.ndarray, rec_3: np.ndarray, path="./picture"):
    def count_times(rec: np.ndarray, maxcount: int):
        c = np.zeros((maxcount, rec.shape[1]))
        for t in range(rec.shape[1]):
            for i in range(maxcount):
                rec_temp = rec[:, t]
                c[i, t] = rec_temp[rec_temp == i].size
        return c

    max_rec = np.max([rec_1, rec_2, rec_3])
    rec_1 = count_times(rec_1, int(max_rec))
    rec_2 = count_times(rec_1, int(max_rec))
    rec_3 = count_times(rec_1, int(max_rec))

    fig_mpl, ax = plt.subplots(1, figsize=(5, 3), facecolor='white')    # type: Any, plt.Axes
    ax.set_title("Information spread")
    ax.set_ylim(0, 10)
    xx = np.linspace(1, max_rec, max_rec)
    line = ax.plot(xx, rec_1[:, 0], xx, rec_2[:, 0], xx, rec_3[:, 0])    # type: List[plt.Line2D]
    duration = rec_1.shape[1] / 20

    def make_frame_mpl(t):
        line[0].set_ydata(rec_1[:, int(round(t * 20))])
        line[1].set_ydata(rec_2[:, int(round(t * 20))])
        line[2].set_ydata(rec_3[:, int(round(t * 20))])
        return mplfig_to_npimage(fig_mpl)

    animation = mpy.VideoClip(make_frame_mpl, duration=duration)
    animation.write_gif(os.path.join(path, "all.gif"), fps=20)


def main(path="./Graph2k.pickle"):
    global start_time
    start_time = time()

    g = nx.read_gpickle(path)   # type: nx.DiGraph
    print("%f s: Load graph. " % (time()-start_time))
    net = Net(g)
    print("%f s: Prepare delay time and prob. " % (time()-start_time))

    pr = nx.pagerank_numpy(g)
    prlist = sorted(pr, key=lambda key: pr[key], reverse=True)
    print("%f s: Get pagerank and sort user according to it. " % (time()-start_time))
    selected_by_pagerank = prlist[:50]

    # # time for calculate network constraint is so long!!! I give up.
    # nc = nx.constraint(g)
    # nc = sorted(nc, key=lambda key: nc[key], reverse=True)
    # print("%f s: Get network constraint and sort user according to it. " % (time()-start_time))

    influence = dfs(g, prlist[:500])
    big_name = sorted(influence, key=lambda key: influence[key], reverse=True)
    print("%f s: Get influence of each celebrity. " % (time()-start_time))
    selected_by_influence = big_name[:50]

    # Stochastic policy
    blue_sources = list(choice(list(set(g.nodes)-set(selected_by_influence)-set(selected_by_pagerank)), 50))
    red_sources = list(choice(list(set(g.nodes)-set(blue_sources)), 50))
    rec_1 = simu_and_plot(net, red_sources+blue_sources, [1] * 50 + [0] * 50, "Stochastic")
    cost_1 = [pr[user] for user in red_sources+blue_sources]
    cost_1 = np.array(cost_1)
    cost_1 = np.sum(np.exp(100*cost_1))
    print(cost_1)

    # our policy
    rec_2 = simu_and_plot(net, selected_by_influence + blue_sources, [1] * 50 + [0] * 50, "Influence")
    cost_2 = [pr[user] for user in selected_by_influence + blue_sources]
    cost_2 = np.array(cost_2)
    cost_2 = np.sum(np.exp(100*cost_2))
    print(cost_2)

    # pagerank policy
    rec_3 = simu_and_plot(net, selected_by_pagerank + blue_sources, [1] * 50 + [0] * 50, "PageRank")
    cost_2 = [pr[user] for user in selected_by_pagerank + blue_sources]
    cost_3 = np.array(cost_2)
    cost_3 = np.sum(np.exp(100*cost_3))
    print(cost_3)

    # animation
    # develop(rec_1, rec_2, rec_3)


if __name__ == '__main__':
    main()