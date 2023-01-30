class MyLinkedList:
    def __init__(self):
        self.listsize = 0
        self.list = []

    def addnode(self, string):
        node = Node(string)
        self.list.append(node)
        self.listsize += 1

        if (self.listsize > 1):
            prevnode = self.list[self.listsize-1]
            prevnode.setnext(node)
            node.setprev(prevnode)

    def removenode(self, index):
        if (self.listsize > 0):
            self.listsize -= 1
            prevnode = self.list[index - 1]
            nextnode = self.list[index + 1]
            self.list.pop(index)
            prevnode.setnext(nextnode)
            nextnode.setprev(prevnode)

    def getnode(self, index):
        return self.list[index]

    def getallnodes(self):
        return self.list

    def getsiblings(self, index):
        if (index - 1) >= 0:
            prevnode = self.list[index - 1]
        else:
            prevnode = "no previous nodes"
        if (index + 1) < self.listsize:
            nextnode = self.list[index + 1]
        else:
            nextnode = "no next nodes"

        return [prevnode, nextnode]

    def size(self):
        return self.listsize

    def tostring(self):
        for node in self.list:
            print(node.tostring())

class Node:
    def __init__(self, name):
        self.name = name

    def getnext(self):
        return self.next

    def setnext(self, node):
        self.next = node

    def getprev(self):
        return self.prev

    def setprev(self, node):
        self.prev = node

    def tostring(self):
        return self.name






