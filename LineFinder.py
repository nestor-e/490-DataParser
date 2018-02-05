#  Associates line numbers with the tablet Id's they are part of using binary search

import Parse

class LineFinder:
    def __init__(self, data):
        self.tabList = sorted( data, key= lambda tab: tab['startsOn'] )

    def findId(self, lineNum, expectedName = None):
        q = 0;
        r  = len(self.tabList)
        found = None
        while q < r:
            mid = (q + r) // 2
            midTab = self.tabList[mid]
            if midTab['startsOn'] > lineNum:
                r = mid
            elif midTab['endsOn'] < lineNum:
                q = mid + 1
            else:
                q = r
                found = midTab
        if found != None and expectedName != None:
            # Check if expectedName appears in tablet
            pass
        return found
