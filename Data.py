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
    def __init__(self, pHead = None, pNext = None):
        self.head = pHead
        self.length = 0
        self.next = pNext

    def append(self, thisNode):
        item = thisNode
        if isinstance(thisNode, NodeAttr):
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

    def append(self, thisPost):
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
    def __init__(self):
        self.TIME_STEP = -1
        self.NETWORK_FILE_DIR = None   # network file
        self.DIFFUSION_FILE_DIR = None # diffusion file dir
        self.NETWORK_CONSTRAINT_FILE_DIR = None # network constraint file
        self.PAGE_RANK_FILE_DIR = None # PR
        self.nodeList = None  # Node pointer vector. loaded from network.txt
        self.postList = None  # Post pointer vector. loaded from posts.txt
        self.userIdMap = {} # KVP of user string and user id(1, 2, 3...)
        self.postIdMap = {} # KVP of post string(1st attr) and post id(1, 2, 3...)
        self.sourceIdMap = {}; # KVP of source id(second attr in postList) and (1, 2, 3...)
                                     # what is a source id?
    
    def LoadData():
        pass

    def LoadNetwork(filedir):
        pass

    def LoadDiffusion(filedir):
        pass
    
    def LoadFeature(filedir): 
        pass

    def GetUserId(key):
        pass

    def GetPostId(key):
        pass
    
    def GetOrInsertUserId(key):
        pass

    def GetOrInsertPostId(key):
        pass

    def GetOrInsertSourceId(key):
        pass
