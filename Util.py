class TwoKey(object):
    def __init__(self, _str, _len):
        self.str = _str
        self.len = _len

class FileNodeAttr(object):
    def __init__(self, _str, _addr):
        self.str = _str
        self.addr = _addr

class FileNode(object):
    def __init__(self, pHead = None, pNext = None):
        self.head = pHead
        self.length = 0
        self.next = pNext

    def append(self, thisNode):
        item = thisNode
        if isinstance(thisNode, FileNodeAttr):
            item = thisNode
        else:
            print("error in FileNode in Util.py")

        if not self.head:
            self.head = item
            self.length += 1
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = item
            self.length += 1 


class Util(object):
    '''
    static vector<string> ReadFromFile( const char* fileDir);
    static vector<string> ReadFromFile(const char* fileDir, bool flag);
	static vector<string> StringTokenize(string line);
	static int TimeCompare(string t1, string t2);
	static vector<string> StringSplit(string line, char separator);
	static string Int2Str(int num);
	static int String2Int(string str);
	static long StringSplit(char *buffer, long  beginning, char separator); 
	static void LineInsert(FileNode *head, FileNode* newNode);
	static long PosNext( char *buffer, long pos);
	static void SaveToFile(const char* fileDir, char *buffer, long len);
	static long StrToInt(const char * str, const long beg);
	static bool IfEnd(char *buffer, long pos);
    static double String2Double(string str);
    '''
    pass
    
