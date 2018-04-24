from Data import Node
from Data import Post
from Model import model

from typing import List
import numpy as np


class Test(object):
    """

    Attributes:
        model (Model):
        diffusionSize (List[int]):
        diffusionDuration (List[int]):

    """
    def __init__(self):
        self.model = None
        self.diffusionSize = None
        self.diffusionDuration = None

    def SampleRole(self, u):
        """Sample the role of user **u** *w.r.t.* his theta

        Args:
            u (int): index of user whose role is to be sampled

        Returns:
            role (int): role of user **u**

        """
        rolenum = self.model.roleNum
        p = np.array(self.model.theta[u][0:rolenum])
        role = np.random.choice(range(rolenum), size=1, p=p/np.sum(p))
        return role

    def SampleT(self, r):
        """Sample diffusion delay **T** *w.r.t.* role or user

        Args:
            r (int|Node): role if int, user if node

        Returns:
            t (int): diffusion delay

        """
        t = None
        if isinstance(r, Node):
            sum = 0
            for key in r.postIdList.keys():
                post = self.model.postList[r.postIdList[key]]   # type: Post
                sum += post.postTime - post.sourcePost.postTime
            t = sum/len(r.postIdList.keys())
            if t > self.model.maxTime:
                t = self.model.maxTime
        elif isinstance(r, int):
            t = np.random.geometric(p=self.model.Lambda[r])
        return t

    def SampleZ(self, r):
        """

        Args:
            r (int|Node): role if int, user if node

        Returns:
            z (int): 1 if successful, 0 if failed

        """
        z = None
        if isinstance(r, Node):
            sum = 0
            for key in r.postIdList.keys():
                post = self.model.postList[r.postIdList[key]]
                sum += len(post.influencedBy)
            p = len(r.postIdList)/sum
            s = np.random.choice(range(2), size=1, p=[1-p, p])
        elif isinstance(r, int):
            if np.random.random_sample(1) > self.model.rho[r]:
                z = 0
            else:
                z = 1
        return z

    def Simulation(self, method):
        """

        Args:
            method (int):

        Returns:
            (int):

        """
        np.random.seed(0)
        S = self.model.S
        for s in range(S):
            self.diffusionSize[s] = 0
            self.diffusionDuration[s] = 0
        activeList = {}
        activeSet = set()
        sourcePostList = {}
        for i in self.model.postList.keys():
            post = self.model.postList[i]
            if post.sourcePost.id == post.sourcePost.sourcePost.id:
                sourcePostList[post.sourceId] = post
        for i in self.model.postList.keys():
            post = self.model.postList[i]
            if post.sourcePost.id != post.id:
                continue
            s = post.sourceId
            postTime = post.postTime
            self.diffusionSize[s] = 1
            self.diffusionDuration[s] = 0
            activeList = {}
            activeSet = set()
            activeList[post.user.id] = 0
            activeSet.add(post.user.id)
            for j in sourcePostList.keys():
                if sourcePostList[s][j].user.id  in activeSet:
                    continue
                activeList[sourcePostList[s][j].post.user.id] = sourcePostList[s][j].postTime - postTime
                activeSet.add(post.user.id)
            for h in activeList.keys():
                user = self.model.nodeList[h]
                currentTime = activeList[h]
                for target in user.inEdgeList:
                    if target.id in activeSet:
                        continue
                    r = 0
                    if method == 0:
                        r = self.SampleRole(user.id)
                    t = 0
                    if method == 0:
                        t = self.SampleT(r)
                    if method == 1:
                        t =self.SampleT(user)
                    if t == self.model.maxTime:
                        continue
                    z = 0
                    if method == 0:
                        z = self.SampleZ(r)
                    if method == 1:
                        z = self.SampleZ(user)
                    if z == 1:
                        activeList[target.id] = currentTime + t
                        activeSet.add(target.id)
                        if currentTime + t > self.diffusionDuration[s]:
                            self.diffusionDuration[s] = currentTime + t
            self.diffusionDuration[s] = len(activeList)
        return 0

    def TrueSize(self, ):
        """

        Returns:
            (int):

        """
        S = self.model.S
        V = self.model.V
        truth_count = [0] * S
        truth = [0] * V
        activeSet = [set()] * S

        for i in self.model.postList.keys():
            post = self.model.postList[i]
            sid = post.sourceId
            if post.user.id in activeSet[sid]:
                continue
            truth_count[sid] += 1
            activeSet[sid].add(post.user.id)
        for s in range(S):
            truth[truth_count[s]] += 1
        sum = truth[100]
        for v in range(99, 0, -1):
            truth[v] += truth[v + 1]
            sum += truth[v]

        with open("size_test_truth.txt", 'w') as fout:
            for v in range(1, 101):
                fout.write("%d %.5f\n" % (v, truth[v]/sum))
            for v in range(V):
                if truth[v] > 0:
                    # print("%d %.5f\n" % (v, truth[v]/sum))
                    pass

        return 0

    def TrueDuration(self, ):
        """

        Returns:
            (int):

        """
        print("Generating true duration!\n")
        S = self.model.S
        trueTime = [0]*S
        timeCount = [0]*self.model.maxTime
        for i in self.model.postList.keys():
            t = self.model.postList[i].postTime - self.model.postList[i].sourcePost.postTime
            sid = self.model.postList[i].sourceId
            if trueTime[sid] < t < self.model.maxTime:
                trueTime[sid] = t
        for s in range(S):
            timeCount[trueTime[s]] += 1
        for t in range(self.model.maxTime-2, -1, -1):
            timeCount[t] += timeCount[t+1]
            sum += timeCount[t]
        with open("duration_truth.txt", 'w') as fout:
            for t in range(self.model.maxTime):
                fout.write("%d %.5f\n" % (t, timeCount[t]/sum))
        return 0

    def SizeAndDuration(self, method):
        """

        Args:
            method (int):

        Returns:
            (int):

        """
        print("Start Simulation!\n")
        sampleTime = 1000
        if method == 1:
            sampleTime = 10
        S = self.model.S
        self.diffusionSize = [0]*S
        self.diffusionDuration = [0]*S
        totalSize = [[]]*sampleTime
        totalDuation = [[]]*sampleTime
        proc = -1
        for t in range(sampleTime):
            if t*100/sampleTime > proc:
                proc = t*100/sampleTime
                print('Simulation Processing %d%%...\n' % proc)
            self.Simulation(method)
            totalSize[t] = [0]*S
            totalDuation[t] = [0]*S
            for s in range(S):
                totalSize[t][s] = self.diffusionSize[s]
                totalDuation[t][s] = self.diffusionDuration[s]
        sizeCount = [0]*self.model.V
        timeCount = [0]*self.model.maxTime
        for s in range(S):
            meanS = 0
            meanD = 0
            for t in range(sampleTime):
                meanS += totalSize[t][s]
                meanD += totalDuation[t][s]
            meanS /= sampleTime
            meanD /= sampleTime
            sizeCount[meanS] += 1
            timeCount[meanS] += 1
        with open("simulation_result.txt", 'w') as fout:
            sum = sizeCount[100]
            for v in range(99, 0, -1):
                sizeCount[v] += sizeCount[v+1]
                sum += sizeCount[v]
            for v in range(1, 101):
                # fout.write("%d %.5f\n" % (v, sizeCount[v]/sum))
                pass
            for v in range(self.model.V):
                # if sizeCount[v] > 0:
                #       fout.write("%d %.5f\n" % (v, sizeCount[v]/S))
                pass
            sum = timeCount[self.model.maxTime - 1]
            for t in range(self.model.maxTime-2, -1, -1):
                timeCount[t] += timeCount[t+1]
                sum += timeCount[t]
            for t in range(self.model.maxTime):
                fout.write("%d %.5lf\n" % (t, timeCount[t]/sum))
        return 0
