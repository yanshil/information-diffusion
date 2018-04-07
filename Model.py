# -*- coding: utf-8 -*-
#Date:2018.4.3
from Data  import NodeAttr, Node, PostAttr, Post, DataLoader
import sys
import math
from string import atof
import numpy
import random

PI=3.141592653
EE=2.718281828459
MAXINT=10000000

def GammaFunction(x):
    res = 0.5 * (math.log(2 * PI) - math.log(x)) + x * (math.log(x + 1 / (12.0 * x - 1.0 / (10 * x))) - 1)
    return res
    #return math.pow(EE, res)

def SecondCmp(self,a,b):
    return self.a.second<self.b.second

class model(object):
    def __init__(self):
        self.V = 0         # number of users
        self.M = 0         # number of posts
        self.S = 0         # number of sourcee posts
        self.roleNum = 0   # number of roles
        self.K = 0         # numebr of features
        self.maxTime = 0   # maximum delay time
        self.tau0 = 0
        self.tau1 = 0
        self.tau2 = 0
        self.tau3 = 0
        self.alpha = 0
        self.beta_0 = 0    # hyper-parameter of Lambda  success
        self.beta_1 = 0
        self.gamma_0 = 0   # hyper-parameter of rho  fail
        self.gamma_1 = 0   # hyper-parameter of rho
        self.rho = None    # 1d pointer. role-active prob (Bionomial)
        self.Lambda = None # 1d pointer. role-delay prob (geometric)
        self.theta = None  # 2d pointer. user-role prob (Multinomial)
        self.mu = None     # 2d pointer.role-feature mean in Gaussian
        self.delta = None  # 2d pointer.role-feature variance in Gaussian
        self.R = None      # 2d pointer.
        self.T = None
        self.Z = None
        self.nur = None    # 2d pointer.
        self.nr = None     # 1d
        self.nu = None     # 1d
        self.nrz  = None   # 2d pointer.
        self.sumz_v = None
        self.sumt_v = None # 2d pointer.
        self.sumt_r = None # 1d
        self.E = None      # 2d pointer.
        self.nz_t = None   # 2d pointer.
        self.sumz_m = None
        self.sumz_s  = None  # 2d pointer.
        self.sum_Lambda = None  #1d
        self.sum_rho = None     # 1d
        self.sum_mu = None      # 2d pointer.
        self.sum_delta = None   # 2d pointer.
        self.nodeList = None    # vector<Node *>
        self.postList = None    # vector<Post *>
        self.userIdMap = {}     # map<int, int>
        self.dataLoader = None  # DataLoader * 

    def  Init(self):
        self.rho = [0.0]*self.roleNum
        self.Lambda = [0.0]* self.roleNum
        self.mu = [[0.0]]* self.roleNum
        self.delta = [[0.0]]* self.roleNum
        self.theta = [[0.0]]* self.V
        self.R = [[0]]* self.M 
        self.T = [[0]]* self.M 
        self.Z = [[0]]* self.M
        self.nur = [[0]]* self.V
        self.nr = [0]* self.roleNum
        self.nu = [0]* self.V
        self.sumz_v = [[0]]* self.S
        self.sumt_v = [[0]]* self.S
        self.E = [[0]]* self.V
        self.nz_t = [[0]]* self.roleNum
        self.nrz = [[0]]* self.roleNum
        self.t_r= [0]* self.roleNum
        self.sumz_m = [[0.0]]* self.roleNum
        self.sumz_s = [[0.0]]* self.roleNum
        self.instanceNum =  self.V * self.K
        self.tau1 =  self.instanceNum
        self.tau2 = ( self.instanceNum + 0.0) / 2.0
        self.tau3 = 0.0
        self.tau0 = 0.0



        for v in range(0,self.V):
            for t in range (0,self.K):
                 self.tau0 +=  self.nodeList[v].featureList[t]
        self.tau0 /= instanceNum

        for v in range(0,self.V):
            for t in range (0,self.K):
                self.tau3 += math.pow(( self.nodeList[v].featureList[t] -  self.tau0), 2)
        self.tau3 /= 2

        for v in range (0,V):
            self.nu.append(0)
            self.theta.append([0.0]*self.roleNum)
            self.nur[v].append([0.0]*self.roleNum)
            self.E[v].append([0]*self.K)
            # for r in range(0,self.roleNum):
            #     self.theta[v][r] = 0.0
            #     self.nur[v][r] = 0

        for r in range(0,self.roleNum):
            self.mu[r].append([0.0]*self.K)
            self.delta[r].append([0.0]*self.K)
            self.nz_t[r].append([0]*self.K)
            self.nrz[r].append([0]*2)
            self.sumz_m[r].append([0.0]*self.K)
            self.sumz_s[r].append([0.0]*self.K)
            self.nrz[r].insert(0,0)
            self.nrz[r].insert(1,0) 
            self.sumt_r[r] = 0
            self.nr[r] = 0.0
            
        for i in range(0,len(self.postList)):
            Node.user = self.postList[i].user
            l = len(user.inEdgeList)
            self.R.append([0]*l)
            self.T.append([0]*l)
            self.Z.append([0]*l)

        for s in range (0,self.S):
            self.sumz_v[s].append([0]*self.V)
            self.sumt_v[s].append([0]*self.V)
            # for v in range(0,V): 
            #     sumz_v[s][v] = 0
            #     sumt_v[s][v] = 0
            
        for i in range(0,len(self.postList)):
     
            Post.post = self.postList[i]
            Node.source = post.user
            u = source.id
            sid = post.sourceId
            tiu = post.postTime
            for j in range(0,len(source.inEdgeList)):
                Node.target = source.inEdgeList[j]
                pid = target.GetPostIdBySource(post.sourcePost.id)
                tiv = MAXINT
                if (pid != -1):
                    tiv = postList[pid].postTime
                if (pid != -1 & tiv < tiu):
                    continue
                v = target.id
               
                y = 1
                if (pid == -1):
                    y = 0
                r = (numpy.random.rand() * self.roleNum)
                if (r == self.roleNum):
                    r -= 1
                t = (numpy.random.rand() * self.maxTime)
                if (t == self.maxTime):
                    t -= 1,
                z = (numpy.random.rand() * 2)
                if (z == 2):
                    z -= 1
                if (y == 1 & self.sumt_v[sid][v] == 0):
                    t = tiv - tiu
                
                if (y == 1 & self.sumz_v[sid][v] == 0):
                    z = 1
                #if (i == 0 & j < 2):
                #   print('%d %d %d %d\n', tiv, tiu, t, r)
                #   update
                
                tv = 0
                if (t + tiu == tiv):
                    tv = 1
                if (t >= self.self.maxTime):
                    t = self.maxTime - 1
                self.R[i][j] = r
                self.T[i][j] = t
                self.Z[i][j] = z
                self.nur[u][r] += 1
                self.nu[u] += 1
                self.nr[r] += 1
                self.nrz[r][z] += 1
                self.sumt_r[r] += t
                self.sumz_v[sid][v] += z
                self.sumt_v[sid][v] += tv
            
        
        for v in range(0,V):
            Node.user = nodeList[v]
            for t in range(0, K):
                x = user.featureList[t]
                r = (numpy.random.rand() * roleNum)
                if (r == roleNum):
                    r -= 1
                self.E[v][t] = r
                self.nur[v][r] += 1
                self.nu[v] += 1
                self.nz_t[r][t] += 1
                self.sumz_m[r][t] += x
            
        
        for r in range(0,self.roleNum):
            for t in range(0,self.K): 
                self.sumz_m[r][t] /= self.nz_t[r][t]
            
        for v in range(0,V):
            for t in range(0,K):
                r = self.E[v][t]
                x = self.nodeList[v].featureList[t]
                self.sumz_s[r][t] += math.pow((x - self.sumz_m[r][t]), 2)
            
        
        for r in range (0,roleNum):
            for t in range(0,K):
                self.sumz_s[r][t] /= self.nz_t[r][t]

    def  SampleRTZ(self,u,v,y,tiu,tiv,sumtv,sumzv):
        RAlpha = self.roleNum * self.alpha
        p = [0.0]*2 * self.roleNum * self.maxTime

        for r in range(0,self.roleNum):
            term1 = (self.nur[u][r] + self.alpha + 0.0) / (self.nu[u] + RAlpha) #theta
            for t in range(0,self.maxTime):
                prod = 1.0
                for tt in range(0,t):
                    prod *= self.sumt_r[r] - self.nr[r] + self.beta_1 + tt
                
                term2 = (self.nr[r] + self.beta_0) * prod
                prod = 1.0
                for tt in range(0,t+1): 
                    prod *= (self.beta_0 + self.sumt_r[r] + self.beta_1 + tt)
                
                term2 /= prod
                #float term2 = Lambda[r] * math.pow((1 - Lambda[r]), t)
                for z in range(0,2):
                    term3 = self.nrz[r][z]
                    if (z == 0):
                        term3 += self.gamma_0
                    else:
                        term3 += self.gamma_1
                    term3 /= (self.nr[r] + self.gamma_0 + self.gamma_1)
                    term4 = 1.0
                    if (y == 0 & z == 1):
                        term4 = 0.0
                    if (y == 1 & sumzv == 0 & z == 0):
                        term4 = 0.0
                    tv = 0
                    if (t + tiu == tiv):
                        tv = 1
                    if (y == 1 & sumtv == 0):
                        if (tv == 0 & (tiv - tiu < self.maxTime |t != self.maxTime - 1)):
                            term4 = 0.0
                        else:
                            term4 = 1.0
                    
                    idx = r * self.maxTime * 2 + t * 2 + z
                    #print('%d %d %d : %d'%(r, t, z, idx))
                    p[idx] = term1 * term2 * term3 * term4
                    
                    #if (u == 6 & v == 5 & p[idx] > 0):
                    
                    #    print('%d %d %d %d %d: %.5f %.5f %.5f %.5f %.5f'%(r, t, z, idx, sumzv, term1, term2, term3, term4, p[idx]))
                    
                    
                
            
        
        # cumulate multinomial parameters
        for  k  in range(1,2 * self.roleNum * self.maxTime): 
            p[k] += p[k - 1]

        # scaled sample because of unnormalized p[]
        s = (random.random()) * p[2 * roleNum * maxTime - 1]

        sample = 2 * self.roleNum * self.maxTime - 1
        for sample in range(0,2 * self.roleNum * self.maxTime - 1):
            if (p[sample] > s):
                break
        #print('%.3lf %.3lf %d' %(p[K - 1] ,u, topic)
        del p
        return sample

    def  SampleDiffusion(self):     	    
        for i in range(0,len(self.postList)):
        
            Post.post = self.postList[i]
            Node.source = post.user
            u = source.id
            sid = post.sourceId
            tiu = post.postTime
            for j in range(0,len(source.inEdgeList)):
                #print('%d ', j)
                Node.target = source.inEdgeList[j]
                #print('%d', target.id)
                pid = target.GetPostIdBySource(post.sourcePost.id)
                tiv = MAXINT
                if (pid != -1):
                    tiv = postList[pid].postTime
                if (pid != -1 & tiv < tiu):
                    continue
                #if (pid != -1 & tiv - tiu - 1 >= maxTime)
                #    print('Time Exceeds!\n')
                v = target.id
                old_r = self.R[i][j]
                old_t = self.T[i][j]
                old_z = self.Z[i][j]
                old_tv = 0
                #print('old sample: %d %d %d', old_r, old_t, old_z)
                if (old_t + tiu == tiv | (tiv - tiu >= self.maxTime & old_t ==self. maxTime - 1)):
                    old_tv = 1
                self.nur[ u ][ old_r ] -=1
                self.nr[ old_r ] -= 1
                self.nu[ u ]  -=1
                self.sumz_v[sid][v] -= old_z
                self.sumt_v[sid][v] -= old_tv
                self.sumt_r[old_r] -= old_t - 1
                self.nrz[old_r][old_z] -=1
                #if (sumt_v[sid][v] < 0 & u == 6 & v == 162)
                #    print('%d %d', old_tv)
                # sampling
                y = 1
                if (pid == -1):
                    y = 0
                sample = SampleRTZ(u, v, y, tiu, tiv, self.sumt_v[sid][v], self.sumz_v[sid][v])
                r = sample / (self.maxTime * 2)
                t = (sample % (self.maxTime * 2)) / 2
                z = sample % 2
                #print('%d %d %d', r, t, z)
                # update
                tv = 0
                if (t + tiu == tiv | (tiv - tiu >= self.maxTime & t == self.maxTime - 1)):
                    tv = 1
                self.R[i][j] = r
                self.T[i][j] = t
                self.Z[i][j] = z
                self.nur[u][r] +=1
                self.nu[u] +=1
                self.nr[r] +=1
                self.nrz[r][z] += 1
                self.sumt_r[r] += t + 1
                self.sumz_v[sid][v] += z
                self.sumt_v[sid][v] += tv
            
    def  SampleFeature(self):
 	    
        for i in roleNum(0,len(self.nodeList)):
            Node.user = self.nodeList[i]
            u = user.id
            for t in range(0,self.K):
            
                x = user.featureList[t]
                old_e = self.E[u][t]
                self.nur[u][old_e]-=1
                self.nu[u] -= 1
                self.sumz_s[old_e][t] = self.sumz_s[old_e][t] * self.nz_t[old_e][t] - x * x + self.nz_t[old_e][t] * self.sumz_m[old_e][t] * self.sumz_m[old_e][t]
                self.sumz_m[old_e][t] = (self.sumz_m[old_e][t] * self.nz_t[old_e][t] - x + 0.0) / (self.nz_t[old_e][t] - 1)
                self.nz_t[old_e][t] -=self.nz_t[old_e][t]
                self.sumz_s[old_e][t] = (self.sumz_s[old_e][t] - self.nz_t[old_e][t] * self.sumz_m[old_e][t] * self.sumz_m[old_e][t]) / (self.nz_t[old_e][t])
                e = SampleRole(u, x, t)

                #print('%d %d %d', i, t, e)
                self.E[u][t] = e
                self.nur[u][e] +=1
                self.nu[u] +=1
                self.sumz_s[e][t] = self.nz_t[e][t] * self.sumz_s[e][t] + x * x + self.nz_t[e][t] * self.sumz_m[e][t] * self.sumz_m[e][t]
                self.sumz_m[e][t] = (self.sumz_m[e][t] * self.nz_t[e][t] + x) / (self.nz_t[e][t] + 1)
                self.nz_t[e][t] +=1
                self.sumz_s[e][t] = (self.sumz_s[e][t] - self.nz_t[e][t] * self.sumz_m[e][t] * self.sumz_m[e][t]) / self.nz_t[e][t]
            
    def  SampleRole(self,u,x,t):
        
        RAlpha =self.roleNum * self.alpha
        p = [0.0]*self.roleNum
        for r in range(0,self.roleNum):
            tmp_var = self.nz_t[r][t] * self.sumz_s[r][t] + x * x + self.nz_t[r][t] * self.sumz_m[r][t] * self.sumz_m[r][t]
            tmp_mean = (self.sumz_m[r][t] * self.nz_t[r][t] + x) / (self.nz_t[r][t] + 1)
            tmp_nzt = self.nz_t[r][t] + 1
            tmp_var = (tmp_var - tmp_nzt * tmp_mean * tmp_mean) / (tmp_nzt + 0.0)

            term1 = (self.nur[u][r] + self.alpha) / (self.nu[u] + RAlpha)
            term2 = GammaFunction(self.alpha + (tmp_nzt + 0.0) / 2.0) - GammaFunction(self.alpha + (self.nz_t[r][t] + 0.0) / 2)
            term2 = math.pow(EE, term2)
            tmp_term3 = self.tau3 + 0.5 * (self.nz_t[r][t] * self.sumz_s[r][t] + (self.tau1 * self.nz_t[r][t] * math.pow((self.sumz_m[r][t] - self.tau0), 2)) / (self.tau1 + self.nz_t[r][t]))
            tmp_term3 = math.log(tmp_term3) * (self.tau2 + 0.5 * self.nz_t[r][t])
            term3 = self.tau3 + 0.5 * (tmp_nzt * tmp_var + (self.tau1 * tmp_nzt * math.pow(tmp_mean - self.tau0, 2)) / (self.tau1 + tmp_nzt))
            term3 = math.log(term3) * (self.tau2 + 0.5 * tmp_nzt)
            term3 = tmp_term3 - term3
            term3 = math.pow(EE, term3)
            term3 *= math.sqrt(self.tau1 + self.nz_t[r][t]) / math.sqrt(self.tau1 + tmp_nzt)
            #print('%.3lf %.3lf %.10lf'%(term1, term2, term3))
            p[r] = term1 * term2 * term3
    
        #cumulate multinomial parameters
        for k in range(1,self.roleNum):
            p[k] += p[k - 1]
        #scaled sample because of unnormalized p[]
        s = (random.random()) * p[self.roleNum - 1]

        role = self.roleNum - 1
        for role in range(0,self.roleNum - 1):
            if (p[role] > s):
                break
        #print('%.3lf %.3lf %d'%(p[K - 1], u, topic))
        del p
        return role
  
    # def  GetOrInsertUserId( key):
 	  #   pass
    # def  GetUserId(  key):
 	  #   pass

    def  LoadData(self,dataLoader):
        self.postList = dataLoader.postList
        self.nodeList = dataLoader.nodeList
        self.V = len(nodeList)  #the number of users
        self.M = len(postList) #the number of post
        self.S = len(dataLoader.sourceIdMap) #the number of source post
        self.K = len(Node(dataLoader.nodeList[0]).featureList) #pagerank & network constraint
        print('#source posts: %d, #users: %d, #posts: %d\n', S, V, M)   

    def  GibbsSampling( self,maxIter,   BURN_IN,   SAMPLE_LAG):
     	    
        print('####################')
        print('Start Learning!')
        srand(745623)
        Init()
        sample_cnt = 0
        self.sum_Lambda = []
        self.sum_rho = []
        self.sum_mu = [[0.0]]*self.roleNum
        self.sum_delta = [[0.0]]*self.roleNum
        for r in range(0,self.roleNum):         
            self.sum_Lambda.append(0.0)
            self.sum_rho.append(0.0)
        
        self.sum_mu=[([0] * self.K) for p in range(self.roleNum)] 
        self.sum_delta= [([0] * self.K) for p in range(self.roleNum)] 
        for r in range(0,self.roleNum):     
            for t in range(0,self.K):
                self.sum_mu[r][t]=0.0
                self.sum_delta[r][t]=0.0
        
        for iter in range(1,maxIter+1):
            print('[Iteration %d]...'%iter)
            s1 = SampleDiffusion()
            if (s1 == -1):
                print('Error when sampling diffusion process!')
                return -1
            
            SampleFeature()
            if (iter < BURN_IN):
                continue
            if ((iter - BURN_IN) % SAMPLE_LAG != 0):
                continue
            sample_cnt += 1
            # update parameters
            for u in range(0,len(self.nodeList)):
                sum = 0.0
                for r in range(0,self.roleNum):
                    self.theta[u][r] += (self.nur[u][r] +self.alpha + 0.0) / (self.nu[u] + self.roleNum * self.alpha)  #algorithm 1
                    sum += self.theta[u][r]
                
                
               # if (sum != sample_cnt):
                
               #     for r in range(0,roleNum):
               #          print('%d %d %.5lf'%(nur[u][r], nu[u], theta[u][r]))
                    
               #      return -1
                
            
            
            for r in range(0,self.roleNum):
            
                self.Lambda[r] = (self.nr[r] + self.beta_0) / (self.sumt_r[r] + self.beta_0 + self.beta_1)  #algorithm 2
                self.rho[r] = (self.nrz[r][1] + self.gamma_1) / (self.nr[r] + self.gamma_0 + self.gamma_1)  #algorithm 3
                for t in range(0,self.K):
                
                    self.mu[r][t] = (self.tau0 * self.tau1 +self. nz_t[r][t] * self.sumz_m[r][t]) / (self.tau1 + self.nz_t[r][t])  #algorithm 4
                    self.delta[r][t] = (2 * self.tau2 + self.nz_t[r][t]) / (2 * self.tau3 + self.nz_t[r][t] * self.sumz_s[r][t] + (self.tau1 * self.nz_t[r][t] * math.pow(self.sumz_m[r][t] - self.tau0, 2)) / (self.tau1 +self.nz_t[r][t]))  #algorithm 5
                
            
            PrintRho()
            PrintNr()
            PrintMu()
            for r in range(0, self.roleNum):
                self.sum_Lambda[r] += 1
                self.sum_rho[r] += 1

                for t in range(0, self.K):        
                    self.sum_mu[r][t] += 1
                    self.sum_delta[r][t] += 1
                
            
        

        for u in range(0, len(self.nodeList)): 
            for r in range(0, self.roleNum):
                self.theta[u][r] /= (sample_cnt + 0.0)
        for r in range(0, self.roleNum):
            self.Lambda[r] = self.sum_Lambda[r] / sample_cnt
            self.rho[r] = self.sum_rho[r] / sample_cnt
            for t in range(0,self.K): 
                self.mu[r][t] = self.sum_mu[r][t] / sample_cnt
                self.delta[r][t] = self.sum_delta[r][t] / sample_cnt
                self.delta[r][t] = math.sqrt(1.0 / self.delta[r][t])
        
        print('########## Final Parameters ##########')
        PrintRho()
        PrintMu()
        
    def  PrintMu(self):
 	    
        print('Mu:')
        for r in range(0, self.roleNum):
            for k in range(0,self.K):       
                print('%.8lf '%self.mu[r][k])
     
        print('Delta: ')
        for r in range(0, self.roleNum):  
            for k in range(0,self.K):
                print('%.8lf '%self.delta[r][k])
           
    def  PrintRho(self):
        print('Rho: ')
        for r in range(0, self.roleNum):
            print('%.8lf '%self.rho[r])
        print('Lambda: ')
        for r in range(0, self.roleNum):
            print('%.8lf '%self.Lambda[r])  

    def  PrintNr(self):
        
        print('#sampled roles:')
        for r in range(0, self.roleNum):
            print('%d '%self.nr[r])

    def  PrintTheta(self):
     	   
        fout = open('model_theta.txt', 'w')
        for v in range(0,self.V):
        
            print(fout+'%s'%str(self.nodeList[v].name))
            for r in range(0, self.roleNum):
                print(fout, '%.5lf '%self.theta[v][r])
            print(fout)
        
        fout.close()

    def  Save(self,fileDir):
 	    
        SaveTheta()
        SaveRho()
        SaveGaussian()
        fout = open(fileDir, 'w')
        for r in range(0, self.roleNum):
            print(fout, '%.10lf '%self.rho[r])
        print(fout)
        for r in range(0, self.roleNum):
            print(fout, '%.10lf '%self.Lambda[r])
        print(fout)
        for r in range(0, self.roleNum):
            for t in range(0,self.K):
                print(fout, '%.10lf '%self.mu[r][t])
            
            print(fout)
        
        for r in range(0, self.roleNum):
        
            for t in range(0,self.K):
                print(fout, '%.10lf '%self.delta[r][t])
            print(fout)
        
        for v in range(0,self.V):
        
            for r in range(0, roleNum):
                print(fout, '%.10lf '%self.theta[v][r])
            print(fout)
        
        fout.close()
  
    def  SaveGaussian(self):
 	  
        fout = open('model_gaussian.txt', 'w')
        fout.write('Mean:')
        for r in range(0,self.roleNum):
            for t in range(0,self.K):
                fout.write('%.5lf '%self.mu[r][t])
            #fout.write('\n')

        fout.write('Deviation:')
        for r in range(0,self.roleNum):
            for t in range(0,self.K): 
                print(fout, '%.5lself.f '%self.delta[r][t])
            print(fout, '\n')
        fout.close()

    def  SaveRho(self):
     	    
        fout = open('model_rho.txt', 'w')
        print(fout, 'Rho:')
        for r in range(0, self.roleNum):
            print(fout, '%.10lf '%self.rho[r])
        print(fout, '\nLambda:\n')
        for r in range(0, self.roleNum):
            print(fout, '%.10lf '%self.Lambda[r])
        print(fout, '\n')
        fout.close()
        
    def  SaveTheta(self):
     	    
        fout = open('model_theta.txt', 'w')
        for v in range(0,self.V):
        
            print(fout, '%s'%str(self.nodeList[v].name))
            for r in range(0, self.roleNum):
                print(fout, '%.5lf '%self.theta[v][r])
            
        
        fout.close()
        

    def  Test(self):   
        print('Post-level test!\n')
        truth =set()
        pair={}
        #vector<pair<int, float> >* res = new vector<pair<int, float> >[S]
        res=[]
        for s in range(0,self.S):
            truth.clear()
            for v in range(0, self.V):
                res.append(pair={"first":"v","second":1.0})

        for i in range(0,len(self.postList)):
            Post.post = self.postList[i]
            sid = post.sourceId
            u = post.user.id
            Node.user = post.user
            if (post.sourcePost.id != post.id):
                truth[sid].append(user.id)

            for j in range(0,len(user.inEdgeList)): 
                Node.target = user.inEdgeList[j]
                v = user.inEdgeList[j].id
                pid = target.GetPostIdBySource(post.sourcePost.id)
                tiv = MAXINT
                if (pid != -1):
                    tiv = postList[pid].postTime
                if (pid != -1 & tiv < post.postTime):
                    continue
                prob = 0.0
                maxProb = 0.0
                maxR=0
                for r in range(0, self.roleNum):
                    prob += (self.rho[r] * math.pow(1 - self.Lambda[r], self.maxTime - 1) + (1 - self.rho[r])) * self.theta[u][r]
                    if (self.theta[u][r] > maxProb):
                        maxProb = theta[u][r]
                        maxR = r
                #unactive users
                prob = self.rho[maxR] * math.pow(1 - self.Lambda[maxR], self.maxTime - 1) + (1 + self.rho[maxR])
                res[sid][v].second *= prob
            
        
        posCnt = 0
        allCnt = 0
        for s in range(0,self.S):
            posCnt += len(truth)
            allCnt += len(res)
        print('Average Postive Instance: %.5lf\n', (posCnt + 0.0) / (S + 0.0))
        print('Postive : Negative Instance: %.5lf\n', (posCnt + 0.0) / (allCnt - posCnt))
        Map = 0.0
        mrr = 0.0
        estCnt = 0
        P = []
        for  i in range(0,100):
            P[i] = 0.0
        print('#query : %d\n', S)
        
        res.sort(SecondCmp)
            # sort(res[s].begin(), res[s].end(), SecondCmp)
            #if (s == 0)
            #    print('%.10lf %.10lf\n', res[s][0].second, res[s][1].second)
        for s in range(0,S):  
            ap = 0.0
            ar = 0.0
            hitCnt = 0
            for  i in range (0,len(res[s])):
                v = res[s][i].first
                hit = 0
                if (truth[s].count(v) > 0):
                    hit +=1
                hitCnt += hit
                if (hit > 0):
                
                    #if (s == 0)
                    #    print('%d ', i)
                    ap += (hitCnt + 0.0) / (i + 1.0)
                    ar += 1.0 / (i + 1.0)
                
                #ap += (hitCnt + 0.0) / (i + 1.0)
                if (i < 100):
                    P[i] += hit
                #ap += (hit + 0.0) / (i + 1.0)
                #mrr += (hitCnt + 0.0) / (i + 1.0)
            
            Map += ap / len(truth)
            mrr += ar / len(truth)
            #if (s == 0)
            #    print('\nMAP: %.5lf\n', ap / truth[s].size())
            testCnt += len(truth)
        
        for i in range(0,100):
            P[i] += P[i - 1]
        for i in range(0,100):
            P[i] /= ((i + 1.0) * S)
        Map /= S
        mrr /= S
        print('#Test cases: %d\n', testCnt)
        print('P@1: %.5lf\n', P[0])
        print('P@3: %.5lf\n', P[2])
        print('P@5: %.5lf\n', P[4])
        print('P@10: %.5lf\n', P[9])
        print('P@20: %.5lf\n', P[19])
        print('P@50: %.5lf\n', P[49])
        print('P@100: %.5lf\n', P[99])
        print('MAP: %.5lf\n', Map)
        print('MRR: %.5lf\n', mrr)
        
    def  RoleLevelTest(self):
    
        print('Role-level test!\n')
        truth =set()
        pair={}
        res=[]
        for r in range(0,roleNum):
            truth.clear()
            for v in range(0, V):
                for s in range(0,S):
                    res[r].insert(s+1,pair={"first":"v","second":1.0})
                    #res[r][s].push_back(make_pair(v, 1.0))
        
        for i in range(0,len(postList)):
        
            Post.post = self.postList[i]
            sid = post.sourceId
            u = post.user.id
            Node.user = post.user
            if (post.sourcePost.id != post.id):
                truth[sid].append(user.id)
            for j in range(0,len(user.inEdgeList)):
                Node.target = user.inEdgeList[j]
                v = user.inEdgeList[j].id
                pid = target.GetPostIdBySource(post.sourcePost.id)
                tiv = MAXINT
                if (pid != -1):
                    tiv = postList[pid].postTime
                if (pid != -1 & tiv < post.postTime):
                    continue
                prob = 0.0
                role = 0
                for r in range(0,self.roleNum):
                    prob += (rho[r] * math.pow(1 - Lambda[r], maxTime - 1) + (1 - rho[r])) * theta[u][r]#inactive user
                    if (self.theta[v][r] > self.theta[v][role]):
                        role = r
                res[role][sid][v].second *= prob    
        posCnt = 0
        allCnt = 0
        for s in range(0,S):
        
            posCnt += truth[s].size()
            allCnt += res[0][s].size()
        
        print('Average Postive Instance:'+'%.5f'%(posCnt + 0.0) / (S + 0.0))
        print('Postive : Negative Instance:'+'%.5f'%(posCnt + 0.0) / (allCnt - posCnt))
       
        C = []
        testCase = 0
        for r in range(0,self.roleNum):
            print('Role: %d', r)
            C.append(0)
            Map = 0.0
            mrr = 0.0
            P = []
            for i in range(0,100):
                P.append(0.0)
            for s in range(0,S):
                truth.clear()
            for i in range(0,len(self.postList)):
                Post.post= list()
                sid = post.sourceId
                u = post.user.id
                Node.user = post.user
                role = 0
                for rr in range(0,self.roleNum):
                    if (self.theta[u][rr] > self.theta[u][role]):
                        role = rr
                if (post.sourcePost.id != post.id & role == r):
                    truth[sid].append(u)
            
            for s in range(0,S): 
            
                C[r] += len(self.res[r][s])
                res.sort(SecondCmp)
                ap = 0.0
                ar = 0.0
                hitCnt = 0
                for  i in range(0,len(res[r][s])):
                    v = res[r][s][i].first
                    hit = 0
                    if (truth[s].count(v) > 0):
                        hit +=1
                        hitCnt += hit
                    if (hit > 0):
                        ap += (hitCnt + 0.0) / (i + 1.0)
                        ar += 1.0 / (i + 1.0)
                    
                    #ap += (hitCnt + 0.0) / (i + 1.0)
                    if (i < 100):
                        P[i] += hit
                    #ap += (hit + 0.0) / (i + 1.0)
                    #mrr += (hitCnt + 0.0) / (i + 1.0)
                
                if (len(truth[s]) > 0):
                    Map += ap / len(truth[s])
                    mrr += ar / len(truth[s]) 
                
                testCase += len(truth[s])
            
            for i in range(0,100):
                P[i] += P[i - 1]
            for i in range(0,100):
                P[i] /= ((i + 1.0) * S)
            Map /= S
            mrr /= S
            print('P@1:'+'%.5lf'%P[0])
            print('P@3:'+'%.5lf'%P[2])
            print('P@5:'+'%.5lf'%P[4])
            print('P@10:'+'%.5lf'%P[9])
            print('P@20:'+'%.5lf'%P[19])
            print('P@50:'+'%.5lf'%P[49])
            print('P@100:'+'%.5lf'%P[99])
            print('MAP:'+'%.5lf'%Map)
            print('MRR:'+'%.5lf'%mrr)
    
        allC = 0
        for r in range(0,self.roleNum):
            allC += C[r]
        for r in range(0,self.roleNum):
            print('%.5lf'%((C[0] + 0.0) / allC))
      