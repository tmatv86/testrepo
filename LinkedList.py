import time

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data

    def getById(self, value):
        if self.data == value:
            return self
        return None

class LinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def insert_first(self, val):
        new_node = Node(val)
        new_node.next = self.head
        self.head = new_node
        self.tail = self.head

    # insert to a position
    def insertTo(self, position:int, val):
        node = Node(val)
        nextNode = self.head
        counter = 1
        while True:
            counter += 1
            if counter == position:
                node.next = nextNode.next
                nextNode.next = node
                break
            nextNode = nextNode.next

    def remove(self, val):
        delNode = self.head
        if self.head.data == val:
            self.head = delNode.next
            return
        while delNode is not None:
            if delNode.next.data == val:
                delNode.next = delNode.next.next
                break
            delNode = delNode.next

    def insert_last(self, val):
        new_node = Node(val)
        if self.head is None:
            self.head = new_node
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        self.tail = last.next

    def search_value(self, val):
        node = self.head
        while node is not None:
            if node.data == val:
                return node.data
            node = node.next
        return None

    def insert_next(self, val):
        new_node = Node(val)
        if self.tail is not None:
            self.tail.next = new_node
            self.tail = new_node

    def insertBefore(self, prev1, val):
        new_node = Node(val)
        curNode = self.head
        while curNode is not None:
            if curNode.next.data == prev1:
                new_node.next = curNode.next
                curNode.next = new_node
                break
            curNode = curNode.next

    # return Node current instance
    def get_instance(self, val):
        import gc
        for g in gc.get_objects():
            if isinstance(g, Node) and (g.getById(val) != None):
                return g
        return None
    def insertAfter(self, old, val):
        old_el = Node(old)
        node = Node(val)
        curNode = self.head
        while curNode:
            if curNode.data == old_el.data:
                node.next = curNode.next
                curNode.next = node
            curNode = curNode.next

    def fast_insertAfter(self, old, val):
        old_el = Node(old)
        node = Node(val)
        currNode = self.get_instance(old_el.data)
        node.next = currNode.next
        currNode.next = node


    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return "->".join(nodes)

if __name__ == '__main__':


    # Linked list tests:
    llist = LinkedList()
    llist.insert_first('A')
    llist.insert_last('Z')
    llist.insertTo(2, 'R')
    llist.insertTo(3, 'U')
    llist.insertTo(3, 'P')
    llist.insertTo(3, 'N')
    llist.insert_last('B')
    # print(llist)
    llist.insertAfter('R', 'T')
    llist.insertAfter('U', 'K')
    llist.insertBefore('T', 'E')
    llist.insertBefore('E', 'M')
    llist.insertAfter('M', 'W')
    llist.insert_first('D')
    llist.remove('Z')
    llist.insert_last('C')
    llist.insert_next('H')
    llist.insert_next('L')
    llist.insert_next('S')
    llist.insertAfter('P', 'X')
    llist.insertAfter('K', 'J')
    
    val = llist.search_value('P')
    if val:
        print("Element exists: ", val)
    else:
        print("Element does not exist!")


    llist.insertAfter('L', 'TT')
    print(llist)
    llist.remove('H')
    llist.remove('D')
    llist.remove('A')
    llist.insert_first('V')


    nlist = LinkedList()
    nlist.insert_first('F')

    timebef = time.time()
    for s in range(34, 126):
        nlist.insert_next(chr(s))
    timeafter = time.time()

    print(timeafter - timebef)
    print(nlist)
    llist.insertBefore('E', 'Y')
    llist.insertAfter('K', 'N')
    print(llist)






