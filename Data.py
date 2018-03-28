import sys

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
    def __init__(self,id = None, name = None, inEdgeIdList = None, 
        outEdgeIdList = None, inEdgeList = [], outEdgeList = [], 
        featureList = None, postIdList = None,  pHead = None, pNext = None):
        self.id = id  
        self.name = name
        self.inEdgeIdList = inEdgeIdList
        self.outEdgeIdList = outEdgeIdList
        self.inEdgeList = inEdgeList
        self.outEdgeList = outEdgeList
        self.featureList = featureList
        self.postIdList = postIdList
        self.head = pHead
        self.length = 0
        self.next = pNext

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
        self.influencedBy = None # 注意这个是干嘛的


class Post(object):
    '''
        the chain table only need one function : append
    '''
    def __init__(self, pHead = None, pNext = None):
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
    def __init__(self, NETWORK_FILE_DIR = None, DIFFUSION_FILE_DIR = None, NETWORK_CONSTRAINT_FILE_DIR = None, PAGE_RANK_FILE_DIR = None ):
        self.TIME_STEP = -1
        self.NETWORK_FILE_DIR = NETWORK_FILE_DIR   # network file
        self.DIFFUSION_FILE_DIR = DIFFUSION_FILE_DIR # diffusion file dir
        self.NETWORK_CONSTRAINT_FILE_DIR = NETWORK_CONSTRAINT_FILE_DIR # network constraint file
        self.PAGE_RANK_FILE_DIR = None # PR
        self.nodeList = []    # Node pointer vector. loaded from network.txt
        self.postList = None    # Post pointer vector. loaded from posts.txt
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
        

        


    def LoadNetwork(self, filedir):
        print("########Loading Network Data########")
        file = open(filedir)
        line = file.readline()
        count = 0
        while line:
            tokens = line.strip().split(" ")
            # print(line)
            if len(tokens) < 1:
                continue
            count = count + 1
            if count % 100000 == 1:
                print("Loading", count, "th line")
            
            source = self.GetOrInsertUserId(tokens[0])
            '''
                // usw map in STL to find whether the use has been processed
                // if does, return its ID. if not, make a KVP and return a new id,
                // and push a new Node in nodeList
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
                pri#nt(self.nodeList[source].name, " ", self.nodeList[source].outEdgeList[len(self.nodeList[source].outEdgeList) - 1].name)
            # 这里得到的是所有入/出关系

            # 这里显然可以改进！！！！！！！！！！！！！！！！
            temp = len(self.nodeList)
            for j in range(temp):
                thisNode = self.nodeList[j]
                self.nodeList[j].outEdgeIdList = []
                for k in range(len(thisNode.outEdgeList)):
                    self.nodeList[j].outEdgeIdList.append(thisNode.outEdgeList[k].id)
                self.nodeList[j].outEdgeIdList.sort()
                # print(j, " ", self.nodeList[j].outEdgeIdList)
            line = file.readline()
        # print(self.userIdMap)
        # print(len(self.userIdMap))
        # self.userIdMap, nodeList测试通过
        # print(self.nodeList[0].outEdgeList[0].name)
        # for i in range(len(self.userIdMap)):
        #     print(i, " ", self.nodeList[i].outEdgeList[0].name)
        # print(self.nodeList[11].name)
        print("Load", count, "users in total")
        return 0



    def LoadDiffusion(self, filedir):
        pass
    
    def LoadFeature(self, filedir): 
        pass

    def GetUserId(self, key):
        pass

    def GetPostId(self, key):
        pass
    
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
        pass
