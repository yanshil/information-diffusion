import sys
import math
import datetime

class NodeAttr(object):
    def __init__(self):
        '''
        id, name
        inEdgeIdList : a integer list indicating followers
        outEdgeIdList : ... followees
        inEdgeList : pointer list indicating the followers
        outEdgeList : ... followees
        feature: a double list indicating features
        postIdList : KVP <pair<int, int>> , source id and post id pair(by this user)
        '''
        self.id = -1
        self.name = None
        self.inEdgeIdList = []
        self.outEdgeIdList = []
        self.inEdgeList = None
        self.outEdgeList = None
        self.featureList = None
        self.postIdList = {}


# DataLoader里面存储的是这个链表
class Node(object):
    '''
        the chain table only need one function : append
    '''
    def __init__(self,id = None, name = None):
        self.id = id  
        self.name = name
        self.inEdgeIdList = []
        self.outEdgeIdList = []
        self.inEdgeList = []
        self.outEdgeList = []
        self.featureList = []
        self.postIdList = []
        self.head = None
        self.length = 0
        self.next = None

    def Append(self, thisNode):
        item = thisNode
        if isinstance(thisNode, Node):
            item = thisNode
        else:
            print("error loading data in Node")

        if not self.head:
            self.head = item
            self.length += 1
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = item
            self.length += 1
    
    def GetPostPosBySource(self,sourcePostId):
        l = 0
        r = len(self.postIdList) - 1
        pos = -1
        # quick sort
        while l <= r:
            mid = math.floor((l + r) / 2)
            if self.postIdList[mid][0] == sourcePostId:
                pos = mid
                break;
            if self.postIdList[mid][0] < sourcePostId:
                l = mid + 1
            else:
                r = mid - 1
        
        while len(self.postIdList) > 0 & pos > 0  == sourcePostId:
            if self.postIdList[pos - 1][0] == sourcePostId :
                pos = pos - 1
            else:
                break
        return pos


    def GetPostIdBySource(self, sourcePostId):
        res = self.GetPostPosBySource(sourcePostId)
        if res == -1 :
            return -1
        return self.postIdList[res][1]



class PostAttr(object):
    def __init__(self):
        '''
            int     |        id; |
            Node*    |       user;
            int       |      postTime;
            int        |     inactiveNeighbors; | number of user's follower that havent repost
            int         |    sourceId;
            string       |   name;
            Post*         |  sourcePost;
            vector<Post*>  | influencedBy; | travers use's followee
        '''
        self.id = -1
        self.user = None  # 注意这里的指针
        self.postTime = -1
        self.inactiveNeighbors = -1
        self.sourceId = -1
        self.name = None
        self.sourcePost = None
        self.influencedBy = None  # 注意这个是干嘛的


class Post(object):
    '''
        the chain table only need one function : append
    '''

    def __init__(self, pHead=None, pNext=None):
        self.head = pHead
        self.length = 0
        self.next = pNext

    def Append(self, thisPost):
        item = thisPost
        if isinstance(thisPost, PostAttr):
            item = thisPost
        else:
            print("error loading data in Node")

        if not self.head:
            self.head = item
            self.length += 1
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = item
            self.length += 1


class DataLoader(object):
    def __init__(self, NETWORK_FILE_DIR=None, DIFFUSION_FILE_DIR=None, NETWORK_CONSTRAINT_FILE_DIR=None,
                 PAGE_RANK_FILE_DIR=None):
        self.TIME_STEP = -1
        self.NETWORK_FILE_DIR = NETWORK_FILE_DIR   # network file
        self.DIFFUSION_FILE_DIR = DIFFUSION_FILE_DIR # diffusion file dir
        self.NETWORK_CONSTRAINT_FILE_DIR = NETWORK_CONSTRAINT_FILE_DIR # network constraint file
        self.PAGE_RANK_FILE_DIR = None # PR
        self.nodeList = []    # Node pointer vector. loaded from network.txt
        self.postList = []    # Post pointer vector. loaded from posts.txt
        self.userIdMap = {}     # KVP of user string and user id(1, 2, 3...)
        self.postIdMap = {}     # KVP of post string(1st attr) and post id(1, 2, 3...)
        self.sourceIdMap = {};  # KVP of source id(second attr in postList) and (1, 2, 3...)
                                     # what is a source id?
    
    def LoadData(self):
        print("######## Start loading data ########");
        self.userIdMap = {}
        self.postIdMap = {}
        self.sourceIdMap = {}
        self.LoadNetwork(self.NETWORK_FILE_DIR)
        self.LoadDiffusion(self.DIFFUSION_FILE_DIR)
        self.LoadFeature(self.NETWORK_CONSTRAINT_FILE_DIR)

        a = 0
        b = 0

        for i in range(len(self.nodeList)):
            if len(self.nodeList[i].featureList) == 0 :
                self.nodeList[i].featureList.append(1.0)
                a = a + 1 
        
        self.LoadFeature(self.PAGE_RANK_FILE_DIR)
        for i in range(len(self.nodeList)):
            if len(self.nodeList[i].featureList) < 2 :
                self.nodeList[i].featureList.append(0)
                b = b + 1 
        
        # printf("Missing %.5lf%% (%d / %d) PageRank.\n", (b + 0.0) * 100 / nodeList.size(), b, (int) nodeList.size());
        # printf("Missing %.5lf%% (%d / %d) NetworkConstraint.\n", (a + 0.0) * 100 / nodeList.size(), a, (int) nodeList.size());
        print("Dataset is ready!")

        


    def LoadNetwork(self, filedir):
        print("########Loading Network Data########")
        file = open(filedir)
        line = file.readline()
        count = 0
        '''
        while line:
            count = count + 1
            if count % 100 == 0:
                print(count)
            line = file.readline()
        '''

        while line:
            tokens = line.strip().split(" ")
            # print(line)
            if len(tokens) < 1:
                continue
            count = count + 1
            if count % 100000 == 0:
                break
                print("Loading", count, "th line")
            starttime = datetime.datetime.now()
            source = self.GetOrInsertUserId(tokens[0])
            if source == 1 :
                a = 1
                b = 1

            '''
                # usw map in STL to find whether the use has been processed
                # if does, return its ID. if not, make a KVP and return a new id,
                # and push a new Node in nodeList
            '''
            self.nodeList[source].name = tokens[0]

            for j in range(len(tokens)): # 1, 2, 3, .. n-1
                if j == 0:
                    continue
                target = self.GetOrInsertUserId(tokens[j])
                self.nodeList[target].name = tokens[j]
                # 其实name是什么完全不重要了， 咦，好像name已经被输进去了
                self.nodeList[source].outEdgeList.append(self.nodeList[target])
                self.nodeList[target].inEdgeList.append(self.nodeList[source])
                # print(self.nodeList[source].name, " ", self.nodeList[source].outEdgeList[len(self.nodeList[source].outEdgeList) - 1].name)
            # 这里得到的是所有入/出关系
            line = file.readline()


        # print(self.userIdMap)
        # print(len(self.userIdMap))
        # 这里显然可以改进！！！！！！！！！！！！！！！！
        temp = len(self.nodeList)
        for j in range(temp):
            thisNode = self.nodeList[j]
            self.nodeList[j].outEdgeIdList = []
            for k in range(len(thisNode.outEdgeList)):
                self.nodeList[j].outEdgeIdList.append(thisNode.outEdgeList[k].id)
            self.nodeList[j].outEdgeIdList.sort()
            # print(j, " ", self.nodeList[j].outEdgeIdList)
        print("Load", count, "users in total")
        return 0



    def LoadDiffusion(self, filedir):
        print("########Loading Diffusion Data########")
        file = open(filedir)
        line = file.readline()
        count = 0
        notfound = 0
        # while line:
        #     line = file.readline()
        #     count = count + 1
        #     if count % 100000 == 0:
        #         print (count)
        while line:
            tokens = line.strip().split("\t")
            # print(line)
            if len(tokens) < 1:
                continue
            count = count + 1
            if count % 100000 == 0:
                break
                print("Loading", count, "th line in Diffusion")

            pid = len(self.postList)    # postList is a list containing posts
            t = eval(tokens[1])         # first attribute in a line
            uid = self.GetUserId(tokens[2])#-----------------这句话OK了么？
            if uid == -1:
                notfound = notfound + 1
                line = file.readline()
                continue
            
            post = Post()       # create a new Post()
            post.id = pid
            post.name = tokens[0]
            post.user = self.nodeList[uid]
            post.postTime = t / self.TIME_STEP

            sid = post.id

            if len(tokens[3]) > 1 :
                sid = self.GetPostId(tokens[3])
            
            if len(tokens[5]) > 1 & self.GetPostId(tokens[5]) == -1 :
                line = file.readline()
                continue
            
            if sid == -1:
                line = file.readline()
                continue
            
            post.sourceId = self.GetOrInsertSourceId(sid) # ----------
            # make pair in sourceIdMap

            # postIdMap is a dictionary, key is tokens[0], value is pid
            # tokens[0] is the name of the post, pid is a 1 2 3.. n number of this post
            self.postIdMap[tokens[0]] = pid 

            self.postList.append(post)

            post.sourcePost = self.postList[sid]
            # 上面这句话没用？

            # 放入user id 的postIdList里面
            self.nodeList[uid].postIdList.append([sid, post.id])
            # 第一个是tokens[3]的， 第二个是123456的
            line = file.readline()
        
        # finish reading all the posts
        for i in range(len(self.nodeList)):
            self.nodeList[i].postIdList.sort() # sort  by sid

        # traverse all the posts, determine "influencedBy" and "neighbors"
        for i in range(len(self.postList)):
            post = self.postList[i]
            post.influencedBy = []
            user = post.user
            #if i % 100 == 0:
                 #print(i, 'influence', len(user.outEdgeList) )
            if self.postList[i].sourcePost.id != self.postList[i].id:
                # if this post is not original
                # search user's followees, get where this post is from
                for j in range( len(user.outEdgeList) ):
                    source = user.outEdgeList[j]
                    pid = source.GetPostIdBySource(post.sourcePost.id) # !!!!!!!!!!!!!!!!!!!
                    sourcePostTime = -1
                    if pid != -1:
                        sourcePostTime = self.postList[pid].postTime
                    if pid == -1:
                        continue
                    if sourcePostTime <= post.postTime:
                        post.influencedBy.append(self.postList[pid])
            self.postList[i].inactiveNeighbors = 0
            # search followers
            for j in range(len(user.inEdgeList)):
                target = user.inEdgeList[j]
                # print(post.sourcePost.id)
                p = target.GetPostIdBySource(post.sourcePost.id)
                if p == -1:
                    self.postList[i].inactiveNeighbors += 1

        print("Load", count, "posts in total")
                
    
    
    def LoadFeature(self, filedir): 
        file = open(filedir)
        line = file.readline()
        count = 0
        print('#########loading feature##########')
        while line :
            count = count + 1
            if count % 100000 == 0:
                print('loading', count, 'feature')
            tokens = line.strip().split(" ")

            uid = tokens[0]
            uid = self.GetUserId(uid)
            if uid == -1:
                line = file.readline()
                continue
            
            val = eval(tokens[1])
            # print(uid)
            # print(len(self.nodeList))
            self.nodeList[uid - 1].featureList.append(val + 1e-10)
            line = file.readline()
        print('End of loading feature')
        return 0

    def GetUserId(self, key):
        if key in self.userIdMap:
            return self.userIdMap[key]
        else:
            return -1

    def GetPostId(self, key):
        if key in self.postIdMap:
            return self.postIdMap[key]
        else:
            return -1

    def GetOrInsertUserId(self, key):
        if len(self.userIdMap) > 0 :
            if  self.userIdMap.__contains__(key):
                return self.userIdMap[key]
        thisNode = Node(len(self.userIdMap), key)
        self.nodeList.append(thisNode)
        self.userIdMap[key] = len(self.userIdMap) # 从0开始
        return thisNode.id
    


    def GetOrInsertPostId(self, key):
        pass

    def GetOrInsertSourceId(self, key):
        if key in self.sourceIdMap:
            return self.sourceIdMap[key]
        thisId = len(self.sourceIdMap)
        self.sourceIdMap[key] = thisId
        return thisId
