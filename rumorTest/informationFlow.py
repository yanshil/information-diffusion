# coding: utf-8

# # 算法思路
# 不去直接根据时间来分析这个传播过程,而是从每一个消息源头开始,生成一次边图(这样才能具有随机性);根据生成的边图,求出消息源转发到达各个节点的时间.统计能到达的节点以及到达的时间
# 
# 那么根据所有的消息源头,就可以求得所有消息到达的情况,可以统计出每一个时刻,每一个人收到的消息数,这就是我们想要的结果
# 

# In[126]:


import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from IPython import get_ipython

# get_ipython().magic(u'matplotlib inline')
from numpy.random import (random, randint, seed)
import math

Inf = 999999
seed(0)


class Net(object):
    def __init__(self, G):
        self.Num = nx.number_of_nodes(G)
        self.PersonList = nx.nodes(G)
        self.EdgeList = nx.edges(G)
        self.G = G

        # 随机生成各个点的政治属性
        self.policy = {node: random()*200-100 for node in self.PersonList}
        nx.set_node_attributes(self.G, self.policy, name='policy')  # 均匀分布（可调试）
        # 随机生成每条边的延迟时间
        self.delayTime = {edge: randint(1, 10) for edge in self.EdgeList}
        nx.set_edge_attributes(self.G, self.delayTime, name='weight')
        # 随机生成每条边的激活概率
        self.Eprob = {edge: random() for edge in self.EdgeList}
        nx.set_edge_attributes(self.G, self.Eprob, name='Eprob')

        # 根据延迟时间布局
        # self.pos=nx.kamada_kawai_layout(self.G,weight='weight') # positions for all nodes

    def Spread(self, sourceList, poliTendency):
        '''
        输入消息源头,
        返回Rec[PersonNum][Time]表示person在t时刻**总共**接收到的消息数
        返回poliRed[PersonNum][Time]表示person在**t时刻**接收到的红营推送数
        返回poliBlue[PersonNum][Time]表示/// 蓝///
        '''
        #         对于每一个消息源头,先随机生成一次图
        #         根据随机生成的图跑一次最短路径算法
        #         得到每一个节点收到消息的时间,没收到用大数表示
        MaxTime = 100
        Rec = np.zeros([self.Num, MaxTime])
        politicRed = np.zeros([self.Num, MaxTime])
        politicBlue = np.zeros([self.Num, MaxTime])
        count = 0
        for source in sourceList:
            weightn = {}
            # 模拟只传播一次
            for edge in self.EdgeList:
                weightn[edge] = self.delayTime[edge] if random() > self.Eprob[edge] else Inf
            nx.set_edge_attributes(self.G, weightn, name='weightn')
            SpreadTime = nx.shortest_path_length(self.G.reverse(copy=False), source=source, weight='weightn')
            for (person, time) in SpreadTime.items():
                if time < MaxTime:
                    Rec[person][time:] += 1
                    if poliTendency[count] == 1:
                        politicRed[person][time] += 1
                    else:
                        politicBlue[person][time] += 1
            count += 1
        return Rec, politicRed, politicBlue

    def Change(self, Rec, politicRed, politicBlue):
        '''
        输入各个时刻的收到的消息数
        返回各个时刻的政治立场
        '''
        m, n = Rec.shape
        PoliChange = np.zeros([m, n])
        print(m, n)
        for person in self.PersonList:
            PoliChange[person, 0] = self.policy[person]
        # PoliChange[:, 1:] = np.minimum(1, PoliChange[:, 0:-1] + 0.05 * Rec[:, 1:])
        for t in range(n - 1):
            PoliChange[:, t + 1] = np.clip(PoliChange[:, t] + 0.1*politicRed[:, t+1] - 0.1*politicBlue[:, t+1],
                                           -1000, 1000)     # 越靠近1约red
        PoliChange = 1/(1+np.exp(-0.01*PoliChange))
        # TODO:
        # p.s. 上面这句话怎么向量化。。。 如何用generator遍历dict?
        PoliMap = np.average(PoliChange, 0)

        return PoliMap

    def Show(self):
        plt.figure(figsize=(18, 18))
        nx.draw_networkx_edges(self.G, self.pos, alpha=0.3)
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=self.policy.keys(),
                               node_size=200,
                               cmap=plt.cm.RdBu)
        plt.axis('off')
        plt.show()


def mulDiGraph2DiGraph(M):
    # create weighted graph from M
    G = nx.DiGraph()
    for u, v, data in M.edges(data=True):
        w = data['weight'] if 'weight' in data else 1.0
        if G.has_edge(u, v):
            G[u][v]['weight'] += 0
        else:
            G.add_edge(u, v, weight=0)
    return G


if __name__ == '__main__':
    popNum = 2000
    sourceNum = 100

    # Gra = nx.fast_gnp_random_graph(popNum,0.05,seed=None,directed=True)
    # Gra = nx.scale_free_graph(popNum)
    # Gra = mulDiGraph2DiGraph(Gra)
    Gra = nx.read_gpickle('./Graph2k.pickle')
    print("after loading graph from pickle")
    net = Net(Gra)
    # net.Show()
    print("after setting graph attributes")

    cmap = plt.cm.get_cmap('rainbow', 1000)
    sourceList = [randint(0, popNum - 1) for i in range(sourceNum)]
    # print(sourceList)
    poliTendency = np.array([0 * i for i in range(math.floor(sourceNum / 2))])
    poliTendency = np.append(np.array([1 ** i for i in range(math.floor(sourceNum / 2))]),
                             np.array([0 * i for i in range(math.floor(sourceNum / 2))]))  # 0 for red and 1 for blue
    # print(poliTendency)
    Rec, poliRed, poliBlue = net.Spread(sourceList, poliTendency)
    plt.imshow(np.sort(Rec, axis=0), interpolation='nearest', cmap=cmap, aspect='auto')
    plt.colorbar()
    plt.xlabel('Time')
    plt.ylabel('User ID')
    plt.title('Receiving Message Situation for All Users')
    plt.show()

    PoliMap = net.Change(Rec, poliRed, poliBlue)
    plt.plot(PoliMap)
    plt.xlabel('Time')
    plt.ylabel('Political Value')
    plt.title('Political Attitude')
    plt.axis([0, Rec.shape[1], 0.4, 0.6])
    plt.show()

#    net.Spread([0,1,2,3,4,5])


# In[132]:


# Rec.max()


# In[127]:


# nx.get_edge_attributes(net.G,name='weightn')


# plt.plot(Rec[])


# In[128]:


# net.Change(Rec)


# In[109]:


# Rec
