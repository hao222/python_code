# -*- coding:utf-8 -*-
# @author wuhao
# @date 2022/2/18

class Node(object):
    """
    定义单链表节点类
    """

    def __init__(self, data, next=None):
        """data为数据项，next为下一节点的链接，初始化节点默认链接为None"""
        self.data = data
        self.next = next


class LinkList:
    def __init__(self):
        self.head = None
        self.length = 0

    def demo(self):
        # 定义3个节点对象分别为node1、node2和node3
        node1 = None
        node2 = Node(1, None)
        node3 = Node('hello', node2)
        print(node1, node2.data, node2, node3.next)

    def createLinkedList(self):
        """创建5个节点， 数据项分别为  10,8,6,4,2的链表"""
        for count in [2, 4, 6, 8, 10]:
            self.head = Node(count, self.head)
            self.length += 1
        return self.head, self.length

    def printlinkedlist(self):
        i = self.length
        ls = []
        temp = self.head
        while i > 0:
            ls.append(temp.data)
            temp = temp.next
            i -= 1
        print(ls)

    def traversal(self):
        """遍历"""
        head = None
        for count in range(1, 6):
            head = Node(count, head)
        while head:
            print(head.data)
            head = head.next

    def search_target(self, targetItem):
        """搜索某值"""
        temp = self.head
        while temp and targetItem != temp.data:
            temp = temp.next
        if temp:
            print(targetItem, "success")
        else:
            print(targetItem, "fail")

    def search_index(self, index):
        """访问链表某一项"""
        temp = self.head
        while index > 0:
            temp = temp.next
            index -= 1
        print(temp.data)

    def replace_target(self, tar, new):
        """替换某个值"""
        temp = self.head
        while temp and tar != temp.data:
            temp = temp.next
        if temp:
            temp.data = new
            print(tar, "has been replaced by ", new)
        else:
            print(tar, "is not in linkedlist")

    def replace_index(self, index, new):
        """替换链表某一项"""
        temp = self.head
        while index > 0:
            temp = temp.next
            index -= 1
        temp.data = new

    def insert_at_end(self, new):
        """在末尾插入元素"""
        if self.head is None:
            self.head = Node(new, self.head)
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = Node(new, None)
        self.length += 1

    def insert_anywhere(self, index, new):
        """在任意位置插入"""
        if self.head is None or index <= 0:
            self.head = Node(new, self.head)
        else:
            temp = self.head
            while index > 1 and temp.next:
                temp = temp.next
                index -= 1
            temp.next = Node(new, temp.next)
        self.length += 1

    def delete_at_end(self):
        """在末尾删除元素"""
        if not self.head.next:
            self.head = None
        else:
            temp = self.head
            while temp.next.next:
                temp = temp.next
            remove_item = temp.next.data
            temp.next = None
        self.length -= 1

    def delete_any_where(self, index):
        """在任意位置删除元素"""
        if index <= 0 or self.head.next is None:
            remove_item = self.head.data
            self.head = self.head.next
        else:
            temp = self.head
            while index > 1 and temp.next.next:
                temp = temp.next
                index -= 1
            remove_item = temp.next.data
            temp.next = temp.next.next
        self.length -= 1




if __name__ == "__main__":
    l = LinkList()
    l.createLinkedList()
    l.search_target(6)
    l.search_index(3)